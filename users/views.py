from django.shortcuts import render,redirect
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Registerinfo
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

#email verify
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage








# Create your views here.
csrf_exempt
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        print(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
  
            users = Registerinfo.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)   
            users.save()
            
            #email verify
            current_site = get_current_site(request)
            mail_subjet = 'plsactivate your account'
            message = render_to_string('user_temp/account_verification_email.html',{
                'user' : users,#to get the user in the template and to get the primary key
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(users.pk)),#encoding the primary key for safty
                'token':default_token_generator.make_token(users),#create a token  for the perticular user
                
            })
            #send email
            to_mail = email
            send_mail = EmailMessage(mail_subjet,message, to=[to_mail])#to = sending mail to the provided email
            send_mail.send()
            
            
            
            
            messages.success(request, 'Registration success')
            return redirect('register')
        
        print(form.errors)
    else:
        form = RegisterForm()  
        #  
        # return redirect('home')
    
    form = RegisterForm()
    
    context={'form':form}
    return render(request,'user_temp\signup.html',context)











def user_login(request):
    
    if request.method == 'POST':
        print("---------------------user---login----------------------------")
        print(request.POST)
        email = request.POST['email']
        password = request.POST['password']
        print(email, password)
        users = Registerinfo.objects.get(email=email)
        print(users)
        user = authenticate( email=email, password=password)

        # user = authenticate(request, email=email, password=password)
        print(user)
        print("------------------------------------------------------------") 

        
        if user is not None:
            login(request, user)
            
            return redirect('home')
        else:
            messages.warning(request, 'invalid email or password!')
           
            return redirect('login')
        
    return render(request, 'user_temp\login.html')







@login_required(login_url = 'login')
def user_logout(request):
    logout(request)
    messages.success(request,'logout successfully')
    return redirect('login') 









# @login_required(login_url='login')
def home(request):
    return render(request,'home.html')






def activate(request,uidb64,token):
    return HttpResponse('done')