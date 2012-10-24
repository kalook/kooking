#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.http import HttpResponse
from collection.models import *
from django.core.paginator import Paginator, InvalidPage, EmptyPage
import simplejson
import urllib
from libs.lib import *
from django.core.context_processors import request
import os
import Cookie
import base64
from cStringIO import StringIO 
import Image
from datetime import date
def crawler(request):
	
	validation(request)
	package = []
	url ='https://graph.facebook.com/'
	
	page_name_input = page_name = request.POST['page_url'].split("www.facebook.com/")[1]
	 
	if page_name[:6]=='pages/':
		page_name = page_name.split("/")
		page_name = page_name[2]
	

	result = simplejson.load(urllib.urlopen(url+page_name))
	category = request.POST['category']
	
	try:
		
		#print result.get("name")
		
		temp_collection = Collection.objects.filter(page_id=result.get("id"))
		if temp_collection:
			package.append("already")
			package.append("error")
			return package
		
		
		#카테고리 정의 [신규 카테고리일 경우 새로 생성]
		try:
			temp = Category.objects.get(category = category)
			temp.save()
		except:
			temp = Category.objects.create(
					category = category
					)
				
		#페이스북 정보 가져오기
		if not result.get("about"):
			temp_text = result.get("description")
		else:
			temp_text = result.get("about")
		try:
			#세부항목 입력
			try:
				ip = request.META['REMOTE_ADDR']
			except:
				ip = request.META['HTTP_X_REAL_IP']
			picture = urllib.urlopen(url+result.get("id")+'/picture?type=large').geturl()	
			'''
			paths = "/data/fpage/files/thumbnail/"
			if picture:
				img_data = urllib.urlopen(picture) 
				img_io = StringIO(img_data.read()) 
				im = Image.open(img_io)
				im.save(paths+result.get("id")+".jpg")	
			'''

			marketingcenter = MarketingCenter.objects.create(
						company = request.POST['company'],
						charge = request.POST['charge'],
						phone = request.POST['phone'],
						email = request.POST['email'],
						ip = ip
						)
			collection = Collection.objects.create(
						page_id = result.get("id"),
						page_title = result.get("name"),
						page_name = page_name_input,
						picture  =   picture,
						like = result.get("likes"),
						talker = result.get("talking_about_count"),
						description = temp_text,
						category_id = temp,
						marketing_id = marketingcenter,
						view = 0,
						ip = ip
						)


		except Exception as e:
			print e
		package.append("success")
		return package
	
	
	except:
		package.append("sorry")
		package.append("error")
		return package


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

		
def index(request,type='recommand',page=1):
	collection =[]
	category_name = category_count =''
	
	if type=='search':
		#collection = Collection.objects.filter(page_title__contains=keyword)
		#검색 페이징 포함 알고리즘
		
		
		search = request.GET['search'].split('/') 
		type='search?search='+search[0]
		collection = Collection.objects.filter(page_title__contains=search[0],view=1)
		temp_page = search.pop()
		if isNumber(temp_page):
			page = temp_page
	else:
		if type=='recommand':
			recommand_list =[
							"1300Kstory",
							"monthlyjs",
							"echatelaine",
							"woohoostory",
							"imdb",
							"officialpsy",
							"bejeweledblitz",
							"9suk9suklive",
							"bulls9com",
							"superstark"]
			collection = Collection.objects.filter(page_name__in=recommand_list)
			category_name = u'전체'
			category_count = Collection.objects.all().count()
			#val = map(lambda recom:(lambda coll: (collection)))(recommand_list)
			'''
			i=1
			print [i for list in enumerate(recommand_list) ]
			for i, list in enumerate(recommand_list):
				print collection[i].page_name, '=='	, list 
			'''
			temp=[]
			for list in recommand_list:
				for p in collection:
					if list==p.page_name:
						temp.append(p)
			collection=temp

			
			
		elif type=='all':
			collection = Collection.objects.filter(view=True).order_by('-id')
			category_name = u'전체'
			category_count = Collection.objects.all().count()
		elif type=='liketop':
			collection = Collection.objects.filter(view=True).order_by('-like')
		elif type=='new':
			collection = Collection.objects.filter(view=True).order_by('-id')		
		else:
			collection = Collection.objects.filter(category_id=type,view=1).order_by('-id')
			category_name = Category.objects.get(id=type).category
			category_count =  Category.objects.get(id=type).counting()
		
	collectionCount = Collection.objects.all().count()
	category = Category.objects.order_by('id')
	tools = page_tools(collection,page)
	return render_to_response(
		'index.html',
		{
			'request': request,
			'type' : type,
			'category' : category,
			'page_number' : page,
			'collection' : tools['page_info'],
			'paging': tools['paging'],
			'next' : tools['next'],
			'prev' : tools['prev'],
			'category_count_all' : collectionCount,
			'category_name':category_name,
			'category_count':category_count
		}
	)

