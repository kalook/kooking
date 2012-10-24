#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.http import HttpResponse
from collection.models import *
from admin.models import *
from collection.views import *

import simplejson
import urllib
from libs.lib import *
from django.core.context_processors import request
import os, os.path, sys
import Cookie
import base64
from datetime import datetime,date
def adminpage(request,page=1):

	collection =""
	#request.session["user"] = "Administrator"
	print request.method
	if request.method=="POST":
		if request.POST['password'] == "rbehtkfkdskfktkfkd":
			request.session["user"] = "Administrator"
			return HttpResponseRedirect("/admin/")
		else:
			return HttpResponseRedirect("/")
	else:
		if request.session.get("Administrator",True) :
			collection = Collection.objects.order_by('-id')
			tools = page_tools(collection,page)	

	return render_to_response(
		'admin.html',
		{
			'request': request,
			'collection' : tools['page_info'],
			'paging': tools['paging'],
			'next' : tools['next'],
			'prev' : tools['prev'],
			'page_number' : page
		}
	)

def event_management(request):
	
	
	total = Events.objects.all().order_by('-id')
	t_list = []

	result =[]
	for p in total:
		t_list.append(p.event_type)
	event_types = list(set(t_list))
	
	for event_name in event_types:
		total_num = Events.objects.filter(event_type = event_name).count()
		result.append({'type':event_name,'total':total_num})

	#event = Events.objects.filter(event_type=type).order_by('-id')

	return render_to_response(
		'event_management.html',
		{
			'request': request,
			'event' : total,
			'result':result
		}
	)

def event_download(request,type):
	view_info = Events.objects.filter(event_type=type).order_by('id')

	import csv
	response = HttpResponse(mimetype='text/csv')
	response['Content-type'] = 'charset=euc-kr'
	response['Content-Disposition'] = 'attachment; filename=event_request_'+type+'.csv'
	writer = csv.writer(response)
	writer.writerow(['name','email', 'date', 'ip'])
	for request in view_info:
		writer.writerow([request.name.encode('euc-kr'),request.email.encode('euc-kr'),request.date,request.ip.encode('euc-kr') ])			

	return response

def counselling(request,page=1):
	counselling = Counselling.objects.order_by('-id')
	tools = page_tools(counselling,page)
	return render_to_response(
		'counselling.html',
		{
			'request':request,
			'counselling' : tools['page_info'],
			'paging': tools['paging'],
			'next' : tools['next'],
			'prev' : tools['prev'],
			'page_number' : page
		}
	)

def counselling_view(request,id=4):
	counselling = Counselling.objects.get(id=id)
	return render_to_response(
		'counselling_view.html',
		{
			'request':request,
			'counselling':counselling
		}
	)

def counselling_delete(request,id):
	Counselling.objects.get(id=id).delete()
	return HttpResponseRedirect('/admin/counselling/1/')


def eventmanagement_create(request):
	category = Category.objects.all().order_by('-id')
	if request.method=="POST":
		try:
			ip = request.META['HTTP_X_REAL_IP']
		except:
			ip = request.META['REMOTE_ADDR']
		if request.POST['link_url']:
			link = request.POST['link_url']
		else:
			link = request.POST['link']
		try:
			banner = handle_uploaded_file('events',request.FILES['banner'])
		except:
			banner = ''
		try:
			start_date = request.POST['start_date'].split("/")
			start_date = date(int(start_date[2]), int(start_date[0]), int(start_date[1]))
			end_date = request.POST['end_date'].split("/")
			end_date = date(int(end_date[2]), int(end_date[0]), int(end_date[1]))
		except:
			start_date = request.POST['start_date'].split("-")
			start_date = date(int(start_date[0]), int(start_date[1]), int(start_date[2]))
			end_date = request.POST['end_date'].split("-")
			end_date = date(int(end_date[0]), int(end_date[1]), int(end_date[2]))
		
		EventManagement.objects.create(
			event_type 	= request.POST['type'],
			category 	= request.POST['category'],
			sponsorship = request.POST['sponsorship'],
			title		= request.POST['title'],
			banner      = banner,
		    start_date  = start_date,
		    end_date    = end_date,
		    person     	= request.POST['person'],
		    publish     = request.POST['publish'],
		    link        = request.POST['link_url'],
		    link_type   = request.POST['link_type'],
			ip = ip
			)
		
		return HttpResponseRedirect('/admin/events/1/')

	return render_to_response(
		'event_create.html',
		{
			'request':request,
			'category':category
		}
	)

