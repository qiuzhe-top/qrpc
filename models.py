'''
Author: 邹洋
Date: 2022-01-10 17:33:43
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2022-01-11 18:31:07
Description: 
'''

from django.db import models
class Api(models.Model):
    function = models.CharField(blank=False, max_length=100)
    url = models.CharField(blank=False, max_length=100)
    star_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建日期')
    last_time = models.DateTimeField(auto_now=True, verbose_name=u'最后修改日期')
