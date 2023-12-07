from django.contrib import admin
from .models import Cars
# Register your models here.


class CarAdmin(admin.ModelAdmin):
    list_display=('make', 'model', 'milage', 'transmission', 'fuel', 'added_date', 'is_available',)

    
    
admin.site.register(Cars,CarAdmin)