def pageinfo(request,type='all',page=1):
	if type=='all':
		collection = Collection.objects.filter(view=True).order_by('-id')
		category_name = u'전체'
		category_count = Collection.objects.all().count()
	else:
		collection = Collection.objects.filter(category_id=type,view=1).order_by('-id')
		category_name = Category.objects.get(id=type).category
		category_count =  Category.objects.get(id=type).counting()
	collectionCount = Collection.objects.all().count()
	category = Category.objects.order_by('id')
	tools = page_tools(collection,page)
	return render_to_response(
		'pageinfo.html',
		{
			'request': request,
			'type' : type,
			'category' : category,
			'page_number' : page,
			'collection' : tools['page_info'],
			'paging': tools['paging'],
			'next' : tools['next'],
			'prev' : tools['prev'],
			'category_count_all' : collectionCount,
			'category_name':category_name,
			'category_count':category_count
		}
	)


def info(request):
	category = Category.objects.order_by('id')
	collectionCount = Collection.objects.all().count()
	return render_to_response(
		 'info.html',
		 {
			 'request': request,
			 'category' : category,
			 'category_count_all' : collectionCount
	
		 }
	)
		
def event(request,event_name):
	category = Category.objects.order_by('id')
	collectionCount = Collection.objects.all().count()
	if event_name == 'darkknight':
		html = 'event.html'
	else:
		html = event_name+'.html'

	if request.method=="POST":
		try:
			if not event_name =='darkknight':
				event = Events.objects.get(check_id = request.POST['user_id'],event_type=event_name)
				if 'callback' in request.session:
					del request.session['callback']
				return HttpResponse("false")
			else:	
				event = Event.objects.get(check_id = request.POST['user_id'])
				return HttpResponse("false")
		except:
			if not event_name =='darkknight':
				try:
					events = Events.objects.create(
						check_id	= request.POST['user_id'],
						name 		= request.POST['name'],
						email 		= request.POST['email'],
						event_type 	= event_name,
						ip   		= request.META['HTTP_X_REAL_IP']
						)
				except:
					events = Events.objects.create(
						check_id	= request.POST['user_id'],
						name 		= request.POST['name'],
						email 		= request.POST['email'],
						event_type 	= event_name,
						ip   		= request.META['REMOTE_ADDR']
						)
			else:	
				events = Event.objects.create(
					check_id	= request.POST['user_id'],
					name 	= request.POST['name'],
					email 	= request.POST['email'],
					ip   	= request.META['HTTP_X_REAL_IP']
					)
			if 'callback' in request.session:
				del request.session['callback']
			return HttpResponse(events)
	else:
		#크롬에서 images를 부르는 버그?
		if not event_name=="images":
			request.session['event_name'] = event_name
		
		if 'callback' in request.session:
			callback = request.session['callback']
			del request.session['callback']
		else:
			callback=""
	return render_to_response(
		'/event/'+html,
		{
			'request': request,
			'event_name': event_name,
			'category' : category,
			'url': request.META['HTTP_HOST'],
			'callback' : callback,
			'category_count_all' : collectionCount
		}
	)

def event_oauth(request):


	event_name = request.session['event_name'] 
	request.session['callback'] = "True"
	return render_to_response(
		'/event/oauth.html',
		{
			'request': request,
			'event_name':event_name
		}
	)


def marketing(request):
	category = Category.objects.order_by('id')
	collectionCount = Collection.objects.all().count()
	if request.method=="POST" :
		
		result = crawler(request)
		'''
		if result.pop()=="success":
			print result.pop()
		else:
			print result.pop()
		'''
		return render_to_response(
			'marketing.html',
			{
				'request': request,
				'category' : category,
				'category_count_all' : collectionCount
			}
		)
	return render_to_response(
			'marketing.html',
			{
				'request': request,
				'category' : category,
				'category_count_all' : collectionCount
			}
		)

