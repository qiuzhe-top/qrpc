'''
Author: 邹洋
Date: 2022-01-10 17:12:39
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2022-01-11 22:36:40
Description: 
'''

from .views import synchronous_api
from django.urls import path

urlpatterns = [
    path('synchronous_api',synchronous_api),
]