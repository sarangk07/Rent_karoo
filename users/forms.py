from typing import Any
from django import forms
import re

from .models import Registerinfo,Profile

class RegisterForm(forms.ModelForm):
    #password & conform password field ,it don't need to add in the database 
    password = forms.CharField(widget=(forms.PasswordInput(attrs={'placeholder':'password','class':'form-control'})))
    conf_password = forms.CharField(widget=(forms.PasswordInput(attrs={'placeholder':'re-type','class':'form-control'})))
    
    
    
    class Meta:
        model = Registerinfo #eath model ann use chyyendath 
        fields = "__all__" #models le ellaaa values um use chyyan
        
        # fields =['first_name','last_name','email','mobile']
      
      
      
    #for styling input fields
    def __init__(self,*args,**kwargs):
        super(RegisterForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

     
    #password and conf_password validation 
    def clean(self):
        cleaned_data = super(RegisterForm, self).clean() #super means it accessing the password and conf_password from the RegisterForm.
        password = cleaned_data.get('password')
        conf_password = cleaned_data.get('conf_password')
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        
        
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', password):
            print(password,conf_password)
            raise forms.ValidationError(
                "Password must contain at least one letter, one digit, and be at least 8 characters long."
                )       
        if not re.match(r'^[A-Za-z][A-Za-z\s]*$', first_name):
            raise forms.ValidationError("First name must only contain characters and no spaces.")

        if not re.match(r'^[A-Za-z][A-Za-z\s]*$', last_name):
            raise forms.ValidationError("Last name must only contain characters and no spaces.")
        
        print(password, conf_password)
        if password != conf_password:
            raise forms.ValidationError(
                "Password does not match"
            )
            
        return cleaned_data



class ProfileUpdate(forms.ModelForm):

    class Meta:
        model = Profile  
        fields = "__all__" 
        
        
    def __init__(self,*args,**kwargs):
        super(ProfileUpdate,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

        
    def save(self, commit: bool = ...) -> Any:
        return super().save(commit)
        
        
            
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# from django import forms
# from .models import Registerinfo

# class RegisterForm(forms.ModelForm):
#     password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password', 'class': 'form-control'}))
#     password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 're-type', 'class': 'form-control'}))

#     class Meta:
#         model = Registerinfo
#         fields = "__all__"

#     def clean_password2(self):
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")

#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError("Passwords do not match")

#         return password2

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         if commit:
#             user.save()
#         return user

#     def __init__(self, *args, **kwargs):
#         super(RegisterForm, self).__init__(*args, **kwargs)
#         for field in self.fields:
#             self.fields[field].widget.attrs['class'] = 'form-control'

