from django.shortcuts import render,redirect

from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.contrib.auth import login,logout
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from . import forms
from .forms import ReviewRatingForm,UpdateReviewForm

from django.views.generic import DetailView
from  .models import Service,ReviewRating

from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .models import Cart, Category
from django.views.generic import ListView
from django.db.models import Sum
from django.db.models import Count
from django.http import JsonResponse
from django.db.models import Q
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string

def send_email(user,service_name,subject,template):
    message = render_to_string(template,{
        'user':user,
        'service_name':service_name,

    })
    send_email=EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()

# class ServiceDetailView(DetailView):
#     model=Service
#     template_name ='details.html'
#     context_object_name = 'service'

#     # pk_url_kwarg = 'id'

#     def post(self,request,*args,**kwargs):
#         service=self.get_object()
#         if self.request.method=="POST": 
#             reviews_form=forms.ReviewRatingForm(data=request.POST)
#             if  reviews_form.is_valid():
#                 new_comment=ReviewRatingForm.save(commit=False)
#                 new_comment.service=service
#                 new_comment.user= self.request.user
#                 new_comment.save()
#             return self.get(request, *args,**kwargs)  
#     def get_context_data(self, **kwargs):
#         context=super().get_context_data(**kwargs)
#         service=self.object
#         reviews=service.reviews.all()
#         reviews_form=forms.ReviewRatingForm()
#         context['reviews']=reviews
#         context['reviews_form'] = reviews_form



def service_detail(request,id):
    service = Service.objects.get(id=id)

    reviews=ReviewRating.objects.filter(service_id=service.id,status=True)

    context= {
        'service':service,
        'reviews':reviews,
    }
    return render(request,'detail.html',context)


# def Submit_review(request,id):
#     if request.method=='POST':
#         try:
#             reviews=ReviewRating.objects.get(user__id=request.user.id,service__id=id)
#             form=ReviewRatingForm(request.POST,instance=reviews)
#             form.save()
#             messages.success(request,'Thank You! Your review has been updated.')
#             return redirect("homepage")
#         except ReviewRating.DoesNotExist:
#             form= ReviewRatingForm(request.POST)
#             if form.is_valid():
#                 data=ReviewRating()
#                 data.review = form.cleaned_data['review']
#                 data.rating= form.cleaned_data['rating']
#                 data.service_id=id
#                 data.user_id= request.user.id
#                 data.save()
#                 messages.success(request,'Thank You! Your review has been submitted.')
#                 return redirect("homepage")



def Submit_review(request,id):
    service=get_object_or_404(Service,id=id)
    form=ReviewRatingForm(request.POST)
    # Assuming 'review' and 'rating' are extracted from the form data
    # review = request.POST.get('review', '')
    # rating = request.POST.get('rating', '')

    if request.method =='POST':
       if form.is_valid():
        data= form.save(commit=False)
        review = form.cleaned_data['review']
        rating = form.cleaned_data['rating']
        data.user=request.user
        data.service=service
        data.review=review
        data.rating=rating
        data.save()
        messages.success(request, 'Thank you! Your review has been submitted.')
        return redirect("homepage")

    context = {
        'service': service,
        'form': form,
    }
    return render(request, 'detail_2.html', context)


# def Update_review(request,id):
#     review = get_object_or_404(ReviewRating, id=id)
#     service = review.service  # Retrieve the related service
#     reviews = ReviewRating.objects.filter(service=service) 
#     if request.method == 'POST':
#         form =UpdateReviewForm(request.POST, instance=review)
#         if form.is_valid():
#             form.instance.user=request.user
#             form.save()
#             messages.success(request, 'Thank you! Your review has been updated.')
#             return redirect("homepage")
#     else:
#         form = UpdateReviewForm(instance=review)

#     context = {
#         'form': form,
#         'review': review, 
#         'service': service,  # Pass the service to the context
#         'reviews': reviews,
#     }
#     return render(request, 'update_review.html', context)




def Update_review(request,id):
    review = get_object_or_404(ReviewRating, id=id)
    service = review.service  # Retrieve the related service
    reviews = ReviewRating.objects.filter(service=service) 
    if request.method == 'POST':
        form = ReviewRatingForm(request.POST, instance=review)
        if form.is_valid():
            form.instance.user=request.user
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect("homepage")
    else:
        # form = ReviewRatingForm(instance=review)
        
        # Pass the user's previous comment to the form
        initial_data = {'rating': review.rating, 'review': review.review}
        form = ReviewRatingForm(instance=review, initial=initial_data)


    context = {
        'form': form,
        'review': review, 
        'service': service,  # Pass the service to the context
        'reviews': reviews,
    }
    return render(request, 'update_review.html', context)

