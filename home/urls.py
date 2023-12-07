from django.urls import path,include
from . import views

urlpatterns=[
    path('', views.home,name='home'),
    path('cars/', views.cars,name='cars'),
    path('carDetails/<int:id>/', views.carDetails,name='carDetails'),
    path('pickupDetails/<int:id>/', views.pickupDetails,name='pickupDetails'),
    
]