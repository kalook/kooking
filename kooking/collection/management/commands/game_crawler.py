# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
import simplejson
import urllib
import csv
from collection.models import *
from django.db.models import Q
from fpage.collection.models import *
from BeautifulSoup import *
class Command(BaseCommand):
	
	LANG = "utf-8"
	def handle(self,*args,**options):
		
		url ='https://graph.facebook.com/'
		
		f = open("g.csv")
		r = csv.DictReader(f,['ID'])
		for urls in r:
			#print urls['ID']
			url ='http://graph.facebook.com/'+urls['ID']
			result = simplejson.load(urllib.urlopen(url+'/friends?access_token=0f84d5b754e16caeaacf5cb11eecbc6c'))
			print result
		#page_name = "{url}".format(**urls).split("https://www.facebook.com/")[1]
		'''
		url ='http://www.facebook.com/search/results.php?q=Coco%20Girl'
		ids = 'Coco Girl'
		handle = urllib.urlopen(url)
		data = handle.read()
		soup = BeautifulSoup(data,fromEncoding="euc-kr")
		print soup
		'''
		'''
		collection_list = Collection.objects.all().order_by('id')
		for collection in collection_list:
			try:
				if collection.page_id :
					result = simplejson.load(urllib.urlopen(url+collection.page_id))
				else:
					result = simplejson.load(urllib.urlopen(url+collection.page_name))
				collection.page_title	= result.get("name")
				collection.picture		= result.get("picture")
				collection.like 		= result.get("likes")
				collection.talker 		= result.get("talking_about_count")
				if not result.get("about"):
					collection.description 	= result.get("description")
				else:
					collection.description 	= result.get("about")
				collection.save()
				print collection.id
				print result.get("name"),':',result.get("likes")
				print collection.page_title,u'업데이트 완료'
			except Exception,e:
				print collection.page_title,u'업데이트 실패'
				print e
		'''

