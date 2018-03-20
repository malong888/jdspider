from django.db import models
import mongoengine

class Jd_data(mongoengine.Document):
    """此时不是继承与models.Model, 是继承Document类"""
    # 参数如果required=True, 必须要实例化，也就是不能为空，如果为空就抛出ValidationError错误
    product_id = mongoengine.StringField(required=True)  # 商品ID
    #product_name = mongoengine.StringField(required=True)  # 商品名字
    jd_img_url = mongoengine.StringField(required=True, max_length=200) #商品图片url
    jd_page_url = mongoengine.StringField(required=True, max_length=200)  # 商品链接
    jd_shop_name = mongoengine.StringField(required=True, max_length=200)  # 店家名字
    jd_product_price = mongoengine.IntField(required=True)  # 价钱
    jd_comments = mongoengine.ListField()  # 评论的详情
    jd_comment_num = mongoengine.IntField(required=True)  # 评论数
    jd_good_count = mongoengine.IntField(required=True)  # 好评数
    jd_gen_count = mongoengine.IntField(required=True)  # 中评数
    jd_bad_count = mongoengine.IntField(required=True)  # 差评
    jd_add_count = mongoengine.IntField(required=True)  # 追评

    #自定义的管理
    meta = {
        'collection': 'jd_data',  # 指定要链接的集合
        'ordering': ['-jd_product_price'],  # 默认商品价格排序
    }
