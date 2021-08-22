#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
import sys
import os
import json

#############################配置区##############################
#保存目录
path = r"D:\0file\Download"
#################################################################

#################################################################
############################代码区###############################
try:
    name = input("请输入漫画名字：")
    th = int(input("请输入漫画搜索结果排序位置（数字）："))
except:
    print("输入错误")
    sys.exit()

#—————————————————————————————函数区————————————————————————————#
#创建目录
def mkdir(path):
    folder = os.path.exists(path)
    if not folder:                   
    	os.makedirs(path)            
    else:
	    print (path + "目录已存在")
#请求
def request_get(url):
    try:
        headers = {"Uesr-Agent" : "Dart/2.10 (dart:io)", "region" : "1"}
        request_str = requests.get(url,headers=headers)
        request_str.encoding = 'utf-8-sig'
        return request_str
    except:
        print("访问失败，请检查网络")
        sys.exit()
#下再图片
def down(uuid,chaper):
    get_pictrue_url = "https://api.copymanga.com/api/v3/comic/{}/chapter2/{}".format(name_words[th],uuid)
    picture_str = request_get(get_pictrue_url)
    picture_str = json.loads(picture_str.text).get("results").get("chapter").get("contents")
    num = 1
    for i in picture_str:
        picture = request_get(i.get("url"))
        with open(chaper_path + "\{}.jpg".format(num),"wb") as code:
            code.write(picture.content)
        num = num + 1
    print("已下载" + chaper)

#——————————————————————————————————————————————————————————————#
if __name__ == "__main__":  # 程序入口
    #获取搜索结果
    search_url = "https://api.copymanga.com/api/v3/search/comic?limit=10&q={}".format(name)
    search_str = request_get(search_url)
    name_str = json.loads(search_str.text).get("results").get("list")
    name_words = {}
    names = {}
    num = 1
    for i in name_str:
        name_words.update({num : i.get("path_word")})
        names.update({num : i.get("name")})
        num += 1

    #创建漫画目录
    name_path = path + r'\{}'.format(names[th])
    mkdir(name_path)
    #获取每一话的uuid
    uuid_url = "https://api.copymanga.com/api/v3/comic/{}/group/default/chapters?limit=200".format(name_words[th])
    uuid_str = request_get(uuid_url)
    uuid_str = json.loads(uuid_str.text).get("results").get("list")
    for i in uuid_str:
        chaper = i.get("name")
        uuid = i.get("uuid")
        chaper_path = name_path + r"\{}".format(chaper)
        mkdir(chaper_path)
        down(uuid,chaper)
#################################################################
#################################################################



