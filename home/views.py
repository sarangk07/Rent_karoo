from django.shortcuts import render, redirect
from home.models import Cars, PickupData, Payment, Wishlist
from users.models import Registerinfo, Profile

from django.http import HttpResponse
from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import datetime

from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import razorpay

import re
from django.shortcuts import get_object_or_404
from django.conf import settings

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.core.paginator import Paginator


# Create your views here.

# -------Pendings-------

# booking date kazhinjal [pickupData htmlpage] a car dy not available anenn message kalayanam

# Admin page


# home page
def home(request):
    cars = Cars.objects.filter(is_available=True)

    if request.user.is_authenticated:
        try:
            profuser = get_object_or_404(Profile, user=request.user)
            context = {"cars": cars, "profuser": profuser}
        except:
            context = {"cars": cars}
            return render(request, "index.html", context)
    else:
        print(cars)
        context = {"cars": cars}
    return render(request, "index.html", context)


# pickupDetails view
@login_required(login_url="login")
@csrf_exempt
def pickupDetails(request, id):
    try:
        cars = Cars.objects.get(id=id)
        allcars = Cars.objects.all()
        users = request.user
        all_pickups = PickupData.objects.all()

        # Retrieve other bookings for the same car with payment
        other_bookings = PickupData.objects.filter(
            Q(car=cars) & ~Q(id=id) & Q(pay=True)
        )

        context = {
            "cars": cars,
            "allcars": allcars,
            "users": users,
            "other_bookings": other_bookings,
        }

        return render(request, "garage/pickupDetails.html", context)

    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect("pickupDetails", id=id)


# car details
def carDetails(request, id):
    print(id)
    cars = Cars.objects.get(id=id)

    context = {"cars": cars}
    return render(request, "garage/car-single.html", context)


# all cars
# @login_required
def cars(request):
    cars = Cars.objects.filter(is_available=True)

    print("*-/*-/-*-*-*-///-*/*", cars)
    paginator = Paginator(cars, 6)
    page = request.GET.get("page")
    paged_product = paginator.get_page(page)

    if request.user.is_anonymous:
        print("Anonymous User============================================")
        context = {"cars": paged_product, "user": request.user}
        return render(request, "garage/cars.html", context)
    else:
        print("User=========================================")
        wishlist = Wishlist.objects.get(wish_user=request.user)
        cars_in_wishlist = [car for car in cars if car in wishlist.wish_car.all()]
        context = {"cars": paged_product, "wishlist": cars_in_wishlist}
        return render(request, "garage/cars.html", context)


# car search
def search(request):
    if "keyword" in request.GET:
        keyword = request.GET["keyword"]
        if keyword:
            car = Cars.objects.filter(is_available=True)
            cars = car.order_by("added_date").filter(
                Q(model__icontains=keyword) | Q(make__icontains=keyword)
            )  # Q using for OR operator
        else:
            return redirect("cars")
        paginator = Paginator(cars, 6)
        page = request.GET.get("page")
        paged_product = paginator.get_page(page)

        if request.user.is_anonymous:
            context = {"cars": paged_product}
        else:
            wishlist = Wishlist.objects.get(wish_user=request.user)
            cars_in_wishlist = [car for car in cars if car in wishlist.wish_car.all()]
            context = {"cars": paged_product, "wishlist": cars_in_wishlist}
    return render(request, "garage/cars.html", context)


# car type sorting
def sorting(
    request,
    car_type=None,
):
    if car_type:
        car = Cars.objects.filter(is_available=True)
        cars = car.filter(carType__icontains=car_type).order_by("added_date")

        paginator = Paginator(cars, 6)
        page = request.GET.get("page")
        paged_product = paginator.get_page(page)
        if request.user.is_anonymous:
            context = {"cars": paged_product}
        else:
            wishlist = Wishlist.objects.get(wish_user=request.user)
            cars_in_wishlist = [car for car in cars if car in wishlist.wish_car.all()]
            context = {"cars": paged_product, "wishlist": cars_in_wishlist}
        return render(request, "garage/cars.html", context)
    else:
        return redirect("cars")


