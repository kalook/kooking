# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
import simplejson
import urllib
import csv
from django.http import HttpResponse
class Command(BaseCommand):
	
	LANG = "utf-8"
	def handle(self,*args,**options):
		
		url ='https://graph.facebook.com/'
		f = open("id.csv")
		r = csv.DictReader(f)
		total_list = []
		with open('test.csv', 'wb') as test_file:
			file_writer = csv.writer(test_file)
			file_writer.writerow(['ID'])
			for ids in r :
				result = simplejson.load(urllib.urlopen(url+ids['toychair']))
				if not result.get("id") is None:
					print result.get("id")
					#total_list.append(result.get("id"))
					file_writer.writerow([result.get("id").encode('euc-kr')])
			print "========================================"
			print "end collect"
			file_writer.close()
		
		'''
		with open('test.csv', 'wb') as test_file:
			file_writer = csv.writer(test_file)
			for idd in total_list:
				try:
					file_writer.writerow([idd])
				except:
					pass
		'''