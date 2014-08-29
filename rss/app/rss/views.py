#coding=utf-8
from django.template.loader import get_template
from django.template import Context
from django.template import Template
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.db import connection
import json
import models
import logging
from django.contrib.syndication.views import Feed
from django.utils import feedgenerator
# 主页

class WeixinRss(Feed):
    def __init__(self):
        self.title = ""
        self.link = "/feeds/"
        #描述
        self.description = ""

    def get_object(self, request, openid):
        return openid

    def items(self,openid):
        print openid
        weixin = models.WeiXin()
        items = weixin.get_items(openid)
        self.title = items["title"]
        self.description = items["description"]
        return items["items"]
    #订阅的标题
    def item_title(self, item):
        return item["title"]
    #订阅的表示
    def item_description(self, item):
        return item["content"]
    #每条订阅的链接
    def item_link(self,item):
        return item["link"]

def index(request):
    logging.info("hello open")
    return HttpResponse("hello")

def feed(request,openid):
    print "feed"
    print openid

    weixin = models.WeiXin()
    items = weixin.get_items(openid)
    feed = feedgenerator.Rss201rev2Feed(
        title=items["title"],
        link="/feed",
        description=items["description"],
        language="zh-cn"
    )
    for item in items["items"]:
        feed.add_item(title=item["title"],description=item["content"],link=item["link"])

    str = format(feed.writeString('utf-8'))
    return HttpResponse(str)

def format(str):
	str = str.replace('>', '>\n')
	str = str.replace('<', '\n<')
	str = str.replace('\n\n', '\n')
	return str