# car price sorting
def priceSorting(request, sort_type=None):
    cars = Cars.objects.filter(is_available=True)

    if sort_type == "price_low_to_high":
        cars = cars.order_by("rentAmount")
    elif sort_type == "price_high_to_low":
        cars = cars.order_by("-rentAmount")
    elif sort_type == "below_500":
        cars = cars.filter(rentAmount__lt=500)
    else:
        return redirect("cars")

    paginator = Paginator(cars, 6)
    page = request.GET.get("page")
    paged_product = paginator.get_page(page)
    if request.user.is_anonymous:
        context = {"cars": paged_product}
    else:
        wishlist = Wishlist.objects.get(wish_user=request.user)
        cars_in_wishlist = [car for car in cars if car in wishlist.wish_car.all()]
        context = {"cars": paged_product, "wishlist": cars_in_wishlist}
    return render(request, "garage/cars.html", context)


# add wishlist
def add_to_wishlist(request, car_id):
    if request.user.is_authenticated:
        if request.method == "POST":
            car = Cars.objects.get(pk=car_id)
            user = request.user

            wishitem, created = Wishlist.objects.get_or_create(wish_user=user)

            if created:
                wishitem.wish_car.add(car)
                data = {
                    "message": "Wishlist added successfully",
                }
            else:
                wishitem.wish_car.add(car)
                data = {
                    "message": "Wishlist already exists",
                }

                # Get the referring URL
                referer = request.META.get("HTTP_REFERER", None)

                # If the referring URL exists and matches the allowed hosts, redirect back to it.
                if referer:
                    allowed_hosts = ['rentkaro.shop', '16.171.1.65']
                    for host in allowed_hosts:
                        if referer.startswith(f'https://{host}') or referer.startswith(f'http://{host}'):
                            return HttpResponseRedirect(referer)

            return redirect("cars")  # Adjust the redirect URL if needed
        else:
            return redirect("home")



# def add_to_wishlist(request, car_id):
#     if request.user.is_authenticated:
#         if request.method == "POST":
#             car = Cars.objects.get(pk=car_id)  # car id
#             user = request.user  # user email

#             print("------request.user----------*******CAR**", car.id, user)

#             wishitem, created = Wishlist.objects.get_or_create(wish_user=user)

#             if created:
#                 wishitem.wish_car.add(car)
#                 data = {
#                     "message": "Wishlist added successfully",
#                 }
#             else:
#                 wishitem.wish_car.add(car)
#                 data = {
#                     "message": "Wishlist already exists",
#                 }

#                 referer = request.META.get("HTTP_REFERER", None)

#                 if referer and referer.startswith(request.build_absolute_uri("/")):
#                     return HttpResponseRedirect(referer)
#         else:
#             return redirect("home")






# remove wishlist
def remove_from_wishlist(request, car_id):
    if request.user.is_authenticated:
        car = Cars.objects.get(pk=car_id)
        wishlist = Wishlist.objects.get(wish_user=request.user)
        wishlist.wish_car.remove(car)
        wishlist.save()

        # Get the referring URL
        referer = request.META.get("HTTP_REFERER", None)

        # If the referring URL exists and matches the allowed hosts, redirect back to it.
        if referer:
            allowed_hosts = ['rentkaro.shop', '16.171.1.65']
            for host in allowed_hosts:
                if referer.startswith(f'https://{host}') or referer.startswith(f'http://{host}'):
                    return HttpResponseRedirect(referer)

    # If no referring URL or it doesn't match, redirect to "dashbord".
    return redirect("dashbord")



# terms and conditions
def termsandConditions(request):
    return render(request, "garage/terms&conditions.html")


# payment


