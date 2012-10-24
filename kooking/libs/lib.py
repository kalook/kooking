# -*- coding: utf-8 -*-
from jinja2 import FileSystemLoader, Environment

from django.http import HttpResponse
from django.conf import settings
import locale
import simplejson
import urllib

locale.setlocale(locale.LC_ALL, '')
template_dirs = getattr(settings,'TEMPLATE_DIRS')
default_mimetype = getattr(settings, 'DEFAULT_CONTENT_TYPE')
env = Environment(loader=FileSystemLoader(template_dirs))

def render_to_response(filename, context={},mimetype=default_mimetype):
    template = env.get_template(filename)
    rendered = template.render(**context)
    return HttpResponse(rendered,mimetype=mimetype)

def str_short(value):
    if value:
        return unicode(value.replace('<br />',''))
    else:
        return ''
    
def decimal(value):
	if not value:
		return 0
	return locale.format('%.f', value, 1)
	
    
def str_isEqual(value1,value2):
    return value1 == int(value2)

def isNumber(s):
  try:
    float(s)
    return True
  except ValueError:
    return False

import base64
def base64encode(s):
    if s :
        return base64.encodestring(s)
    else :
        return s
def split_fpage_event(s):
    if s:
        s = s.split("https://fpage.kr/event/")
        return s[1]
    else :
        s

def split_another_event(s):
    if s:
        s = s.split("/")
        return s[3]
    else :
        s

def convert_category(category,type):
    if type=="kor":
        category_eng_dic={
                u"전체":"all",
                u"영화":"movie",
                u"쇼핑":"shopping",
                u"인물":"person",
                u"게임":"game",
                u"교육":"education",
                u"스포츠":"sprots",
                u"출판":"publication",
                u"여행":"trevel",
                u"해외":"foreign",
                u"지역":"location",
                u"엔터테인먼트":"entertainment",
                u"의료":"medical",
                u"공연":"performance",
                u"기타":"etc",
                u"방송/언론":"media",
                u"기업":"business",
                u"기관/단체":"institute",
                u"브랜드":"brand",
            }
        print category_eng_dic[category]
        return category_eng_dic[category]
    else:
        category_eng_dic={
                "all":u"전체",
                "movie":u"영화",
                "shopping":u"쇼핑",
                "person":u"인물",
                "game":u"게임",
                "education":u"교육",
                "sprots":u"스포츠",
                "publication":u"출판",
                "trevel":u"여행",
                "foreign":u"해외",
                "지역":u"location",
                "entertainment":u"엔터테인먼트",
                "medical":u"의료",
                "performance":u"공연",
                "etc":u"기타",
                "media":u"방송/언론",
                "business":u"기업",
                "institute":u"기관/단체",
                "brand":u"브랜드",
            }
        return category_eng_dic[category]



def GenPasswd():
    import subprocess
    import random

    password = ''.join([random.choice('ABCDEFGHIJKLMNOPQRSTUV\
    WXYZabcdefghijklmnopqrstuvwxyz1234567890') for i in range(10)])
    return password

env.filters['convert_category'] = convert_category
env.filters['str_short'] = str_short
env.filters['str_isEqual'] = str_isEqual
env.filters['decimal'] = decimal
env.filters['split_another_event'] = split_another_event
env.filters['split_fpage_event'] = split_fpage_event
env.filters['base64encode'] = base64encode
