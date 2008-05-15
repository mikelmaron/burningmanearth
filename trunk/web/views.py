import math
from datetime import datetime
from django.shortcuts import get_object_or_404, render_to_response
from django.core.paginator import ObjectPaginator, InvalidPage
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.gis.geos import *
from bme.web.models import *

def index(request):
	years = year.objects.all().order_by('-year')
	return render_to_response('index.tmpl', {'years': years})

def art_installations(request, year_year):
	xyear = year.objects.filter(year=year_year)
	previous = int(year_year) -1
	next = int(year_year) + 1
	art_installations = art_installation.objects.filter(year=xyear[0])
	return render_to_response('art_installations.tmpl', {'year': xyear[0],
							'art_installations': art_installations,
							'previous' : previous,
							'next' : next,})
	
def themecamps(request, year_year):
	xyear = year.objects.filter(year=year_year)
	previous = int(year_year) -1
	next = int(year_year) + 1
	theme_camps = theme_camp.objects.filter(year=xyear[0])
	return render_to_response('themecamps.tmpl', {'year': xyear[0],
							'theme_camps': theme_camps,
							'previous' : previous,
							'next' : next,})
	

def year_info(request, year_year):
	xyear = year.objects.filter(year=year_year)
	streets = circular_street.objects.filter(year=xyear[0])
	previous = int(year_year) -1
	next = int(year_year) + 1
	return render_to_response('year.tmpl', {'year': xyear[0],
						'streets' : streets,
						'previous' : previous,
						'next' : next,})

def art_installation_id(request, year_year, art_installation_id):
	xyear = year.objects.filter(year=year_year)
	xart_installation = art_installation.objects.get(id=art_installation_id)
	return render_to_response('art_installation.tmpl', {'year': xyear[0],
							'art_installation': xart_installation,})

def art_installation_name(request, year_year, art_installation_name):
	xyear = year.objects.filter(year=year_year)
	xart_installation = art_installation.objects.filter(year=xyear[0],slug=art_installation_name)
	return render_to_response('art_installation.tmpl', {'year': xyear[0],
							'art_installation': xart_installation[0],})

def themecampid(request, year_year, theme_camp_id):
	xyear = year.objects.filter(year=year_year)
	xtheme_camp = theme_camp.objects.get(id=theme_camp_id)
	return render_to_response('themecamp.tmpl', {'year': xyear[0],
							'theme_camp': xtheme_camp,})

def themecampname(request, year_year, theme_camp_name):
	xyear = year.objects.filter(year=year_year)
	theme_camp_name = theme_camp_name.replace('-',' ')
	xtheme_camp = theme_camp.objects.filter(year=xyear[0],name__iexact=theme_camp_name)
	return render_to_response('themecamp.tmpl', {'year': xyear[0],
							'theme_camp': xtheme_camp[0],})

def geocode(year_year, hour, minute, street):
	hour = int(hour)
	minute = int(minute)
	if minute == 0:
		minute = 58
		hour = hour -1
	else:
		minute = minute - 2 # Magnetic Declination??
	
	if(hour > 12):
		return HttpResponse("invalid time")
	elif(hour < 0):
		return HttpResponse("invalid time")
	if(minute > 59):
		return HttpResponse("invalid time")
	elif(minute < 0):
		return HttpResponse("invalid time")
	
	xyear = year.objects.filter(year=year_year)
	street = street.replace('-',' ')
	xstreet = circular_street.objects.filter(year=xyear[0],name__iexact=street)
	if xstreet.count() < 1:
		return HttpResponse("invalid street")

	radial = ((hour*30)+(minute*0.5))+60
	if radial >= 360:
		radial = radial - 360

	pnt = xyear[0].location_point
	
	pnt2 = getpoint(xyear[0].location_point.y, xyear[0].location_point.x,xstreet[0].distance_from_center,-radial)
	return pnt2	

def geocoder(request, year_year, hour, minute, street):
	pnt = geocode(year_year, hour, minute, street)
	return HttpResponse(pnt)

def neighborhood(request, year_year, hour, minute, street):
	pnt = geocode(year_year, hour, minute, street)
	xyear = year.objects.filter(year=year_year)
	previous = int(year_year) -1
	next = int(year_year) + 1
	time = hour + ":" + minute
	hour = int(hour)
	minute = int(minute)
	if minute == 0:
		minute = 58
		hour = hour -1
	else:
		minute = minute - 2 # Magnetic Declination??
	
	if(hour > 12):
		return HttpResponse("invalid time")
	elif(hour < 0):
		return HttpResponse("invalid time")
	if(minute > 59):
		return HttpResponse("invalid time")
	elif(minute < 0):
		return HttpResponse("invalid time")
	street = street.replace('-',' ')
	xstreet = circular_street.objects.filter(year=xyear[0],name__iexact=street)
	radial = ((hour*30)+(minute*0.5))+60
	if radial >= 360:
		radial = radial - 360
	return render_to_response('neighborhood.tmpl', {'year': xyear[0],
						'time': time,
						'previous' : previous,
						'next' : next,
						'street' : xstreet[0],
						'point' : pnt,
						'radial': -radial})

def getpoint(lat1,lon1,dist,dir):
        lat1 = (math.pi/180)*lat1
        lon1 = (math.pi/180)*lon1
        dir = (math.pi/180)*dir
        dist = dist / (185200.0/30.48)
        dist = dist / (180*60/math.pi)

        lat=math.asin(math.sin(lat1)*math.cos(dist)+math.cos(lat1)*math.sin(dist)*math.cos(dir))
        dlon=math.atan2(math.sin(dir)*math.sin(dist)*math.cos(lat1),math.cos(dist)-math.sin(lat1)*math.sin(lat))
        lon = ((lon1 - dlon+math.pi) % (2*math.pi)) - math.pi

        lat = lat * (180/math.pi)
        lon = lon * (180/math.pi)
        pnt = Point(float(lon), float(lat))

        return pnt
