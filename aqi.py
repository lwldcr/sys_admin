#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 2013/12/06
# lwldcr@gmail.com

# updated: 2013/12/11
# fetch_air_html():  
############################################
#html = ''.join(fs[28:31]).replace('\n','') 
#html = fs[0].replace('\n','')
###########################################
# parse_html():
##############################
# d_air[city] = air_info
# d_air[city] = air_info[5:8]
##############################

import os, sys, urllib
from HTMLParser import HTMLParser

class MyHtmlParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.info = []

    def handle_data(self, data):
        data = str(data).replace(' ','').decode("gbk")
        if data:
            self.info.append(data)

weather_file = '/Users/brucelee/Documents/weather.txt'

d_city = {
        "Shanghai": ["58362", "上海"],
        "Beijing": ["54511", "北京"],
        "Hangzhou": ["58457", "杭州"],
        "Guangzhou": ["59287", "广州"],
        "Shenzhen": ["59493", "深圳"],
        "Wuhan":    ["57494", "武汉"],
        "Nanjing":  ["58238", "南京"],
        "Hefei":    ["58321", "合肥"],
        "Bengbu":   ["58221", "蚌埠"],
        "Qingdao":  ["54857", "青岛"],
        "Suzhou":   ["58357", "苏州"],
        "Wuxi": ["58354", "无锡"],
        "Changzhou":["58343", "常州"],
        "Yangzhou": ["58245", "扬州"],
        "Xi'an":    ["57036", "西安"],
        "Ha'erbin": ["50953", "哈尔滨"],
        }

d_air = {}

site = 'waptianqi.2345.com/'

def fetch_air_html(city):
    "Fetch air quality page."
    if city not in d_city.keys():
        print "city: %s not recorded,exiting..." % (city)

    seq_num = d_city[city][0]
    air_suffix = 'air-' + seq_num + '.htm'
    full_url = 'http://' + site + air_suffix
    try:
        skt = urllib.urlopen(full_url)
    except:
        print "Open url error: %s" % (full_url)
        sys.exit(1)

    fs = skt.readlines()
    try:
        html = fs[0].replace('\n','')
    except:
        pass
    if not html:
        print city
    return html

def parse_html(city,html):
    """Parse html."""
    if not html:
        print "Blank HTML feed, exiting..."
        sys.exit(1)
    myParser = MyHtmlParser()
    myParser.feed(html)
    myParser.close()

    air_info = []
    for i in myParser.info:
        if i:
            air_info.append(i)
    if air_info:
        d_air[city] = air_info[5:8]

def r_date():
    """return date info."""
    from datetime import datetime
    return datetime.today().strftime("%Y/%m/%d %a %H:%M")

def main():
    """Main loop."""
    for city in d_city.keys():
        h = fetch_air_html(city)
        parse_html(city,h)

    try:
        f = open(weather_file,'a+')
    except IOError:
        f = open(weather_file,'w')
    date_rec = '\n' + str(r_date()) + '\n'
    f.write(date_rec)

    for rec in sorted(d_air.iteritems(), key = lambda a:int(a[1][0]), reverse = False):
        air_str = rec[1][0] + '\t' + rec[1][1] + ':' + rec[1][2]
        loc_rec = "%-8s\t%s\n" % (d_city[rec[0]][1].decode('utf-8'), air_str)
        print loc_rec,
        f.write(loc_rec.encode('utf-8'))

    f.close()

if __name__ == '__main__':
    main()
