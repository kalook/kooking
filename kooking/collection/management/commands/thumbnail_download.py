# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
import simplejson
import urllib
import csv
from datetime import datetime
from collection.models import *
from django.db.models import Q
from fpage.collection.models import *
from cStringIO import StringIO 
import Image
class Command(BaseCommand):
	
	LANG = "utf-8"
	def handle(self,*args,**options):
		
		url ='https://graph.facebook.com/'
		
		collection_list = Collection.objects.all().order_by('-id')
		for collection in collection_list:
			try:
				if collection.page_id :
					result = simplejson.load(urllib.urlopen(url+collection.page_id))
					picture = urllib.urlopen(url+collection.page_id+'/picture?type=large').geturl()
				else:
					result = simplejson.load(urllib.urlopen(url+collection.page_name))
					picture = urllib.urlopen(url+collection.page_name+'/picture?type=large').geturl()
				collection.page_title	= result.get("name")
				collection.picture		= picture
				collection.like 		= result.get("likes")
				collection.talker 		= result.get("talking_about_count")
				if not result.get("about"):
					collection.description 	= result.get("description")
				else:
					collection.description 	= result.get("about")
				collection.save()

				paths = "/data/fpage/files/thumbnail/"
				thumnail = collection.picture
				if thumnail:
					img_data = urllib.urlopen(thumnail) 
					img_io = StringIO(img_data.read()) 
					im = Image.open(img_io) 
					#im.thumbnail((100, 100), Image.ANTIALIAS) 
					im.save(paths+collection.page_id+".jpg")			
					#thumnail = "/images/thumbnail/"+datetime.now().strftime('%Y-%m-%d')+"_"+title_url+".jpg"

				print collection.id
				print result.get("name"),':',result.get("likes")
				print collection.page_title,u'업데이트 완료'

			except Exception,e:
				
				print collection.page_title,u'업데이트 실패'
				print e


