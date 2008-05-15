from django.contrib.gis.db import models
from django.db import connection
from django.contrib.auth.models import User
import datetime

class year(models.Model):
	def __str__(self):
		return self.year
	year = models.CharField(max_length=4)
	location = models.CharField(max_length=50)
	location_point = models.PointField(null=True, blank=True)
	participants = models.IntegerField(null=True, blank=True)
	theme = models.CharField(max_length=20, null=True, blank=True)
	notes = models.TextField(null=True, blank=True)
	class Admin: pass
        class Meta:
                ordering = ('-year',)

class circular_street(models.Model):
	def __str__(self):
		return self.year.year + " " + self.name
	year = models.ForeignKey(year)
	name = models.CharField(max_length=50)
	order = models.IntegerField(null=True, blank=True)
	width = models.IntegerField(null=True, blank=True)
	distance_from_center = models.IntegerField(null=True, blank=True)
	class Admin:
		list_filter = ['year']
        class Meta:
                ordering = ('order',)
		

class theme_camp(models.Model):
	def __unicode__(self):
		return self.year.year + " " + self.name
	name = models.CharField(max_length=100)
	year = models.ForeignKey(year)
	description = models.TextField(null=True,blank=True)
	url = models.URLField(null=True,blank=True)
	contact_email = models.EmailField(null=True,blank=True)
	hometown = models.CharField(max_length=50, null=True, blank=True)
	location_point = models.PointField(null=True, blank=True)
	location_poly = models.PolygonField(null=True, blank=True)
	circular_street = models.ForeignKey(circular_street, null=True, blank=True)
	time_address = models.TimeField(null=True, blank=True)
	participants = models.ManyToManyField(User, null=True, blank=True)	
	class Admin:
		list_display = ('name', 'hometown', 'circular_street', 'time_address')
		list_filter = ['year', 'circular_street', 'time_address']
		ordering = ('name',)
		search_fields = ('name',)
        class Meta:
                ordering = ('name',)

class art_installation(models.Model):
	def __unicode__(self):
		return self.year.year + " " + self.name
	year = models.ForeignKey(year)
	name = models.CharField(max_length=255)
	slug = models.SlugField(max_length=255, prepopulate_from=("name",))
	artist = models.CharField(max_length=255, null=True, blank=True)
	description = models.TextField(null=True, blank=True)
	url = models.URLField(null=True, blank=True)
	contact_email = models.EmailField(null=True, blank=True)
	circular_street = models.ForeignKey(circular_street, null=True, blank=True)
	time_address = models.TimeField(null=True, blank=True)
	location_point = models.PointField(null=True, blank=True)
	location_poly = models.PolygonField(null=True, blank=True)
	class Admin:
		list_filter = ['year']
        class Meta:
                ordering = ('name',)

class playa_event(models.Model):
	EVENT_TYPE_CHOICES = (
		('NONE', 'None'),
		('AA', 'AA Meeting'),
		('CLASS', 'Class/Workshop'),
		('BURN', 'Burning'),
		('PARADE', 'Parade'),
		('KIDS', 'Kids Event'),
		('DAILY', 'Daily Event'),
		('MUSIC', 'Music Event'),
		('PERF', 'Performance Event'))
	def __str__(self):
		return self.name
	year = models.ForeignKey(year)
	name = models.CharField(max_length=100)
	description = models.TextField(null=True, blank=True)
	type = models.CharField(max_length=6, choices=EVENT_TYPE_CHOICES)
	start_date_time = models.DateTimeField(null=True, blank=True)
	end_date_time = models.DateTimeField(null=True, blank=True)
	duration = models.IntegerField(null=True, blank=True)
	repeats = models.BooleanField(null=True, blank=True)
	hosted_by_camp = models.ForeignKey(theme_camp, null=True, blank=True)
	located_at_art = models.ForeignKey(art_installation, null=True, blank=True)
	location_point = models.PointField(null=True, blank=True)
	location_track = models.LineStringField(null=True, blank=True)
	url = models.URLField(null=True, blank=True)
	contact_email = models.EmailField(null=True, blank=True)
	class Admin:
		list_display = ('name', 'year', 'type', 'start_date_time', 'end_date_time')
		list_filter = ['year', 'type']
		ordering = ('name','start_date_time')
		search_fields = ('name','description')