@login_required(login_url="login")
def payment(request, id):
    try:
        cars = Cars.objects.get(id=id)
        # pickupDatas = PickupData.objects.filter(car.model==cars)

        # print(",.,.,.,.,.,.,.,.,.<><><><><><><><><><><><><><<><><><><><><><><><><",pickupDatas)
        users = request.user
        allcars = Cars.objects.all()
        all_pickups = PickupData.objects.all()

        cars.save()

        if request.method == "POST":
            pickup = request.POST["pickup"]
            dropoff = request.POST["dropoff"]
            pickuptime = request.POST["pickuptime"]
            pickuplocation = request.POST["pLocation"]
            email = request.POST["email"]
            mobile = request.POST["mobile"]
            licence = request.POST["licence"]

            car = cars
            user = users
            selected_plan = request.POST["selected_plan"]

            if "tc" in request.POST:
                tc = request.POST["tc"]
            else:
                messages.error(request, "You must agree to the Terms and Conditions.")
                return redirect("pickupDetails", id=id)

            if not all([pickup, dropoff, pickuptime, email, mobile, licence]):
                messages.error(request, "fill all the fields")
                return redirect("pickupDetails", id=id)

            elif len(mobile) != 10:
                messages.error(request, "mobile number need 10 digits!")
                return redirect("pickupDetails", id=id)

            # Input time in the format '12:30am'
            input_time = pickuptime

            # Convert the input time to a datetime object
            time_obj = datetime.strptime(input_time, "%I:%M%p")
            # Format the datetime object to the desired time format
            formatted_time = time_obj.strftime("%H:%M:%S")

            # current date
            current_date = datetime.now()
            formatted_date = current_date.strftime("%m-%d-%Y")
            formatted_date_obj = datetime.strptime(formatted_date, "%m-%d-%Y").date()

            print(formatted_date_obj)
            print(type(formatted_date_obj))

            pickup_datetime = datetime.strptime(pickup, "%m/%d/%Y")
            dropoff_datetime = datetime.strptime(dropoff, "%m/%d/%Y")
            print("-------------formated.date.type---------", formatted_date_obj)

            # Check if there's any overlap with existing bookings

            rental_days = (dropoff_datetime - pickup_datetime).days
            totalAmt = rental_days * cars.rentAmount
            gst = int(totalAmt * 5 / 100)
            gTotal = int(totalAmt + gst)
            print(f"{rental_days} days")

            input_time = pickuptime
            time_obj = datetime.strptime(input_time, "%I:%M%p")
            formatted_time = time_obj.strftime("%H:%M:%S")
            pickup_datetime = datetime.strptime(pickup, "%m/%d/%Y")
            dropoff_datetime = datetime.strptime(dropoff, "%m/%d/%Y")
            rental_days = (dropoff_datetime - pickup_datetime).days

            # picDays = (dropoff_datetime - formatted_date_obj).days
            totalAmt = rental_days * cars.rentAmount

            if car.carType == "SUV":
                plan_values = {"Silver": 900, "Gold": 1300, "Diamond": 1500}
            elif car.carType == "Sedan":
                plan_values = {"Silver": 850, "Gold": 1200, "Diamond": 1400}
            elif car.carType == "Hatchback":
                plan_values = {"Silver": 800, "Gold": 1100, "Diamond": 1300}
            else:
                plan_values = {"Silver": 700, "Gold": 1000, "Diamond": 1100}

            planTotal = plan_values.get(selected_plan, 0) + totalAmt
            gst = int(planTotal * 5 / 100)
            gTotal = int(planTotal + gst)

            if not re.match(r"^(\+\d{1,3}[- ]?)?\d{10}$", mobile):
                messages.error(request, "This is not a valid mobile number!")
                return redirect("pickupDetails", id=id)

            if not re.match(r"^[A-Z]{2}[0-9]{2}[A-Z]{2}[0-9]{4}$", licence):
                messages.error(request, "This is not a valid licence number!")
                return redirect("pickupDetails", id=id)

            if not re.match(r"^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$", email):
                messages.error(request, "This is not a valid email!")
                return redirect("pickupDetails", id=id)

            # Dropoff date not be lower that pickup date!
            if pickup_datetime > dropoff_datetime:
                messages.error(request, "Dropoff date not be lower that pickup date!")
                return redirect("pickupDetails", id=id)

            # Pickup date can't be Past Date!
            elif formatted_date_obj > pickup_datetime.date():
                print("==================error=====================")
                messages.error(request, "Pickup date can't be Past Date!")
                return redirect("pickupDetails", id=id)
            # pickupdate not go longer that 1 month
            # -----code---wandto write------

            # When dropoff_date is equal to current date
            if formatted_date_obj == pickup_datetime.date():
                cars.in_garage = False
                cars.save()
            # When dropoff_date is equal to current date
            if formatted_date_obj == dropoff_datetime.date():
                cars.in_garage = True
                cars.save()

            # Rent a car only for 100 Days
            if rental_days > 100:
                messages.error(request, "Rent a car maximum 100 Days only!!")
                return redirect("pickupDetails", id=id)

            # Rent a car with in 60 day from current day  [pickup_datetime time not go longer that 60 days from current day]
            # if picDays>60:
            #     messages.error(request, "rent a car with in 60 Days")
            #     return redirect('pickupDetails', id=id)

            # licence id validation!

            # if all_pickups.licence_ID == licence:
            #     messages.error(request, "licence id must be unique!")
            #     return redirect("pickupDetails", id=id)

            if any(
                pickup_datetime.date() == pickup.pickup_date
                and cars.model == pickup.car.model
                and pickup.pay
                for pickup in all_pickups
            ):
                messages.error(
                    request, "Date already booked for the same car with payment!"
                )
                return redirect("pickupDetails", id=id)
            elif any(
                (
                    pickup_datetime.date()
                    <= pickup.dropoff_date
                    <= dropoff_datetime.date()
                    or pickup_datetime.date()
                    <= pickup.pickup_date
                    <= dropoff_datetime.date()
                    or (
                        pickup.pickup_date <= pickup_datetime.date()
                        and dropoff_datetime.date() <= pickup.dropoff_date
                    )
                )
                and cars.model == pickup.car.model
                and pickup.pay
                for pickup in all_pickups
            ):
                messages.error(
                    request,
                    "There is another booking for the same car in the date period!",
                )
                return redirect("pickupDetails", id=id)

            print(
                "++++allPayment+++++++++++++++++++++++++++++++++++++++++",
                all_pickups,
                "++++++++++++++++++++++++++++++++++++++++++",
            )

            print("--------------else-------------", pickup_datetime)
            print(type(pickup_datetime))

            pickup_data = PickupData(
                Pickup_time=formatted_time,
                pickup_date=pickup_datetime.date(),
                dropoff_date=dropoff_datetime.date(),
                PickLocation=pickuplocation,
                mobile_number=mobile,
                licence_ID=licence,
                car=car,
                user=user,
                plan=selected_plan,
                totalAMT=gTotal,
            )
            pickup_data.save()

            # razorpay_payment-------------------------------------
            client = razorpay.Client(auth=(settings.KEYID, settings.KEY))

            payment = client.order.create(
                {"amount": gTotal * 100, "currency": "INR", "payment_capture": 1}
            )
            print("++++++++++payment++++++++++++", payment)
            # pay = Payment(
            #     razorpay_order_id=payment['id']
            # )
            # pay.save()

            pickup_data.save()
            other_bookings = PickupData.objects.filter(
                Q(car=cars) & ~Q(id=pickup_data.id)
            )
            print("-----------razorpay------------")
            print(client)
            print(payment, "********payment********")

            context = {
                "cars": cars,
                "pickup_data": pickup_data,
                "rental_days": rental_days,
                "totalAmt": totalAmt,
                "gst": gst,
                "gTotal": gTotal,
                "payment": payment,
                "other_bookings": other_bookings,
                "selected_plan": selected_plan,
            }
            print(
                "**---------------------------------------",
                cars,
                pickup_data,
                rental_days,
                "-------------------",
                other_bookings,
                "----------------------**",
            )
            print(totalAmt, gst, gTotal)
            print(payment)
            return render(request, "payment/paymentpage.html", context)
        # else:
        context = {
            "cars": cars,
        }
        return render(request, "payment/paymentpage.html", context)
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect("pickupDetails", id=id)


