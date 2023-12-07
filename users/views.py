from django.shortcuts import render,redirect
from .forms import RegisterForm
from .models import Registerinfo
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest ,HttpResponse

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage





# Create your views here.

#user register
@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)#request.POST-- it contains all the field values
        print(request.POST)
        print("-------------------------register--------------------------")
        if form.is_valid():
            first_name = form.cleaned_data['first_name'] #when we use the django form we need to use cleaned_data[]
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
  
            users = Registerinfo.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)   
            users.save() #the create_user form is from the models.py 
            
            #user activation 
            current_site = get_current_site(request) #get_current_site - function is used to obtain the current site for the request
            mail_subject = "please activate your account"     
            message = render_to_string('user_temp/account_verification_email.html',{ #function is used to render an HTML template (account_verification_email.html) as a string
               'user':users,        #pass the user to the html
               'domain': current_site,
               'uid': urlsafe_base64_encode(force_bytes(users.pk)), #user id
               'token':default_token_generator.make_token(users),
            })
            to_email = email
            sent_email = EmailMessage(mail_subject, message, to=[to_email])
            sent_email.send()  
        
            messages.success(request, 'Registration success. please activate your account .check your mail')
            return redirect('register')
        
        print(form.errors)
    else:
        form = RegisterForm()   
    context={'form':form}
    return render(request,'user_temp\signup.html',context)





#user login
def user_login(request):
    if request.method == 'POST':
        print("---------------------User-^-login----------------------------")
        print(request.POST)
        email = request.POST['email']
        password = request.POST['password']
        print(email, password)
        users = Registerinfo.objects.get(email=email)
        print(users)
        user = authenticate(request, email=email, password=password ) 
        #The purpose of authenticate is to check if the provided credentials are valid and correspond to an active user in the system
        print(user)
        print("------------------------------------------------------------") 
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.warning(request, 'invalid email or password!')
            return redirect('login')
        
    return render(request, 'user_temp/login.html')





#user logout
@login_required(login_url = 'login')
def user_logout(request):
    logout(request)
    messages.success(request,'logout successfully')
    return redirect('login') 



#user dashbord
@login_required(login_url='login')
def dashbord(request):
    return render(request,'user_temp/dashbord.html')



#user account activation
def activate(request,uidb64,token):
   try :
       uid = urlsafe_base64_decode(uidb64).decode()
       print(uid)
       user =  Registerinfo.objects.get (pk = uid)  
   except (TypeError,ValueError,OverflowError,Registerinfo.DoesNotExist):
       user = None
   if user is not None and default_token_generator.check_token(user,token):
       user.is_active = True
       user.save()
       messages.success(request,'congratulations your account  is activated') 
       return redirect('login')
   else:
       messages.error(request,'Invalid activation link') 
       return redirect('register')



#user forgotpassword
def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Registerinfo.objects.filter(email=email).exists():#.exists() --check the email in the Acccounts
            user = Registerinfo.objects.get(email=email)
            
            current_site = get_current_site(request)
            mail_subject = "reset password"    
            message = render_to_string('user_temp/reset_password_email.html',{
               'user':user,
               'domain': current_site,
               'uid': urlsafe_base64_encode(force_bytes(user.pk)), #user id
               'token':default_token_generator.make_token(user),
            })
            to_email = email
            sent_email = EmailMessage(mail_subject, message, to=[to_email])
            sent_email.send()
 
            messages.success(request, 'reset password email send success! check your mail')
            return redirect('login')    
        else:
            messages.error(request,'Account with this email not found!')    
            return redirect('forgotpassword')
    return render(request,'user_temp/forgotpassword.html')






#user resetPassword validation
def resetpassword_validate(request,uidb64,token):
    try :
        uid = urlsafe_base64_decode(uidb64).decode()
        user =  Registerinfo.objects.get (pk = uid)
    except (TypeError,ValueError,OverflowError,Registerinfo.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid
        messages.success(request,'Plese reset tour password') 
        return redirect('resetPassword')
    else:
        messages.error(request,'The link has been expired') 
        return redirect('login')
    
    
    
    
    
    
    
#user resetpassword
def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password1']
        confirm_password = request.POST['password2']
        
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Registerinfo.objects.get(pk = uid)
            user.set_password(password)
            user.save()
            messages.success(request,"new password updated")
            return redirect('login')
        else:
            messages.error(request,'Password Dose not match')
            return redirect('resetPassword')
    else:        
        return render(request,'user_temp/resetPassword.html')


        
        
    
    