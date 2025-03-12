from django.shortcuts import render,redirect,HttpResponse
from datetime import datetime
from .models import customer,Booking,Contact
import qrcode
from io import BytesIO
import base64

from django.core.mail import send_mail
from django.conf import settings
import pyotp
from django.core.mail import send_mail
import random


# Create your views here.
def home(request):
    return render(request,"index.html")


def about(request):
    return render(request,"about.html")


def contact(request):
    return render(request,"contact.html")

def book(request):
    current_time= datetime.now()
    return render(request,"book.html",{'current_time':current_time})

def register(request):
    return render(request,"register.html")
def login(request):
    return render(request,"login.html")




def save(request):
    if request.method=="POST":
        nm=request.POST["name"]
        em=request.POST["email"]
        nmb=request.POST["number"]
        add=request.POST["address"]
        ct=request.POST["city"]
        st=request.POST["state"]
        pin=request.POST["pincode"]
        ps=request.POST["password"]
        cps=request.POST["confpassword"]

        if ps==cps:

            data=customer(name=nm,email=em,number=nmb,address=add,city=ct,state=st,pincode=pin,password=ps)
            data.save()
            return redirect("/login")
        else:
            return HttpResponse("Password Not Matching")
    else:
        return HttpResponse("Fails...")



def check(request):
    if request.method=="POST":
        em=request.POST["email"]
        ps=request.POST["password"]

        data=customer.objects.filter(email=em,password=ps)
        if data:
            request.session["username"]=em
            request.session["password"]=ps
            return redirect("/dashboard")
        else:
            return HttpResponse("Fails")
    else:
        return redirect("/login")


def dashboard(request):
    if request.session.get('username') is not None:
        user_email = request.session["username"]
        password = request.session["password"]


        data = customer.objects.filter(email=user_email, password=password)
        if data:

            customer_instance = customer.objects.get(email=user_email)


            bookings = Booking.objects.filter(user=customer_instance)


            latest_booking = bookings.last()
            amount = latest_booking.amount if latest_booking else 0

            return render(request, "dashboard.html", {
                'data': data,
                'bookings': bookings,
                'amount': amount
            })
        else:
            return HttpResponse("User Not Found")
    else:
        return redirect('/')



def logout(request):
    del request.session['username']
    del request.session['password']
    return redirect('/')


def savebook(request):
    if request.method == 'POST':
        pk = request.POST['pickup']
        de = request.POST['delivery']
        gt = request.POST['goodtype']
        vt = request.POST['vehicletype']
        pd = request.POST['date']
        dt = request.POST['distance']
        am = request.POST['amount']

        # Get the logged-in user's email from the session
        user_email = request.session.get("username")

        # Get the customer instance
        customer_instance = customer.objects.get(email=user_email)

        # Create a booking and save it
        data = Booking(
            pickup=pk,
            delivery=de,
            goodtype=gt,
            vehicletype=vt,
            pickupdate=pd,
            distance=dt,
            amount=am,
            user=customer_instance
        )
        data.save()

        # Send confirmation email
        subject = "Booking Confirmation"
        message = (
            f"Dear {customer_instance.name},\n\n"
            f"Your booking has been confirmed successfully! Here are the details:\n"
            f"Pickup Location: {pk}\n"
            f"Delivery Location: {de}\n"
            f"Good Type: {gt}\n"
            f"Vehicle Type: {vt}\n"
            f"Pickup Date: {pd}\n"
            f"Distance: {dt} km\n"
            f"Amount: ₹{am}\n\n"
            f"Thank you for choosing our service!"
        )
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user_email]

        send_mail(subject, message, from_email, recipient_list)

        return redirect('/dashboard')
    else:
        return HttpResponse("Request method not allowed.")




def payment(request):
    qr_code = None
    upi_id = "9834460866-2@ibl"  # Default UPI ID
    amount = request.GET.get('amount', 0)

    if request.method == 'POST':
        payment_mode = request.POST.get('payment_mode')

        # Define payment URLs
        payment_urls = {
            'google_pay': f'upi://pay?pa={upi_id}&pn=Recipient%20Name&mc=1234&am={amount}',
            'phonepe': f'upi://pay?pa={upi_id}&pn=Recipient%20Name&mc=1234&am={amount}',
            'paytm': f'upi://pay?pa={upi_id}&pn=Recipient%20Name&mc=1234&am={amount}',
        }


        payment_url = payment_urls.get(payment_mode)
        if payment_url:
            qr = qrcode.make(payment_url)
            buffer = BytesIO()
            qr.save(buffer)
            buffer.seek(0)
            image_png = buffer.getvalue()
            qr_code = base64.b64encode(image_png).decode('utf-8')
            buffer.close()

    return render(request, 'payment.html', {'qr_code': qr_code, 'amount': amount})



