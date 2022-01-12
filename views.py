'''
Author: 邹洋
Date: 2022-01-10 17:14:19
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2022-01-12 10:35:25
Description: 
'''
import json
import logging
import threading
import time
from collections import OrderedDict

import requests
from cool.views import CoolAPIException, CoolBFFAPIView, ErrorCode, ViewSite
from cool.views.utils import get_api_info, get_url, get_view_list
from django.conf import settings
from django.conf.urls import url
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.urls.resolvers import URLPattern, URLResolver
from django.utils.module_loading import import_string

from . import models

log = logging.getLogger(__name__)

QRPC_SERVERS_URL = settings.QRPC_SERVERS_URL  # ('http://127.0.0.1:8000',)
QRPC_LOCA = settings.QRPC_LOCA  #'http://127.0.0.1:8000'
RPC_URL = '/qrpc/synchronous_api'

API_DATA = []


def api_dict():
    # 获取本机系统接口函数名称
    if API_DATA:
        return API_DATA
    else:
        views = get_view_list()
        for v in views:
            view_class = v['view_class']
            cl = str(view_class)
            i = cl.rfind('.')
            url = QRPC_LOCA + get_api_info(view_class)['apis'][0]['url']
            function = cl[i + 1 : -2]
            API_DATA.append({"function": function, "url": url})
            # print(api)
    save_api(API_DATA)
    return API_DATA


def synchronous_api(request):
    '''
    获取接口
    '''
    d = api_dict()
    data = json.loads(request.body)
    return JsonResponse(d, safe=False)

def req(url,data):
    headers = {"Content-type": "application/json"}
    data = json.dumps(data)
    return requests.post(url, data, timeout=5, headers=headers)
    # return requests.post(url, data, timeout=5)

class Send(threading.Thread):
    # 携带自己的api数据去交换对方的api数据
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url

    def run(self) -> None:
        try:
            data = api_dict()
            res = req(self.url + RPC_URL, data)
            status_code = res.status_code
            if status_code == 200:
                data = res.json()
                save_api(data)
                print("本机与"+self.url + " 成功同步")
            else:
                print("本机与"+self.url + " 请求状态异常", status_code)
        except Exception as e:
            log.error(e)
            log.error(self.url+"同步失败")


def save_api(data):
    for d in data:
        o, f = models.Api.objects.update_or_create(
            function=d['function'], defaults={'url': d['url']}
        )


def init():
    for url in QRPC_SERVERS_URL:
        if url != QRPC_LOCA:
            Send(url).start()

init()


def qrpc(function,data):
    '''
    模仿rpc调用

    Args:
        url ([type]): [description]
    '''
    url = models.Api.objects.get(function=function).url
    data = req(url,data).json()
    return data['data']
