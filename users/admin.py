from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Registerinfo,Profile

# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ('first_name','last_name','email','username','date_joined','last_login','is_active')
    
    filter_horizontal = ()
    
    list_filter = ()
    
    fieldsets = ()



admin.site.register(Registerinfo,AccountAdmin)
admin.site.register(Profile)