def editprofile(request):
    x=request.GET["id"]
    data=customer.objects.filter(id=x)
    return render(request,"editprofile.html",{'data':data})

def saveeditprofile(request):
    if request.method=="POST":
        id=request.POST["id"]
        nm=request.POST["name"]
        em=request.POST["email"]
        nmb=request.POST["number"]
        add=request.POST["address"]
        ct=request.POST["city"]
        st=request.POST["state"]
        pin=request.POST["pincode"]
        ps=request.POST["password"]

        customer.objects.filter(id=id).update(name=nm,email=em,number=nmb,address=add,city=ct,state=st,pincode=pin,password=ps)
        return redirect("/dashboard")
    else:
        return redirect("/editprofile")

def forget(request):
    return render(request,"forget.html")


def reset_password(request):
    return render(request,"reset_password.html")








def send_otp(request):
    if request.method == "POST":
        email = request.POST["email"]
        user = customer.objects.filter(email=email).first()

        if user:
            otp = random.randint(100000, 999999)  # Generate 6-digit OTP
            request.session['reset_email'] = email
            request.session['otp'] = otp  # Store OTP in session


            subject = "Password Reset OTP"
            message = f"Your OTP for password reset is: {otp}"
            from_email = settings.EMAIL_HOST_USER
            send_mail(subject, message, from_email, [email])

            return HttpResponse(
                "<script>alert('OTP sent! Check your email.'); window.location.href='/verify_otp';</script>")
        else:
            return HttpResponse("<script>alert('Email not found!'); window.location.href='/forget';</script>")

    return render(request, 'forget_password.html')



def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST["otp"]
        saved_otp = request.session.get('otp')

        if str(entered_otp) == str(saved_otp):
            request.session['otp_verified'] = True
            return redirect('/reset_password')
        else:
            return HttpResponse(
                "<script>alert('Invalid OTP! Try again.'); window.location.href='/verify_otp';</script>")

    return render(request, 'verify_otp.html')



def reset_password(request):
    if request.method == "POST":
        if not request.session.get('otp_verified'):
            return HttpResponse("<script>alert('OTP not verified!'); window.location.href='/forget';</script>")

        email = request.session.get('reset_email')
        new_password = request.POST["new_password"]

        user = customer.objects.filter(email=email).first()
        if user:
            user.password = new_password
            user.save()


            request.session.flush()

            return HttpResponse(
                "<script>alert('Password Reset Successfully! Redirecting to login...'); window.location.href='/login';</script>")
        else:
            return HttpResponse("<script>alert('User not found!'); window.location.href='/forget';</script>")

    return render(request, 'reset_password.html')





def savemsg(request):
    if request.method=="POST":
        nm=request.POST.get('name')
        em=request.POST['email']
        nmb=request.POST['number']
        ser=request.POST['servicetype']
        msg=request.POST['message']

        data=Contact(name=nm,email=em,number=nmb,servicetype=ser,message=msg)
        data.save()

        return HttpResponse("<script>alert('we will get soon! Feedback Send Successfully'); window.location.href='/';</script>")
    else:
        return HttpResponse("fails")






import csv
from django.http import HttpResponse
from .models import customer, Booking, Contact  # Ensure model names are correctly capitalized

def excel(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data.csv"'

    writer = csv.writer(response)

    # Export Customers
    writer.writerow(['ID', 'Name', 'Email', 'Number', 'Address', 'City', 'State', 'Pincode'])
    for c in customer.objects.all():  # Use the correct model name
        writer.writerow([c.id, c.name, c.email, c.number, c.address, c.city, c.state, c.pincode])

    writer.writerow([])  # Empty row for separation

    # Export Bookings
    writer.writerow(['ID', 'Customer', 'Pickup', 'Delivery', 'Good Type', 'Vehicle Type', 'Date', 'Distance', 'Amount'])
    for b in Booking.objects.all():
        writer.writerow([
            b.id,
            b.user.name if b.user else 'N/A',  # Handle None case for ForeignKey
            b.pickup,
            b.delivery,
            b.goodtype,
            b.vehicletype,
            b.pickupdate,
            b.distance,
            b.amount
        ])

    writer.writerow([])  # Empty row for separation

    # **Export Contact Data**
    writer.writerow(['ID', 'Name', 'Email', 'Number', 'Service Type', 'Message'])
    for contact in Contact.objects.all():
        writer.writerow([
            contact.id,
            contact.name,
            contact.email,
            contact.number,
            contact.servicetype,
            contact.message
        ])

    return response











