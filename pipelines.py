# -*- coding: utf-8 -*-
import pymongo
import redis
from pymongo.errors import DuplicateKeyError

from settings import MONGO_HOST, MONGO_PORT


class MongoDBPipeline(object):

    def __init__(self):
        mongo_client = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
        db = mongo_client['weibo']
        self.redis_client = redis.Redis(host='redis')
        self.Users = db["Users"]
        self.Relationships = db["Relationships"]

    def process_item(self, item, spider):
        if item is None:
            print("got Nothing!")
            return None
        dic = dict(item)
        le = len(item)
        spider.logger.debug(f"what is item :{le}")
        if spider.name == 'fan_spider':
            self.insert_item(self.Relationships, dic)
            if not self.check_exist(self.redis_client, dic.get("_id")):
                self.redis_add_val(self.redis_client, spider.name, dic.get("fan_id"))
        elif spider.name == 'follower_spider':
            self.insert_item(self.Relationships, dic)
            if not self.check_exist(self.redis_client, dic.get("_id")):
                self.redis_add_val(self.redis_client, spider.name, dic.get("followed_id"))
        elif spider.name == 'user_spider':
            dic['potential'] = False
            if self.check_user(dic):
                dic['potential'] = True
                if not self.check_exist(self.redis_client, dic.get("_id")):
                    self.redis_add_val(self.redis_client, spider.name, dic.get("_id"))
            self.insert_item(self.Users, dic)
            self.insert_uid(self.redis_client, dic.get("_id"))
        return item

    @classmethod
    def check_user(cls, dic):
        fields = [('昵称', 'nick_name'),
                  ('简介', 'brief_introduction'),
                  ('教育经历', 'education')]

        keywords = {
            "复旦大学": ["复旦", "FDU", "光华"],
            "同济大学": ["TJU", "同济", "Tongji", "四平路"],
            "上海交通大学": ["上海交通大学", "上海交大", "SJTU", "上交"],
            "上海财经大学": ["SUFE", "上财", "上海财经大学"],
            "华东师范大学": ["华东师范", "ECNU", "华东师大"],
            "华东理工大学": ["华东理工", "华理", "ECUST"],
            "上海外国语大学": ["上海外国语", "上外", "SISU", "松江大学城"],
            "华东政法大学": ["ECUPL", "华政", "华东政法"],
            "上海中医药大学": ["SHUTCM", "上中医", "上海中医药大学"],
            "上海对外经济贸易大学": ["上经贸大", "上海对外经济贸易大学", "上海对外经贸", "SUIBE"],
            "上海工程技术大学": ["工程大", "上海工程技术大学", "SUES"],
            "上海立信会计金融学院": ["上海立信会计金融学院", "立信金融"],
            "上海应用技术大学": ["上海应用技术大学", "上应大", "应技大"],
            "上海大学": ["上海大学", "SHU", "上大"],
            "上海理工大学": ["上海理工大学", "USST", "上理"],
            "上海音乐学院": ["上音", "上海音乐学院", "SHCM"],
            "上海海洋大学": ["上海海洋大学", "SHOU", "临港大学城"],
            "上海海事大学": ["上海海事大学", "上海海大", "海大", "SMU"],
            "上海体育学院": ["上体", "上海体育学院"],
            "上海师范大学": ["上海师范大学", "上师大", "上师", "SHNU"],
            "东华大学": ["东华大学", "DHU", "东华"],
            "上海电力大学": ["上海电力学院", "上海电力大学", "SUEP"],
            "上海戏剧学院": ["上戏", "上海戏剧学院", "STA"]
        }

        united_fields = " ".join([str(dic.get(kv[1])) for kv in fields])

        for keyword in keywords:
            for item in keywords[keyword]:
                if item in united_fields:
                    return True

        return False

    @staticmethod
    def insert_item(collection, dic):
        try:
            collection.insert(dic)
        except DuplicateKeyError:
            pass

    @staticmethod
    def redis_add_val(client, spider_name, uid):
        if spider_name == 'fan_spider' or spider_name == 'follower_spider':
            url = f"https://weibo.cn/{uid}/info"
            client.lpush(f'user_spider:start_urls', url)
        elif spider_name == 'user_spider':
            url = f"https://weibo.cn/{uid}/fans"
            client.lpush(f'fan_spider:start_urls', url)

            url = f"https://weibo.cn/{uid}/follow"
            client.lpush(f'follower_spider:start_urls', url)
        print('Added:', spider_name, uid)

    @staticmethod
    def insert_uid(client, uid):
        try:
            client.sadd("user", uid)
        except DuplicateKeyError:
            pass

    @staticmethod
    def check_exist(client, uid):
        return client.sismember("user", uid)

# class RedisPipeline(object):
#     def __init__(self):
#         self.client = redis.Redis(host='redis')

#     def process_item(self, item, spider):
#         if spider.name == 'fan_spider':
#             uid = item.fields.get("fan_id")
#             if not self.check_exist(uid):
#                 redis_add_val('user_spider', uid)
#                 self.insert_item(uid)
#                 print('Added:', item.fields.get("fan_id"))
#         elif spider.name == 'follower_spider':
#             uid = item.fields.get("followed_id")
#             if not self.check_exist(uid):
#                 redis_add_val('user_spider', uid)
#                 print('Added:', uid)
#         elif spider.name == 'user_spider':
#             uid = item.fields.get("_id")
#             if Sensor.check_user(item):
#                 redis_add_val('fan_spider', uid)
#                 redis_add_val('follower_spider', uid)
#                 print('Added:', uid)

#     def redis_add_val(self, spider_name, uid):
#         url = f"https://weibo.cn/{uid}/info"
#         self.client.lpush(f'{spider_name}:start_urls', url)
#         print('Added:', url)

#     def insert_item(self, uid: str):
#         try:
#             self.client.sadd("user", uid)
#         except DuplicateKeyError:
#             pass

#     def check_exist(self, uid: str):
#         return self.client.sismember("user", uid)
