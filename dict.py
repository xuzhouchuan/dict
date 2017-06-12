#!/usr/bin/env python
# -*- coding:utf-8 -*-
########################################################################
# 
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
'''
File: dict.py
Author: baidu(baidu@baidu.com)
Date: 2017/06/12 17:13:40


Usage:  dict.py -f WORD_LIST_FILE [ -o OUTPUT_FILE]
        dict.py [-l | -y] -w WORD

Options:
    -h --help           Show this screen
    -f WORD_LIST_FILE   Word list file name
    -o OUTPUT_FILE      output file name
    -w WORD             word
    -l --local          from local dict
    -y --youdao         from youdao dict online
'''

import os
import sys
from bs4 import BeautifulSoup
import commands
import codecs
from docopt import docopt
import json

def get_youdao_meaning(word, q_yinbiao=False):
    page_content = commands.getoutput("curl -s http://youdao.com/w/eng/%s" % word)
    soup =  BeautifulSoup(page_content, "html.parser")
    meaning_tag = soup.find(id="phrsListTab")
    meaning_li = meaning_tag.find_all('li')
    meanings = [ele.string for ele in meaning_li \
            if ele.string is not None and ele.string != '']
    #yinbiao
    yinbiao_span = meaning_tag.find_all('span')
    yinbiao_out = {}
    if len(yinbiao_span) == 5:
        yinbiao_out[u'英'] = yinbiao_span[2].string 
        yinbiao_out[u'美'] = yinbiao_span[4].string
    if q_yinbiao:
        return yinbiao_out, meanings
    return meanings

if __name__ == '__main__':
    arguments = docopt(__doc__, version='0.0')
    if arguments["-f"] is not None:
        #word list file
        input_filename = arguments["-f"]
        output_filename = "%s.output" % input_filename \
                if arguments["-o"] is None else arguments["-o"]
        ofh = codecs.open(output_filename, 'w', 'utf-8-sig')
        with open(input_filename) as fh:
            lines = fh.readlines()
            for line in lines:
                segs = line.split('\t\t')
                word = segs[0]
                frequency = segs[1]
                attr = segs[2]
                meanings = get_youdao_meaning(word)
                print word
                ofh.write(u"%s\t%s\n" % (line.strip(), u'|'.join(meanings)))
        ofh.close()
        print "successful, output file is:%s" % output_filename
        sys.exit(0)

    if arguments["-w"] is not None:
        #get one word meaning
        word = arguments["-w"]
        if arguments["--youdao"]:
            yinbiaos,meanings = get_youdao_meaning(word,True)
            for key, value in yinbiaos.iteritems():
                print "%s:%s" % (key, value)
            for mean in meanings:
                print mean
        else:
            dict_json = json.load(open('dict.json', 'r'))
            if word in dict_json:
                print dict_json[word]
            else:
                print "Local dict not find"


