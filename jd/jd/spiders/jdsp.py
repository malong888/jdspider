# -*- coding: utf-8 -*-
import scrapy
from jd.items import JdItem
from scrapy.http import Request
import json
import re
import random
import requests
from scrapy_redis import spiders
from scrapy.spiders import Rule,CrawlSpider
from scrapy.linkextractors import LinkExtractor#提取页面链接工具
import time
from scrapy_redis.spiders import RedisCrawlSpider

class JdspSpider(RedisCrawlSpider):
    name = 'jdsp'
    allowed_domains = ['jd.com', 'p.3.cn']
    redis_key = 'jd:start_urls'

    #start_urls = ['http://list.jd.com/list.html?cat=9987,653,655&page=1']

    rules = [
        # 商品列表
        Rule(LinkExtractor(allow=r"page=\d+?"), callback='parse_item', follow=True),
        ]

    def parse_item(self, response):
        reg_num = re.compile('page=(\d+?)')
        num = re.search(reg_num,response.url).group(1)
        print("正在翻页%s"%(num))

        gl_items = response.xpath('//li[@class="gl-item"]')

        base_price_url = 'https://p.3.cn/prices/mgets?callback=jQuery%s&skuIds=J_%s&pduid=%s'

        for gl_item in gl_items:
            item = JdItem()
            #店铺名字
            item['jd_shop_name'] = gl_item.xpath('./div/div[@class="p-shop"]/@data-shop_name').extract_first()

            #物品id
            item['product_id'] = gl_item.xpath('.//div/@data-sku').extract_first()

            #详情页面url
            item['jd_page_url'] = 'http://' + gl_item.xpath('.//div[@class="p-img"]/a/@href').extract_first()

            #每个商品价格url
            price_url = base_price_url%(item['product_id'],item['product_id'],random.randint(0,1000000))

            #商品图片url
            jd_img_url = gl_item.xpath('.//img[@height="220"]/@src | .//img[@height="220"]/@data-lazy-img').extract_first()
            item['jd_img_url'] = 'https:' + jd_img_url

            yield Request(url=price_url,callback=self.parse_price,meta={'item':item})

    #解析价格
    def parse_price(self,response):
        item = response.meta['item']
        # resp.text返回的是Unicode型的数据
        # resp.content返回的是bytes型也就是二进制的数据
        # 也就是说，如果你想取文本，可以通过r.text
        # 如果想取图片，文件，则可以通过r.content
        price_json = response.text
        reg = re.compile('jQuery\d+\(\[(.*?)\]\)')
        price_dict = re.search(reg,price_json).group(1)

        #json转成字典
        #商品价格
        item['jd_product_price'] = json.loads(price_dict)['p']

        yield Request(url=item['jd_page_url'],callback=self.parse_detail,meta={'item':item})

    #详情页面解析
    def parse_detail(self,response):

        product_id = response.meta['item']["product_id"]

        # 5 是推薦排序， 6是按照時間排序
        url = 'http://club.jd.com/comment/productPageComments.action?productId=%s&score=0&sortType=6&page=0&pageSize=10'% (product_id)

        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Host': 'club.jd.com',
            'Referer': 'https://item.jd.com/%s.html' % product_id,  # 引用的url
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:52.0) Gecko/20100101 '
                          'Firefox/52.0',
        }

        yield scrapy.Request(url=url,callback=self.get_all_comment,headers=headers,method='GET',meta={'item': response.meta['item']})

    #爬取评论num
    def get_all_comment(self, response):
        item = response.meta['item']
        product_id = response.meta['item']["product_id"]

        if response:
            data = json.loads(response.text)

            #商品评分
            productCommentSummary = data.get('productCommentSummary','')
            if productCommentSummary:
                item['jd_comment_num'] = productCommentSummary.get('commentCount','')#总评论数
                item['jd_good_count'] = productCommentSummary.get('goodCount','')  # 好评数
                item['jd_gen_count'] = productCommentSummary.get('generalCount','')  # 中评
                item['jd_bad_count'] = productCommentSummary.get('poorCount','')  # 差评
                item['jd_add_count'] = productCommentSummary.get('afterCount','')  # 追评


        comment_info_list = []
        for i in range(1,3):
            # 5 是推薦排序， 6是按照時間排序
            url = 'http://club.jd.com/comment/productPageComments.action?productId=%s&score=0&sortType=6&page=%s&pageSize=10'%(product_id,i)
            response = requests.get(url)

            if response:
                data = json.loads(response.text)
                #商品评论
                comments = data.get('comments','')
                for comment in comments:
                    comment_info_dict = {}
                    comment_info_dict['jd_content'] = comment['content']
                    comment_info_dict['jd_creationTime'] = comment.get('creationTime','')
                    comment_info_dict['jd_userClientShow'] = comment.get('userClientShow', '')
                    comment_info_dict['jd_id'] = comment.get('id', '')
                    comment_info_dict['jd_userLevelName'] = comment.get('userLevelName', '')
                    comment_info_list.append(comment_info_dict)

        item['jd_comments'] = comment_info_list

        yield item