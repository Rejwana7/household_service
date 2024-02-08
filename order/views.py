from django.shortcuts import render,redirect
from services.models import Service, Cart
from account.models import ClientAccount
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Order
from django.contrib.auth import login,logout
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
# Create your views here.
def send_order_email(user,order,subject,template):
    message = render_to_string(template,{
        'user':user,
        'order':order,

    })
    send_email=EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()
@login_required
def place_order(request):

    cart_items=Cart.objects.filter(user=request.user)

    if request.method=='POST':
        # address phone no
        address=request.POST.get('address')
        phone=request.POST.get('phone')

        for cart_item in cart_items:
            new_order=Order.objects.create(

                user=request.user,
                service=cart_item.service,
                quantity=cart_item.service_qty,
                address=address,
                phone=phone,
                status='PENDING',

            )

            new_order.calculate_total_amount()
           
            messages.success(request,"Order Placed Successfully")
            send_order_email(request.user,new_order,'order_placed','order_placed_email.html')

        cart_items.delete()
        return redirect('order_history')
    return render(request,'view_cart.html',{'cart_items':cart_items})


def Order_history(request):
    orders=Order.objects.filter(user=request.user) 

    grand_total=sum(order.total_amount for order in orders)
   

    return render(request,'order_history.html',{'orders':orders,'grand_total':grand_total})   