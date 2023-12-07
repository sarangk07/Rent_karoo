from django import forms
from .models import Registerinfo

class RegisterForm(forms.ModelForm):
    #password um conform password um create akkunnu . for checking, it don't need to add in the database 
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
        print(password, conf_password)
        if password != conf_password:
            raise forms.ValidationError(
                "Password does not match"
            )

          
        
            
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
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

