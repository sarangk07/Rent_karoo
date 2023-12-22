from django.contrib import admin
from .models import Cars,PickupData,Payment,Wishlist,Stock
# Register your models here.


class CarAdmin(admin.ModelAdmin):
    list_display=('make', 'model', 'milage', 'transmission', 'fuel', 'added_date', 'is_available', 'in_garage',)
    
class PickupDataAdmin(admin.ModelAdmin):
    list_display=('bookedDate', 'mobile_number', 'car', 'user','licence_ID', 'pickup_date', 'dropoff_date', 'pay')

class PaymentDataAdmin(admin.ModelAdmin):
    list_display=('razorpay_order_id', 'is_paid', 'user')
    
class WishlistDataAdmin(admin.ModelAdmin):
    list_display=('wish_user',)
    
class StockDataAdmin(admin.ModelAdmin):
    list_display=('variant','quantity')
    

    
    
admin.site.register(Cars,CarAdmin)
admin.site.register(PickupData, PickupDataAdmin)
admin.site.register(Payment, PaymentDataAdmin)
admin.site.register(Wishlist, WishlistDataAdmin)
admin.site.register(Stock, StockDataAdmin)