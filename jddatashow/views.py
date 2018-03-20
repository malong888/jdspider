from django.shortcuts import render
from . import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from decimal import Decimal

# 获取数据，分页
def jddatashow(request):
    items = models.Jd_data.objects.order_by('-jd_comment_num')[:30]
    # 获取价格, 名字
    price_list = []
    phone_name= []
    for i in items:
        price_list.append(i['jd_product_price'][:8])
        phone_name.append(i['jd_shop_name'][:1])

    per_page= 30
    paginator = Paginator(items, per_page) # 每页展示10数据, 少于2条合并到上一页中
    page = request.GET.get("page") # 获得当前的页数
    try:
        rows = paginator.page(page)
    except PageNotAnInteger:
        rows = paginator.page(1) #如果输入的不是整数， 就显示第一页
    except EmptyPage:
        rows = paginator.page(paginator.num_pages) # 如果是空的就展示最后一页
    return render(request, 'jdshow/index.html', {"items": rows, 'prices': price_list, 'names': phone_name})

# 详情页
def jd_detail(request, question_id):
    items = models.Jd_data.objects(product_id=str(question_id))
    url = items.first().jd_page_url
    good_count = items.first().jd_good_count # 好评数量
    bad_count = items.first().jd_bad_count
    gen_count = items.first().jd_add_count
    comment_count = items.first().jd_comment_num
    good_comment_rate = '%.2f%%'%(Decimal(good_count)/int(comment_count)*100)
    bad_comment_rate = '%.2f%%'%(Decimal(bad_count)/int(comment_count)*100)
    gen_comment_rate = '%.2f%%'%(Decimal(gen_count)/int(comment_count)*100)

    good_comment_num = Decimal(good_count) / int(comment_count) * 100
    bad_comment_num = Decimal(bad_count)/int(comment_count)*100
    gen_comment_num = Decimal(gen_count)/int(comment_count)*100

    data = {
            'url':url,'comment_num':comment_count,
            'good_rate': good_comment_rate,'bad_rate':bad_comment_rate, 'gen_rate':gen_comment_rate,
            'good':good_count, 'bad':bad_count, 'gen':gen_count, 'id': question_id,
            'good_comment_num':good_comment_num,'bad_comment_num':bad_comment_num,'gen_comment_num':gen_comment_num
            }

    return render(request, 'jdshow/detail.html', {"items":items, "data": data})