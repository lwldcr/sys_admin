#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# check url record file and build download mission
# 2014/1/11 lwldcr@gmail.com

import os,sys

url_rec = '/srv/ftp/pub/upload/url.txt'

def download(url):
    """Start download file from given url."""
    if not url:
        print "No url given!"
        sys.exit(1)

    keywords = [".youku",
                ".tudou",
                ".iqiyi",
                ".ku6",
                ".souhu",
                ".qq",
                ".56",]

    sitename = ""
    for key in keywords:
        if str(url).find(key) != -1:
            sitename = key.replace('.','')
            break
            
    if not sitename:
        print "Not supported site: %s " % url
        sys.exit(1)
    if sitename == '56':
        sitename = 'w56'

    cmd = 'lx ' + sitename + ' ' + url
    try:
        os.system(cmd)
    except:
        pass

def main():
    """Main."""
    if not os.path.isfile(url_rec):
        print "Fatal: \"%s\" does not exist!" % url_rec
        sys.exit(1)

    f = open(url_rec)
    urls = f.readlines()
    f.close()
    try:
        os.remove(url_rec)
    except:
        pass

    for url in urls:
        download(url)

if __name__ == '__main__':
    main()
