from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cars/', views.cars, name='cars'),
    path('carDetails/<int:id>/', views.carDetails, name='carDetails'),
    path('pickupDetails/<int:id>/', views.pickupDetails, name='pickupDetails'),
    path('search/', views.search, name='search'),
    path('sorting/<str:car_type>/', views.sorting, name='sorting'),
    
    
    path('payment/<int:id>/', views.payment, name='payment'),
    path('success/', views.success, name='success'),
    

    path('add_to_wishlist/<int:car_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<int:car_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    
    path('termsandConditions/', views.termsandConditions, name='termsandConditions')
    
]