@login_required
def Add_to_Cart(request,service_id):
    user=request.user
    service=Service.objects.get(id=service_id)
     # Check if the item is already in the cart
    cart_item,created=Cart.objects.get_or_create(user=user,service=service)

    if not created:
        #item already in cart
        messages.info(request, 'This service is already in your cart.')
        send_email(user, service.service_name, 'already_in_cart', 'already_in_cart_email.html')
    else:
         # Item added to the cart
        messages.success(request, f'{service.service_name} added to your cart.')    
        send_email(user,service.service_name,'add_to_cart','add_cart_email.html')
    cart_item.save() 
    return redirect("homepage")    

# def View_Cart(request):
#     user=request.user
#     cart_data=Cart.objects.filter(user=user)
#     amount=0
#     for p in cart_data:
#         value= p.service_qty *p.service.selling_price
#         amount=amount+value
#     totalamount =amount    

#     return render(request,'view_cart.html',{'cart_data':cart_data, 'amount': amount, 'totalamount': totalamount})


class ViewCartView(LoginRequiredMixin,ListView):
    model =Cart
    template_name='view_cart.html'
    context_object_name='cart_data'
    def get_queryset(self): 
        user=self.request.user
        cart_data=Cart.objects.filter(user=user)
        return cart_data

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(**kwargs)

        # Calculate amount and totalamount
        amount=sum(item.total_cost for item in context['cart_data'])
        totalamount=amount

        context['amount']=amount
        context['totalamount'] = totalamount

        return context


# def plus_cart(request):
#     if request.method=='GET':
#         # service_id=request.GET['service_id']
#         service_id=request.GET.get('service_id')
#         c=Cart.objects.get(Q(service=service_id) & Q(user=request.user))
#         c.service_qty+=1
#         c.save()
#         # print(service_id)
#         user=request.user
#         cart=Cart.objects.filter(user=request.user)
#         amount=0
#         for p in cart_data:        
#             value= p.service_qty *p.service.selling_price
#             amount=amount+value
#             totalamount =amount    
#         data={
#         'service_qty':c.service_qty,
#         'amount':amount,
#         'totalamount':totalamount
#         }

#         return JsonResponse(data)


def increase_quantity(request,cart_id):
    cart_item = get_object_or_404(Cart,pk=cart_id)

    if cart_item.user == request.user:
        cart_item.service_qty+=1
        cart_item.save()

        return redirect("view_cart")


def decrease_quantity(request,cart_id):
    cart_item = get_object_or_404(Cart,pk=cart_id)

    if cart_item.user == request.user:
        if cart_item.service_qty > 1:
            cart_item.service_qty-=1
            cart_item.save()

    return redirect("view_cart")        

@login_required
def remove_cart(request,cart_id):
    cart_item = get_object_or_404(Cart,pk=cart_id)

    if cart_item.user == request.user:
        
            cart_item.delete()

    return redirect("view_cart")      




# def category_detail_view(request,category_slug):
#     selected_category=Category.objects.get(slug=category_slug)
#     services=Service.objects.filter(category=selected_category)
#     context = {
#         'category': selected_category,
#         'services': services,
#     }

#     return render(request,'navber.html',context)   

# def categories_list(request,category_slug):
#     category=None
#     categories=Category.objects.all()
#     services=Service.objects.all()
#     if category_slug:
#       category =get_object_or_404(Category, slug=category_slug)
#       services=Service.objects.filter(category=category)
#     return render(request, 'category_list.html', {'categories': categories,'category':category,'services':services})


# def category_detail(request):
#     service=get_object_or_404(Service,id=id)

    
    #return render(request, 'category_detail.html', {'service': services})    


def all_services(request):
    services=Service.objects.all()
    categories = Category.objects.all()
    return render(request,'all_services.html',{'services':services,'categories': categories}) 

def services_by_category(request,category_slug):
    # category=Category.objects.get(slug=category_slug)
    category = get_object_or_404(Category, slug=category_slug)
    services=Service.objects.filter(category=category)
    categories = Category.objects.all()
    # categories = [category]  
    return render(request,'services_by_category.html',{'services': services, 'category': category,'categories': categories})       