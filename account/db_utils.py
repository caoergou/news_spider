#!/usr/bin/env python
# encoding: utf-8
"""
File Description: 
Author: nghuyong
Mail: nghuyong@163.com
Created Time: 2020/4/9
"""
import pymongo
from pymongo.errors import DuplicateKeyError

mongo_client = pymongo.MongoClient(host='mongodb')
collection = mongo_client["weibo"]["account"]


def insert_cookie(username, password, cookie_str):
    """
    insert cookie to database
    :param username: username of weibo account
    :param password: password of weibo account
    :param cookie_str: cookie str
    :return:
    """
    try:
        collection.insert(
            {"_id": username, "password": password, "cookie": cookie_str, "status": "success"})
    except DuplicateKeyError as e:
        collection.find_one_and_update({'_id': username}, {'$set': {'cookie': cookie_str, "status": "success"}})


if __name__ == '__main__':
    # You can add cookie manually by the following code, change the value !!
    insert_cookie(
        username='17035756478',
        password='ORBtws829I4',
        cookie_str='_T_WM=489d4efaebc3ebf0844391f12a6706ad; SCF=Ag1WoDPqtdKiXoGEjVi2m28hNistuUBzQg4Cb05jPk-Tr5zssBLvJx1fekPfR3mvT9NocoR6IdQ22q9PNS8hB6M.; SUB=_2A25MNwPoDeRhGeFO4lYX9SvKwjSIHXVv262grDV6PUJbktB-LWrykW1NQVWbjZdImCGw5WIbVSzw6vPvzd0_DACB; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhPaMQ8aNHSbKAQc_YZ1-qU5NHD95QNeh.XSo-fSo.RWs4Dqc_hi--ciK.Ni-24i--Xi-zRiKyWi--NiKLWiKnXi--Ri-i8i-zEi--ci-8hi-2pi--ci-8hi-2pi--ci-8hi-2p1h-Xe5tt'
    )