# payment success
@login_required
def success(request):
    try:
        user = request.user
        pickups = PickupData.objects.filter(user=user)

        if pickups.exists():
            print("found")
            pickup = pickups.first()  # or .last()
            last_pickup = pickups.last()
            print(
                "PickupData found for the user----------------------------",
                pickup,
                last_pickup,
            )
        else:
            print(
                "No PickupData found for the user----------------------------",
                pickup,
                last_pickup,
            )
            messages.error(request, "No Data found for the user.")
            return redirect("pickupData")

        orderid = request.GET.get("orderid")
        payment_id = request.GET.get("razorpay_payment_id")
        signature = request.GET.get("razorpay_signature")

        payment = Payment.objects.create(
            razorpay_order_id=orderid,
            razorpay_payment_id=payment_id,
            razorpay_payment_signature=signature,
            user=user,
            booking=pickup,
        )

        payment.is_paid = True
        last_pickup.pay = True
        last_pickup.save()
        payment.save()

        # Send email to the booked user
        subject = "Booking Information"
        message = render_to_string(
            "payment/booking_confirmation_email.html",
            {"pickup": pickup, "payment": payment},
        )
        plain_message = strip_tags(message)
        to_email = [user.email]

        send_mail(subject, plain_message, None, to_email, html_message=message)

        return redirect("dashbord")
    except Exception as e:
        print("error", e)

    # client = razorpay.Client(auth=(settings.KEYID, settings.KEY))
    return HttpResponse("An Error Occurred!",e)
