
# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
import simplejson
import urllib
import csv
from collection.models import *
from django.db.models import Q
from fpage.collection.models import *
class Command(BaseCommand):
	
	LANG = "utf-8"
	def handle(self,*args,**options):
		name = []
		category =[]
		error=[]
		
		url ='https://graph.facebook.com/'
		
		f = open("goods1.csv")
		r = csv.DictReader(f,['url','category'])
		for urls in r:
			page_name = "{url}".format(**urls).split("https://www.facebook.com/")[1]
			if page_name[:6]=='pages/':
				page_name = page_name.split("/")
				page_name = page_name[2]
				'''
			   name.append(page_name)
			   category.append(urls['category'])
			   '''
			result = simplejson.load(urllib.urlopen(url+page_name))
			category = urls['category']
			print u"수집중 : ",result.get("id")
			try:
				try:
					temp = Category.objects.get(category = category)
					temp.save()
				except:
					temp = Category.objects.create(
								category = category
								)
				try:
					collection = Collection.objects.get(page_id=result.get("id"))
					collection.page_title	= result.get("name")
					collection.page_name	= page_name
					collection.picture 		= result.get("picture")
					collection.likes 		= result.get("likes")
					collection.talker 		= result.get("talking_about_count")
					if not result.get("about"):
						collection.description 	= result.get("description")
					else:
						collection.description 	= result.get("about")
					collection.category_id 	= temp
					collection.save()
					print u'업데이트 완료',collection.page_name
				except:
					collection = Collection.objects.create(
						page_id = result.get("id"),
						page_title = result.get("name"),
						page_name = page_name,
						picture  =   result.get("picture"),
						like = result.get("likes"),
						talker = result.get("talking_about_count"),
						description = result.get("description"),
						category_id = temp,
						view = 1
						)
					print u"수집완료 : ",collection.page_name
				

			except Exception,e:
				print e
				error.append(page_name)

		for list in error:
			print u"실패주소 : ",list