def goods(request):
	category = Category.objects.order_by('id')
	collectionCount = Collection.objects.all().count()
	if request.method == 'POST':
		try:
			try:
				ip = request.META['HTTP_X_REAL_IP']
			except:
				ip = request.META['REMOTE_ADDR']
			
			counselling = Counselling.objects.create(
				company = request.POST['company'],
				person = request.POST['person'],
				phone = request.POST['phone'],
				email = request.POST['email'],
				title = request.POST['title'],
				contents = request.POST['contents'],
				ip = ip
				)
			return HttpResponse(True)
		except Exception as e:
			print e
			return HttpResponse(False)
	
	return render_to_response(
			'marketinggoods.html',
			{
				'request': request,
				'category' : category,
				'category_count_all' : collectionCount
			}
		)

def validation(request):
	try:
		if request.POST['page_url'] and request.POST['category'] and request.POST['company'] and request.POST['charge'] and request.POST['email'] and request.POST['check']:
			return True
		else:
			return False
	except:
		return False
	
def validate(request):
	#print request.POST['data']
	try:
		if request.method == 'POST':
			url ='https://graph.facebook.com/'
			page_name = request.POST['url'].split("www.facebook.com/")[1]
			
			if page_name[:6]=='pages/':
				page_name = page_name.split("/")
				page_name = page_name[2]
		
			result = simplejson.load(urllib.urlopen(url+page_name))
			temp_collection = Collection.objects.filter(page_id=result.get("id"))
		
			if temp_collection:
				result = "false"
			elif result.get("id"):
				result = "success"
			else:
				result = "false"
		else:
			result = "false"
	except:
		result = "false"
		
	return HttpResponse(result, mimetype="text/html")

def status(request):
	try:
		#print request.POST['id']
		collection = Collection.objects.get(id= request.POST['id']) 
		if collection.view == True:
			collection.view = False
		else:
			collection.view = True
		collection.save()
		retult = 'success'
	except:
		result = 'false'
	return HttpResponse(retult, mimetype="text/html")

def logout(request):
	del request.session['user']
	return HttpResponseRedirect("/")


def detail(request,id='215082308577534'):
	url ='https://graph.facebook.com/'+id

	result = simplejson.load(urllib.urlopen(url))
	temp = Collection.objects.get(page_id=id)

	relation_category = Collection.objects.filter(category_id = temp.category_id).order_by('?')[:4]

	try:
		cover = result.get("cover").get("source")
	except:
		cover = ''
	
	return render_to_response(
		'detail.html',
		{
			'request': request,
			'app_id':  id,
			'code':result.get("username"),
			'link':result.get("like"),
			'category':temp.category_id.category,
			'about':result.get("about"),
			'company_overview':result.get('company_overview'),
			'name':result.get("name"),
			'picture':temp.picture,
			'description':result.get("description"),
			'pharma_safety_info':result.get("pharma_safety_info"),
			'cover':cover,
			'like':result.get("likes"),
			'talker': result.get("talking_about_count"),
			'category_id':relation_category[0].category_id.id,
			'relation_category' : relation_category
		}
	)

def image_proxy(request):
	url = base64.decodestring(request.GET['u'])
	contents = urllib.urlopen(url).read()
	return HttpResponse(contents, content_type='image/jpg')

def url_proxy(request):
	url = base64.decodestring(request.GET['u'])
	contents = urllib.urlopen(url).read()
	return HttpResponse(contents,content_type='text/html')

def script_proxy(request):
	url = request.GET['u']
	contents = urllib.urlopen(url).read()
	return HttpResponse(contents,content_type='text/javscript')



def popup(request):

	return render_to_response(
		'popup.html',
		{
			'request': request
		}
	)

#이벤트 페이지
def events(request,page_category="all",page=1):
	print date.today()
	if page_category =="all":
		events = EventManagement.objects.filter(view=1,end_date__gte=date.today()).order_by('-id')
	else:
		events = EventManagement.objects.filter(view=1,category=page_category,end_date__gte=date.today()).order_by('-id')
	category_dic=[]
	category_filter = EventManagement.objects.filter(view=1,end_date__gte=date.today()).values('category').annotate()

	category_dic.append({"category":"all","count":EventManagement.objects.filter(view=1).order_by('-id').count()})
	
	for category_temp in category_filter:
		counting = EventManagement.objects.filter(view=1,category=category_temp['category']).count()
		category_dic.append({"category":category_temp['category'],"count":counting})
	tools = page_tools(events,page)
	return render_to_response(
		'events.html',
		{
			'request': request,
			'category_dic': category_dic,
			'page_category': page_category,
			'page_number' : page,
			'events' : tools['page_info'],
			'paging': tools['paging'],
			'next' : tools['next'],
			'prev' : tools['prev']
		}
	)