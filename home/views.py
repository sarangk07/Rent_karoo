from django.shortcuts import render,get_object_or_404
from home.models import Cars
from django.http import HttpRequest ,HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    cars = Cars.objects.filter(is_available=True)
    print(cars)
    context = {
        'cars' : cars
        }  
    return render(request,'index.html',context)

def cars(request):
    cars = Cars.objects.filter(is_available=True)
    print(cars)
    context = {
        'cars' : cars
        }
    return render(request,'garage/cars.html',context)

def carDetails(request,id):
    print(id)   
    cars = Cars.objects.get(id=id)
   
    context = {
        'cars' : cars
        }
    return render(request,'garage/carDetails.html',context)


def pickupDetails(request,id):
    cars = Cars.objects.get(id=id)
   
    context = {
        'cars' : cars
        }
    return render(request,'garage/pickupDetails.html',context)