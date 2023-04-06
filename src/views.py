from django.shortcuts import render

# Create your views here.
import razorpay
from .models import Coffee
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
import os
from dotenv import load_dotenv,find_dotenv

load_dotenv(find_dotenv())

def home(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        amount = int(request.POST.get("amount")) *100
        PUBLIC_KEY = os.environ.get("RAZOR_PUBLIC_KEY")
        SECRET_KEY = os.environ.get("RAZOR_SECRET_KEY")
        client = razorpay.Client(auth=(PUBLIC_KEY,SECRET_KEY))
        data = {"amount":amount,"currency":"INR","payment_capture":1}
        payment = client.order.create(data=data)
        print(payment)
        coffee = Coffee(name=name,email=email,amount=amount,payment_id=payment['id'])
        coffee.save()
        print(coffee)
        return render(request,"index.html", {'payment':payment})
    return render(request,"index.html")

@csrf_exempt
def success(request):
    if request.method == "POST":
        a = request.POST
        for key,val in a.items():
            if key == 'razorpay_order_id':
                order_id = val
                break
        print(order_id)
        user = Coffee.objects.filter(payment_id = order_id).first()
        user.paid = True
        user.save()
        name = user.name
        amount = int(user.amount)/100
        msg_plain = render_to_string('email.txt', {'name': name, 'amount': amount})
        msg_html = render_to_string('email.html',  {'name': name, 'amount': amount})
        send_mail("You Donation has been received", msg_plain, settings.EMAIL_HOST_USER,[user.email],html_message=msg_html)
    return render(request,"success.html")

def failure(request):
    return render(request,"failure.html")


        