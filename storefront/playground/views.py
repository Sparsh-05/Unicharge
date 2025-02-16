from django.shortcuts import render , HttpResponse
from .models import charger_collection
from django.conf import settings

API_key = 'AIzaSyD2DGqXXJX1uzTkbNVSvjUhiWTELUj-N2U'

def say_hello(request):
    context = {
        "variable1" : "this is sent"
    }
    return render(request, 'home.html',context)

# Create your views here.
def about(request):
    return HttpResponse("This is about page")

def home(request):
    # Pass the Google Maps API key to the template
    context = {
        'google_maps_api_key':  settings.maps_api,
        'city_lat' : 28.7041,
        'city_long' : 77.1025,
        'city' : "your city"
    }
    return render(request, 'base.html', context)

def delhi(request):
    # Pass the Google Maps API key to the template
    context = {
        'google_maps_api_key': settings.maps_api,
        'city_lat' : 28.7041,
        'city_long' : 77.1025,
        'city' : "Delhi"
    }
    return render(request, 'home.html', context)

def mumbai(request):
    # Pass the Google Maps API key to the template
    context = {
        'google_maps_api_key': settings.maps_api,
        'city_lat' : 19.0760,
        'city_long' : 72.8777,
        'city' : "Mumbai"
    }
    return render(request, 'home.html', context)

def bangalore(request):
    # Pass the Google Maps API key to the template
    context = {
        'google_maps_api_key': settings.maps_api,
        'city_lat' : 12.9716,
        'city_long' : 77.5946,
        'city' : "Bangalore"
    }
    return render(request, 'home.html', context)

def showchargers(request):
    
    chargers = charger_collection.find({},{"_id":0,"latitude":1,"longitude":1})
    chargers_list = list(chargers)

    context = {
        'google_maps_api_key': settings.maps_api,
        'city_lat' : 28.7041,
        'city_long' : 77.1025,
        'city' : "Delhi",
        "chargers": chargers_list
    }
    return render (request,'home.html',context)

def homenew(request):
    chargers = charger_collection.find({},{"_id":0,"latitude":1,"longitude":1})
    chargers_list = list(chargers)

    context = {
        'google_maps_api_key': settings.maps_api,
        'city_lat' : 28.7041,
        'city_long' : 77.1025,
        'city' : "your city",
        "chargers": chargers_list
    }
    return render (request,'home.html',context)