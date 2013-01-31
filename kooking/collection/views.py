#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.core.serializers import serialize
from django.utils.simplejson import dumps, loads, JSONEncoder
from django.db.models.query import QuerySet
from django.utils.functional import curry
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from collection.models import *
from django.core.paginator import Paginator, InvalidPage, EmptyPage
import simplejson as json
import urllib
import urllib2
from libs.lib import *
from django.core.context_processors import request
import os
import Cookie
import base64
from cStringIO import StringIO 
import Image
from datetime import date
from operator import itemgetter


def page_tools(collection,page,devide=5	):
	#devide = 5 #한번에 나올 페이지수
	paginator = Paginator(collection,10)
	
	try:
		page_info = paginator.page(page)
	except (EmptyPage, InvalidPage):
		page_info = paginator.page(paginator.num_pages)
		
	
	number = page_info.number 
	if number%devide==0:
		last = (number/devide) * devide
	else:
		last = (number/devide +1) * devide
	
	paging = paginator.page_range[last-devide:last]
	
	if last-devide>0:
		prev = last-devide
	else:
		prev = None
		
	if last+1<paginator.num_pages:
		next =last+1
	else:
		next =None 
	
	tools ={'page_info':page_info,'paging':paging,'prev':prev,'next':next}
	
	return tools

		
def index(request):
	assemblyman = Assemblyman.objects.all()
	dicass = {}
	totalass =[]
	for point in assemblyman:
		check = Plenary_attendance.objects.filter(assemblyman = point).order_by('id')
		temp1=temp2=temp3=temp4=0
		for c,p in enumerate(check):
			#print c,p.attendance,p.date,p.count
			if p.attendance==u'출석':
				temp1+=1
			elif p.attendance==u'청가':
				temp2+=1
			elif p.attendance==u'출장':
				temp3+=1
			elif p.attendance==u'결석':
				temp4+=1
			#print point.name
		#if point.name==u'박근혜':
		#print point.name ,u'출석 : ',temp1,u'청가 : ',temp2,u'출장 : ',temp3,u'결석 : ',temp4
		dicass = {"ass":point,"temp1":temp1,"temp2":temp2,"temp3":temp3,"temp4":temp4}
		totalass.append(dicass)
		newlist = sorted(totalass, key=itemgetter('temp1')) 
		
	return render_to_response(
		'index.html',
		{
			'request': request,
			'totalass':newlist,
			'type':type
		}
	)
def oauth(request):

	return HttpResponse('aaaa')

def kooking_oauth(request):

	'''
	x-skpop-userId:pcmwooki
	Accept-Language:ko_KR
	Date:Fri Nov 16 20:52:25 KST 2012
	access_Token:a4e0c7d8-eb6b-48f1-9329-dfa8252c98d6
	Content-Type:application/x-www-form-urlencoded;charset=utf-8
	Accept:application/json
	appKey:**************************
	'''
	try:
		access_token = request.GET['access_token']
		url = 'https://apis.skplanetx.com/nate/mail?version=1'
		url2 = 'https://apis.skplanetx.com/users/me/profile?version=1'
		user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
		headers = {
			'x-skpop-userId':'pcmwooki',
			'Accept-Language':'ko_KR',
			'Date':'Fri Nov 16 21:54:58 KST 2012',
			'access_Token':access_token,
			'User-Agent' : user_agent,
			'Accept':'application/json',
			'appKey':'b580d34e-c518-3930-af35-9a9250b5f981'}      
		value = {
				"to":"kalook@inthe-company.com",
				"body": "지켜보고있다.",
				"subject" : "지켜보고있다",
				"bcc" : "",
				"email":"pcmwooki@nate.com",
				"cc:":"지켜보고있다."}
		data = urllib.urlencode(value)
		req = urllib2.Request(url, data, headers)
		response = urllib2.urlopen(req)
		print response

		return HttpResponseRedirect('/')
	except Exception as e:
		print e
		#return HttpResponseRedirect('/')
		#pass
		'''
			https://oneid.skplanetx.com/oauth/authorize?client_id=9e472184-e559-309d-a1f9-625b43f9080d
			&response_type=token&scope=nate&redirect_uri=http://test.inthe-movie.com:1234/kooking_oauth
		'''
		return render_to_response(
			'oauth.html',
			{
				'request': request
			}
		)

def ranking(request,type):
	assemblyman = Assemblyman.objects.all()
	bill_result = Bill_result.objects.all()
	dic = {}
	total_temp = []
	for ass in assemblyman:
		a = Bill_result.objects.filter(assemblyman = ass)
		temp_list = []
		for n,list in enumerate(a):
			temp_list.append(list.result)
		dic = {
			'ass':ass,
			'agree':temp_list.count(u'찬성'),
			'opposite':temp_list.count(u'반대'),
			'abstention':temp_list.count(u'기권'),
			'not_vote':temp_list.count(u'불참'),
			'leave':temp_list.count(u'청가'),
			'absence':temp_list.count(u'결석')
			}
		total_temp.append(dic)
		#sorted(dic.iteritems(), key=itemgetter(1), reverse=True)
		#불참 랭킹
		#newlist = sorted(total_temp, key=itemgetter('not_vote'), reverse=True) 
		#기권랭킹
		newlist = sorted(total_temp, key=itemgetter(type), reverse=True) 
	return render_to_response(
		'index.html',
		{
			'request': request,
			'totalass':newlist,
			'type':type
		}
	)

def plenary(request):
	assemblyman = Assemblyman.objects.all()
	dicass = {}
	totalass =[]
	for point in assemblyman:
		check = Plenary_attendance.objects.filter(assemblyman = point).order_by('id')
		temp1=temp2=temp3=temp4=0
		for c,p in enumerate(check):
			if p.attendance==u'출석':
				temp1+=1
			elif p.attendance==u'청가':
				temp2+=1
			elif p.attendance==u'출장':
				temp3+=1
			elif p.attendance==u'결석':
				temp4+=1
		json_obj = json.dumps( {'name': point.name})
		serialized_obj = serialize('json', [ point, ])
		#print serialized_obj
		dicass = {"ass":json.loads(serialized_obj)[0].get('fields'),"temp1":temp1,"temp2":temp2,"temp3":temp3,"temp4":temp4}
		totalass.append(dicass)
		newlist = sorted(totalass, key=itemgetter('temp1'))
	out = json.dumps(newlist)
	# for p in json.loads(out):
	# 	print p.get('ass').get('phone')
	#plenary = json.JSONEncoder().encode(newlist)
	return HttpResponse(out,content_type='application/json; charset=UTF-8')

def abstention(request):
	return HttpResponse('abstention')

def nonattendance(request):
	return HttpResponse('nonattendance')

