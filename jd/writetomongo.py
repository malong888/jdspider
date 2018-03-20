# coding: utf-8
import redis
import json
import pymongo
import time

def process_items(limit=0,wait=0.1,timeout=5):
    # 连接redis
    redis_cilen = redis.StrictRedis('192.168.153.132', 6379, db=0)

    # 连接mongo
    mongo_client = pymongo.MongoClient(host='localhost', port=27017)
    db = mongo_client['jd']
    col = db['jd_data']

    limit = limit or float('inf')

    processed = 0
    i = 1
    # 判断redis的数据什么时间取完
    while processed < limit:
        ret = redis_cilen.blpop('jdsp:items',timeout)
        i = i+1
        print(i)
        #如果是None跳过此次循环
        if ret is None:
            time.sleep(wait)
            continue

        source, data = ret

        # 写入mongodb 前要转化data为dict
        col.insert(json.loads(data.decode("utf-8")))

if __name__ == '__main__':
    process_items()