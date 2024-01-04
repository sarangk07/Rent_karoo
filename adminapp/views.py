from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from home.models import Cars, PickupData, Payment, Wishlist
from users.models import Registerinfo, Profile
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test
from .form import CarUpdateForm
from django.contrib.auth.hashers import check_password



# Create your views here.
def super_admin(user):
    return user.is_authenticated and user.is_superadmin or user.is_staff


def adminlogin(request):
    try:
        if request.user.is_authenticated:
            return redirect("admindasbord")
        else:
            if request.method == "POST":
                email = request.POST.get("email")
                password = request.POST.get("password")
                userAdmin = Registerinfo.objects.filter(email=email).first()

                if not userAdmin:
                    print("Account not found!")
                    return render(request, "admin/adminlogin.html")

                userAdmin = authenticate(request, email=email, password=password)
                print("*********************************************admin", userAdmin)
                if userAdmin.is_superadmin:
                    login(request, userAdmin)
                    return redirect("admindasbord")

                print("Password error!!")
                return render(request, "admin/adminlogin.html")

            return render(request, "admin/adminlogin.html")

    except Exception as e:
        print(e)
        return HttpResponse("An error occurred. Please try again.")


@user_passes_test(super_admin)
def adminlogout(request):
    logout(request)
    return redirect("home")


@user_passes_test(super_admin)
def adminprofile(request):
    user = request.user
    

    admin = request.user
    users = get_object_or_404(Registerinfo, email=admin)
    print("userrrrrr", users)

    userdata = Profile.objects.get(user=users)
    print("userrrrrrssss", userdata)
    context = {"admin": admin, "userdata": userdata}
    return render(request, "admin/userEdit.html", context)


@user_passes_test(super_admin)
def adminblock(request, id):
    user = Registerinfo.objects.get(email=id)
   

    user.is_block = not user.is_block
    
    user.save()
    print("user found/n", user)
    return redirect("adminuser")

@user_passes_test(super_admin)
def adminActive(request, id):
    user = Registerinfo.objects.get(email=id)
    
    user.is_active = not user.is_active
    user.save()
    print("user found/n", user)
    return redirect("adminuser")


@user_passes_test(super_admin)
def adminStaff(request,id):
    user = Registerinfo.objects.get(email=id)
    user.is_staff = not user.is_staff
    user.save()
    return redirect("adminuser")


@user_passes_test(super_admin)
def admindasbord(request):
    users = Registerinfo.objects.all()
    cars = Cars.objects.all()
    bookings = PickupData.objects.all()
    payments = Payment.objects.all()
    wishlists = Wishlist.objects.all()
    admin = request.user

    latest_bookings = PickupData.objects.filter(pay=True).order_by("-bookedDate")[:3]
    latest_users = Registerinfo.objects.all().order_by("-date_joined")[:3]
    latest_cars = Cars.objects.all().order_by("-added_date")[:3]
    total_cars = Cars.objects.count()
    total_users = Registerinfo.objects.count()
    total_bookings = PickupData.objects.count()
    caron_go = Cars.objects.filter(in_garage=False)
    
    
    
    context = {
        "users": users,
        "payments": payments,
        "latest_bookings": latest_bookings,
        "latestusers": latest_users,
        "latest_cars": latest_cars,
        "cars": cars,
        "bookings": bookings,
        "admin": admin.first_name,
        "total_cars": total_cars,
        "total_users": total_users,
        "total_bookings": total_bookings,
        "caron_go":caron_go
    }
    return render(request, "admin/adminDashbord.html", context)


@user_passes_test(super_admin)
def userviewEdit(request, id):
    users = request.user
    user = get_object_or_404(Registerinfo, email=id)
    if users.is_staff and users.is_superadmin:
        try:
            pickups = PickupData.objects.filter(user=user).order_by("-bookedDate")
            print(
                "----------------------------------------pickupdatas-----------------------------------\n",
                pickups,
            )
            userdata = Profile.objects.get(user=user)
            context = {"user": user, "userdata": userdata, "pickups": pickups}
        except Profile.DoesNotExist:
            userdata = None
            context = {"user": user, "userdata": userdata}
            return render(request, "admin/userEdit.html", context)

        return render(request, "admin/userEdit.html", context)
    else:
        return redirect('admindasbord')
        


@user_passes_test(super_admin)
def adminuser(request):
    userss = request.user
    user = Registerinfo.objects.all()
    context = {"users": user,'userss':userss}
    return render(request, "admin/adminusers.html", context)


@user_passes_test(super_admin)
def admincars(request):
    cars = Cars.objects.all().order_by("-added_date")

    context = {"cars": cars}
    return render(request, "admin/admincars.html", context)


@user_passes_test(super_admin )
def carAdd(request):
    if request.method == "POST":
        form = CarUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("admincars")
    else:
        form = CarUpdateForm()
        
    context = {
        "form": form,
    }
    return render(request, "admin/carupdate.html", context)


@user_passes_test(super_admin)
def carUpdate(request, id):
    car = Cars.objects.get(pk=id)
    print("<><><><><><><><><><><><><<><><><>", request.POST)
    if request.method == "POST":
        form = CarUpdateForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            return redirect("admincars")
    else:
        form = CarUpdateForm(instance=car)
    context = {
        "form": form,
    }
    return render(request, "admin/carupdate.html", context)


@user_passes_test(super_admin)
def carDelete(request, id):
    car = Cars.objects.get(pk=id)
    car.delete()
    return redirect("admincars")

def adsearch(request):
    try:
        if "keyword" in request.GET:
            keyword = request.GET["keyword"]
            if keyword:
                car = Cars.objects.filter(is_available=True)
                cars = car.order_by("added_date").filter(
                    Q(model__icontains=keyword) | Q(make__icontains=keyword)
                )  # Q using for OR operator
            else:
                return redirect("admincars")  
        context = {"cars": cars}
        return render(request, "admin/admincars.html", context)
    except:
        return redirect("admincars")



@user_passes_test(super_admin )
def adminbooking(request):
    bookings = PickupData.objects.all().order_by("-bookedDate")
    payments = Payment.objects.all().order_by("-created_at")

    context = {"bookings": bookings, "payments": payments}
    return render(request, "admin/adminbookings.html", context)


def adminbook(request, id):
    payments = Payment.objects.filter(booking=id)
    print( payments)
    context = {
        'payments': payments
    }
    return render(request, "admin/userEdit.html", context)


@user_passes_test(super_admin)
def paymentDetails(request):
    user = request.user
    payments = Payment.objects.all().order_by("-created_at")

    context = {"payments": payments,'user':user}
    return render(request, "admin/paymentView.html", context)


def paymentDelete(request, id):
    payment = get_object_or_404(Payment, pk=id)
    payment.delete()
    return redirect("paymentDetails")
