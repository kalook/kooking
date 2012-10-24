
from django.db import models

class Category(models.Model):
    category = models.CharField(max_length=1024,null=True)
    category_eng = models.CharField(max_length=1024,null=True)
    def counting(self):
		
        return Collection.objects.filter(category_id = self.id).count()

class MarketingCenter(models.Model):
    company =   models.CharField(max_length=255,null=True)
    charge  =   models.CharField(max_length=255,null=True)
    phone   =   models.CharField(max_length=255,null=True)
    email   =   models.CharField(max_length=255,null=True)
    news    =   models.BooleanField(default='N')
    date    =   models.DateTimeField(auto_now_add=True)
    ip      =   models.CharField(max_length=15,null=True)

class Collection(models.Model):
    page_id     =   models.CharField(max_length=255,null=True)
    page_title  =   models.CharField(max_length=255,null=True)
    page_name   =   models.CharField(max_length=255,null=True)
    picture     =   models.CharField(max_length=255,null=True)
    like        =   models.IntegerField(default=0,null=True)
    talker      =   models.IntegerField(default=0,null=True)
    description =   models.TextField(null=True)   
    category_id =   models.ForeignKey(Category,null=True)
    marketing_id =   models.ForeignKey(MarketingCenter,null=True)
    view        =   models.BooleanField(default=0)
    date        =   models.DateTimeField(auto_now_add=True)
    ip          =   models.CharField(max_length=15,default='128.0.0.1')

class Marketing(models.Model):
    page_id =   models.ForeignKey(Collection,null=True)
    company =   models.CharField(max_length=255,null=True)
    charge  =   models.CharField(max_length=255,null=True)
    phone   =   models.CharField(max_length=255,null=True)
    email   =   models.CharField(max_length=255,null=True)
    news    =   models.BooleanField(default='N')
    date    =   models.DateTimeField(auto_now_add=True)
    ip      =   models.CharField(max_length=15)

class EventManagement(models.Model):
    event_type  =   models.CharField(max_length=255,null=True)
    category    =   models.CharField(max_length=255,null=True)
    sponsorship =   models.CharField(max_length=255,null=True)
    title       =   models.CharField(max_length=255,null=True)
    banner      =   models.CharField(max_length=255,null=True)
    start_date  =   models.DateField(null=True)
    end_date    =   models.DateField(null=True)
    publish     =   models.CharField(max_length=255,null=True)
    person      =   models.CharField(max_length=255,null=True)
    link        =   models.CharField(max_length=255,null=True)
    link_type   =   models.CharField(max_length=255,null=True)
    view        =   models.BooleanField(default=1)
    date        =   models.DateTimeField(auto_now_add=True)
    ip          =   models.CharField(max_length=15)

class Top10(models.Model):
    page_id = models.ForeignKey(Collection)
    count   = models.IntegerField(null =True,default=0)

class Event(models.Model):
    check_id    =   models.CharField(max_length=255,null=True)
    name        =   models.CharField(max_length=255,null=True)
    email       =   models.CharField(max_length=255,null=True)      
    date        =   models.DateTimeField(auto_now_add=True)
    ip          =   models.CharField(max_length=15)

class Events(models.Model):
    check_id    =   models.CharField(max_length=255,null=True)
    name        =   models.CharField(max_length=255,null=True)
    email       =   models.CharField(max_length=255,null=True) 
    event_type  =   models.CharField(max_length=255,null=True)      
    date        =   models.DateTimeField(auto_now_add=True)
    ip          =   models.CharField(max_length=15)

class Counselling(models.Model):
    company     =   models.CharField(max_length=255,null=True)
    person      =   models.CharField(max_length=255,null=True)
    phone       =   models.CharField(max_length=255,null=True)
    email       =   models.CharField(max_length=255,null=True)
    title       =   models.CharField(max_length=255,null=True)
    contents    =   models.TextField(null=True) 
    date        =   models.DateTimeField(auto_now_add=True)
    ip          =   models.CharField(max_length=15)
    