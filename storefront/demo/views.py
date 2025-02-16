from django.shortcuts import render,HttpResponse
from .models import person_collection

# Create your views here.

def index(request):
    return HttpResponse({
        "<h1>This app is running<h1>"
    })

def add_person(request):
    records = {
        "first_name" : "John",
        "last_name" : "smith"
    }
    person_collection.insert_one(records)
    return HttpResponse("new record added")