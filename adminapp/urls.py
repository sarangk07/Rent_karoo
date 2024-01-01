from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.adminlogin, name="adminlogin"),
    path("adminlogout/", views.adminlogout, name="adminlogout"),
    path("admindasbord/", views.admindasbord, name="admindasbord"),
    path("userviewEdit/<str:id>/", views.userviewEdit, name="userviewEdit"),
    path("adminuser/", views.adminuser, name="adminuser"),
    path("adminprofile/", views.adminprofile, name="adminprofile"),
    path("adminblock/<str:id>/", views.adminblock, name="adminblock"),
    path("admincars/", views.admincars, name="admincars"),
    path("caradd/", views.carAdd, name="caradd"),
    path("cardelete/<int:id>/", views.carDelete, name="cardelete"),
    path("caredit/<int:id>/", views.carUpdate, name="caredit"),
    path("adminbooking/", views.adminbooking, name="adminbooking"),
    path("adminbook/<int:id>/", views.adminbook, name="adminbook"),
    path("paymentDetails/", views.paymentDetails, name="paymentDetails"),
    path("paymentDelete/<int:id>/", views.paymentDelete, name="paymentDelete"),
]
