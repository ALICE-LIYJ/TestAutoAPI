#!/usr/bin/env python
# _*_coding:utf-8_*_
import requests

from log.log_record import log_print


def post_main(url, data, header):
    """
     post请求
     :param url:
     :param data:
     :param header:
     :return:
    """
    try:
        res = requests.post(url=url, json=data, headers=header)
        return res.json()
    except Exception as e:
        log_print().error(f"接口请求错误，请求参数：{data}，请求Url：{url}，请求结果：{res.json()}")


def get_main(url, header):
    """
    get请求
    :param url:
    :param header:
    :param param:
    :return:
    """
    try:
        res = requests.get(url=url, headers=header)
        return res.json()
    except Exception as e:
        log_print().info(f"接口请求错误，请求Url：{url}，请求结果：{res.json()}")


def run_main(method, url, header, data=None):
    """
    被调用主request
    :param method:
    :param url:
    :param header:
    :param data:
    :param file:
    :return:
    """
    try:
        res = None
        if method == 'post' or method == 'POST' or method == 'Post':
            res = post_main(url, data, header)
        elif method == 'get' or method == 'GET' or method == 'Get':
            res = get_main(url, header)
        else:
            log_print().error(f"请求方法：{method}格式错误")
        return res
    except Exception as e:
        log_print().error(f"请求方法报错{e}")


if __name__ == '__main__':
    pass
