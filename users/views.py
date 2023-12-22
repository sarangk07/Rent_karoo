from django.shortcuts import render,redirect
from .forms import RegisterForm,ProfileUpdate
from .models import Registerinfo,Profile
from home.models import PickupData,Payment,Wishlist
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest ,HttpResponse

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth import update_session_auth_hash
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
import re
from functools import wraps





# Create your views here.
def logout_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


#user register
@csrf_exempt
@logout_required
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)#request.POST-- it contains all the field values
        print(request.POST)
        print("-------------------------register--------------------------")
            
    
        if form.is_valid():
            first_name = form.cleaned_data['first_name'] 
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            
            users = Registerinfo.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)   
            # users.save()
            Wishlist.objects.create(wish_user=users)
            #user Email activation 
            current_site = get_current_site(request) 
            mail_subject = "please activate your account"     
            message = render_to_string('user_temp/account_verification_email.html',{ 
               'user':users,        
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
        messages.error(request,form.errors)
    else:
        form = RegisterForm()
           
    context={'form':form}
    
    return render(request,'user_temp\signup.html',context)




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
   
   
   




@login_required(login_url='login')
@csrf_exempt
def editProfile(request, id):
    try:
        user = Registerinfo.objects.get(id=id)
        print(user, "-----------------------------=")
        form = ProfileUpdate()
        
        if request.method == 'POST':
            form = ProfileUpdate(request.POST)
            
            if form.is_valid():
                # Check if a profile exists for the user
                profile, created = Profile.objects.get_or_create(user=user)
                
                # Update the existing profile or create a new one
                profile.address = form.cleaned_data['address']
                profile.mobile = form.cleaned_data['mobile']
                profile.gender = form.cleaned_data['gender']
                profile.age = form.cleaned_data['age']
                profile.education = form.cleaned_data['education']
                profile.state = form.cleaned_data['state']
                profile.city = form.cleaned_data['city']
                profile.profilePic = form.cleaned_data['profilePic']
                
                profile.save()
                print(created,profile)

                return redirect('dashbord')
        messages.error(request,form.errors)   
        return render(request, 'user_temp/editProfile.html', {'user': user, 'form': form})
    except Exception as e:
        print('------------------An error occurred:', e)
        messages.error(request,e)
        
        return redirect('editProfile')



#user login
@logout_required
def user_login(request):
    if request.method == 'POST':
        try:
            print("---------------------User-^-login----------------------------")
            print(request.POST)
            email = request.POST['email']
            password = request.POST['password']
            print(email, password)
            users = Registerinfo.objects.get(email=email)
            print(users)
            user = authenticate(request, email=email, password=password)

            print("-----------------------------^------------------------------") 
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.warning(request, 'Invalid email or password!')
                return redirect('login')
        except Registerinfo.DoesNotExist:
            messages.warning(request, 'No user found with the provided email!')
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
    user = Registerinfo.objects.filter(email=request.user.email)
    print(user,'ddddddddddddddddddddddd')
    print(request.user,'lllllllllllllllllllllllllll')
    pickupDetails = PickupData.objects.filter(user=request.user)
    pay = Payment.objects.filter(user=request.user)
    
    
    
    wishlist_items = Wishlist.objects.filter(wish_user=request.user).first()
    
    print("/////////////////////////------------------------",wishlist_items.wish_car.all(),"---------------------------------------//////////////////")  

    context = {
        'pickupDetails':pickupDetails,
        'pay':pay,
        'wishlist_items': wishlist_items.wish_car.all() if wishlist_items else None,
    }
    return render(request,'user_temp/dashbord.html',context)











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
 
            messages.success(request,'reset password email send success! check your mail')
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
        messages.success(request,'Plese reset your password') 
        return redirect('resetPassword')
    else:
        messages.error(request,'The link has been expired') 
        return redirect('login')
    
    
#user resetpassword
def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password1']
        confirm_password = request.POST['password2']
        password_regex = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$'
        
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Registerinfo.objects.get(pk = uid)
            
            print(user.password)
            if user.check_password(password):
                messages.warning(request, 'Old password!')
                return redirect('resetPassword')
            else:
                if not re.match(password_regex, password):
                    messages.error(request,'At least 8 characters in length, Contains at least one alphabetic character (uppercase or lowercase), Contains at least one digit' )
                    return redirect('resetPassword')
                user.set_password(password)
                user.save()
                messages.success(request,"new password updated")
                return redirect('login')
        else:
            messages.error(request,'Password Dose not match')
            return redirect('resetPassword')
    else:        
        return render(request,'user_temp/resetPassword.html')




#cancel order
def cancel(request,id):
    print(id,'--------------------------id-----------------------------')
    order=PickupData.objects.get(id=id)
    bookStatus = Payment.objects.filter(user=request.user).first()
    if bookStatus:
        bookStatus.delete()
        bookStatus.is_paid=False
    order.delete()
    print("-------------order---------------",bookStatus)
    
    car=order.car
    # car.is_available=True
    car.in_garage=True
    car.save()
    
    # return render(request,'user_temp/dashbord.html')
    return redirect('dashbord')    








@login_required(login_url='login')
def changePassword(request):
    if request.method == 'POST':
        oldPassword = request.POST['oldPassword']
        password = request.POST['password1']
        confirm_password = request.POST['password2']
        password_regex = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$'
        # print("+++++++++++oldpassword", oldPassword,password,confirm_password)

        if oldPassword and password and confirm_password:
            if password == confirm_password:
                user = request.user
                print('------------------user----------------------', user.password)
                if user.check_password(oldPassword):
                    if not re.match(password_regex, password):
                        messages.error(request, 'At least 8 characters in length, Contains at least one alphabetic character (uppercase or lowercase), Contains at least one digit')
                        return redirect('changePassword')
                    user.set_password(password)
                    user.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, "New password updated")
                    return redirect('dashbord')
                else:
                    messages.warning(request, 'Old password is wrong!')
                    return redirect('changePassword')

            else:
                messages.error(request, 'Password does not match')
                return redirect('changePassword')
        else:
            messages.error(request, 'All fields must be filled')
            return redirect('changePassword')
    else:
        print("DATA NOT FOUND")
        return render(request, 'user_temp/changePassword.html')

    



 