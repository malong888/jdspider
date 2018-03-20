# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import scrapy

class JdItem(scrapy.Item):
    jd_img_url = scrapy.Field()#商品图片url
    jd_page_url = scrapy.Field()#详情页面url
    jd_product_price = scrapy.Field()#商品价格
    jd_shop_name = scrapy.Field()#店铺名字
    jd_comment_num = scrapy.Field()#总评论
    product_id = scrapy.Field()#商品id
    jd_good_count = scrapy.Field()# 好评数
    jd_gen_count = scrapy.Field()# 中评
    jd_bad_count = scrapy.Field()# 差评
    jd_add_count = scrapy.Field()# 追评
    jd_comments = scrapy.Field()#评论内容