def eventmanagement_list(request,id=1):
	try:
		if not request.session['user']=="Administrator":
			return HttpResponseRedirect('/')
	except:
		return HttpResponseRedirect('/')
		
	events = EventManagement.objects.all().order_by('-id')
	tools = page_tools(events,id)

	return render_to_response(
		'eventmanagement.html',
		{
			'request':request,
			'events':events,
			'counselling' : tools['page_info'],
			'paging': tools['paging'],
			'next' : tools['next'],
			'prev' : tools['prev'],
			'page_number' : id
		}
	)

def eventmanagement_view(request,id):
	event = EventManagement.objects.get(id=id)
	if event.link_type=="fpage":
		fpage_type = event.link.split('/')[4]
		applicants = Events.objects.filter(event_type = fpage_type).count()
	else:
		fpage_type = ''
		applicants = ''
	return render_to_response(
		'event_view.html',
		{
			'request':request,
			'event': event,
			'applicants': applicants,
			'fpage_type': fpage_type
		}
	)

def eventmanagement_modify(request,id):
	category = Category.objects.all().order_by('-id')
	event = EventManagement.objects.get(id=id)
	if request.method=="POST":
		try :
			banner = handle_uploaded_file('events',request.FILES['banner'])
			event.banner = banner
		except:
			pass
		try:
			start_date = request.POST['start_date'].split("/")
			start_date = date(int(start_date[2]), int(start_date[0]), int(start_date[1]))
			end_date = request.POST['end_date'].split("/")
			end_date = date(int(end_date[2]), int(end_date[0]), int(end_date[1]))
		except:
			start_date = request.POST['start_date'].split("-")
			start_date = date(int(start_date[0]), int(start_date[1]), int(start_date[2]))
			end_date = request.POST['end_date'].split("-")
			end_date = date(int(end_date[0]), int(end_date[1]), int(end_date[2]))
		event.event_type 	= request.POST['type']
		event.category 		= request.POST['category']
		event.sponsorship 	= request.POST['sponsorship']
		event.title 		= request.POST['title']
		event.start_date 	= start_date
		event.end_date 		= end_date
		event.person 		= request.POST['person']
		event.publish 		= request.POST['publish']
		event.link 			= request.POST['link_url']
		event.link_type 	= request.POST['link_type'] 
		event.save()
		return HttpResponseRedirect('/admin/events/view/'+id)
	return render_to_response(
		'event_modify.html',
		{
			'request': request,
			'category': category,
			'event': event
		}
	)

def handle_uploaded_file(paths,f):
	upload_path = settings.STORAGE_PATH+'/'+paths
	
	gen_name = GenPasswd()
	tmp_filename = (f.name).split('.')
	file_ext = tmp_filename[1]
	gen_file_name = datetime.now().strftime('%Y_%m_%d') + '_' + (gen_name) + '.' + file_ext
	if not os.path.exists(upload_path):
		os.makedirs(upload_path)    
	#gen_file_name = datetime.now().strftime('%Y_%m_%d') + '_' + (f.name)
	destination_path = upload_path+'/%s' % gen_file_name
	destination = open(destination_path, 'wb+')

	for chunk in f.chunks():
		destination.write(chunk)
	destination.close()
	return gen_file_name