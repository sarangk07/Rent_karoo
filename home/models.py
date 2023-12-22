from django.db import models
from users.models import Registerinfo

# Create your models here.

class Cars(models.Model):
    
    TRANSMISSIONS=[
        ('Automatic','Automatic'),
        ('Manual','Manual'),
    ]
    
    FUEL_TYPE=[
        ('Diesel','Diesel'),
        ('Petrol','Petrol'),
        ('Electric','Electric'),
    ]
    CAR_TYPE=[
        ('SUV','SUV'),
        ('MPV','MPV'),
        ('EV','EV'),
        ('Sedan','Sedan'),
        ('Hatchback','Hatchback'),
    ]
    
    make=models.CharField(max_length=50)
    model=models.CharField(max_length=50)
    milage=models.CharField(max_length=5)
    engine=models.CharField(max_length=20,default="")
    seatingCapacity=models.CharField(max_length=20,default="")
    carType=models.CharField(max_length=20,choices=CAR_TYPE,default="")
    carNumber=models.CharField(max_length=20,unique=True,default="")
    transmission=models.CharField(max_length=20,choices=TRANSMISSIONS)
    rentAmount=models.IntegerField(default=0)
    color=models.CharField(max_length=30)
    year=models.IntegerField()
    carImg=models.ImageField(upload_to='media/carimages')
    fuel=models.CharField(max_length=20,choices=FUEL_TYPE)
    rc_expired_date=models.CharField(max_length=20,default="")
    
    
    in_garage=models.BooleanField(default=True)
    is_available=models.BooleanField(default=True)
    description=models.TextField()
    added_date=models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        verbose_name = 'Cars'
        verbose_name_plural = 'cars'
    
    def __str__(self):
        return f"{self.model} {self.fuel}"


class Stock(models.Model):
    variant = models.ForeignKey(Cars, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.variant} - Stock: {self.quantity}"



    
class PickupData(models.Model):
    Pickup_time = models.TimeField()
    pickup_date = models.DateField()
    dropoff_date = models.DateField()
    mobile_number = models.BigIntegerField()
    licence_ID = models.CharField(max_length=50)
    car = models.ForeignKey(Cars, on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(Registerinfo, on_delete=models.CASCADE,null=True)
    pay = models.BooleanField(default=False)
    bookedDate = models.DateTimeField(auto_now_add=True,null=True)
    
    class Meta:
        verbose_name = 'PickupData'
        verbose_name_plural = 'Bookings Details'
    
    def __str__(self):
        return f"Pickup for {self.car.model} at {self.pickup_date}"
    
        
        
    
    
class Payment(models.Model):
    razorpay_order_id = models.CharField(max_length=500,null=True,blank=True)
    razorpay_payment_id = models.CharField(max_length=500,null=True,blank=True)
    razorpay_payment_signature = models.CharField(max_length=500,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    user = models.ForeignKey(Registerinfo, on_delete=models.CASCADE,null=True,blank=True)
    booking = models.ForeignKey(PickupData,on_delete=models.CASCADE,null=True,blank=True)
    
    is_paid = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Order id: {self.razorpay_order_id}"
    
    
    
class Wishlist(models.Model):
    wish_user = models.ForeignKey(Registerinfo, on_delete=models.CASCADE,null=True,blank=True)
    wish_car = models.ManyToManyField(Cars,blank=True,related_name='fav_cars')
    def __str__(self):
        return str(self.wish_user)
    
    
    
    
    
    
