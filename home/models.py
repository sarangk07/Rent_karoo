from django.db import models

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
    
    
    make=models.CharField(max_length=50)
    model=models.CharField(max_length=50)
    milage=models.CharField(max_length=5)
    transmission=models.CharField(max_length=20,choices=TRANSMISSIONS)
    rentAmount=models.IntegerField(default=0)
    color=models.CharField(max_length=30)
    year=models.IntegerField()
    carImg=models.ImageField(upload_to='media/carimages')
    fuel=models.CharField(max_length=20,choices=FUEL_TYPE)
    is_available=models.BooleanField(default=True)
    description=models.CharField(max_length=80)
    added_date=models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        verbose_name = 'Cars'
        verbose_name_plural = 'cars'
    
    def __str__(self):
        return f"{self.model} {self.fuel}"
    
    
    
    
