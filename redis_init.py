#!/usr/bin/env python
# encoding: utf-8
"""
File Description: 
Author: nghuyong
Mail: nghuyong@163.com
Created Time: 2020/4/15
"""
import datetime
import sys

import redis


def redis_init(spider_name, urls):
    r = redis.Redis(host='redis')
    for key in r.scan_iter(f"{spider_name}*"):
        r.delete(key)
    print(f'Add urls to {spider_name}:start_urls')
    for url in urls:
        r.lpush(f'{spider_name}:start_urls', url)
        print('Added:', url)


def redis_add_val(spider_name, url):
    r = redis.Redis(host='redis')
    r.lpush(f'{spider_name}:start_urls', url)
    print('Added:', url)


def init_user_spider():
    # change the user ids
    user_ids = ['1087770692', '1699432410', '1266321801']
    urls = [f"https://weibo.cn/{user_id}/info" for user_id in user_ids]
    redis_init('user_spider', urls)


def add_user_to_spider(user_id):
    # change the user ids
    url = f"https://weibo.cn/{user_id}/info"
    redis_add_val('user_spider', url)


def init_fan_spider():
    # change the user ids
    user_ids = ['1087770692', '1699432410', '1266321801']
    urls = [f"https://weibo.cn/{user_id}/fans?page=1" for user_id in user_ids]
    redis_init('fan_spider', urls)


def add_user_to_fans_spider(user_id):
    # change the user ids
    url = f"https://weibo.cn/{user_id}/fans?page=1"
    redis_add_val('fan_spider', url)


def init_follow_spider():
    # change the user ids
    user_ids = ['1087770692', '1699432410', '1266321801']
    urls = [f"https://weibo.cn/{user_id}/follow?page=1" for user_id in user_ids]
    redis_init('follower_spider', urls)


def init_comment_spider():
    # change the tweet ids
    tweet_ids = ['IDl56i8av', 'IDkNerVCG', 'IDkJ83QaY']
    urls = [f"https://weibo.cn/comment/hot/{tweet_id}?rl=1&page=1" for tweet_id in tweet_ids]
    redis_init('comment_spider', urls)


def init_user_tweets_spider():
    # crawl tweets post by users
    user_ids = ['1087770692', '1699432410', '1266321801']
    urls = [f'https://weibo.cn/{user_id}/profile?page=1' for user_id in user_ids]
    redis_init('tweet_spider', urls)


def init_keyword_tweets_spider():
    # crawl tweets include keywords in a period, you can change the following keywords and date
    keywords = ['转基因']
    date_start = datetime.datetime.strptime("2017-07-30", '%Y-%m-%d')
    date_end = datetime.datetime.strptime("2017-07-30", '%Y-%m-%d')
    urls = []
    url_format_by_day = "https://weibo.cn/search/mblog?hideSearchFrame=&keyword={}&starttime={}&endtime={}&atten=1&sort=time&page=1"
    time_spread = datetime.timedelta(days=1)
    while date_start <= date_end:
        for keyword in keywords:
            # 添加按日的url
            day_string = date_start.strftime("%Y%m%d")
            urls.append(url_format_by_day.format(keyword, day_string, day_string))
        date_start = date_start + time_spread
    redis_init('tweet_spider', urls)


if __name__ == '__main__':
    mode = sys.argv[1]
    mode_to_fun = {
        'user': init_user_spider,
        'comment': init_comment_spider,
        'fan': init_fan_spider,
        'follow': init_follow_spider,
        'tweet_by_user_id': init_user_tweets_spider,
        'tweet_by_keyword': init_keyword_tweets_spider,
    }
    mode_to_fun[mode]()
