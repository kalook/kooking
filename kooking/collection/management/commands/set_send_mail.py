# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from datetime import datetime
from xml.dom import minidom
from collection.models import *
import time
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.db.models import Q
import urllib
from django.http import HttpResponse
class Command(BaseCommand):
	# 언어환경
	LANG = "utf-8"

	args = '<poll_id poll_id ...>'
	help = 'Closes the specified poll for voting'
	
	def handle(self, *args, **options):	
		
		title = u'페이스북 정보 fpage 첫번째 인사드립니다'
		url = 'http://pcmwooki.inthe-movie.com/news/index.html'
		content = urllib.urlopen(url).read()
		#mail = 'pcmwooki@naver.com'
		
		
		filter_list =['xxing35@nate.com', 'hongmario@gmail.com', 'sachoi@oncompany.co.kr'] 
		email = Marketing.objects.filter(~Q(email__in = filter_list) , Q(email__contains = "@" ))
		
		for p in email :
			
			try:
				msg = EmailMultiAlternatives(title, content, 'kerze@inthe-company.com',[p.email])
				msg.attach_alternative(content, "text/html")
				msg.send()
				print "send mail : ",p.email 
			except Exception as e:
				print "not send mail : "
				print e

		