from django.shortcuts import render,redirect
from django.http import HttpResponse

from services.models import Category
from services.models import  Service
from django.views.generic import ListView
from . import forms
from django.contrib import messages
# Create your views here
class Homeview(ListView):
    model= Service
    template_name='home.html'
    context_object_name='data'
    
    def get_queryset(self):
        category_slug=self.kwargs.get('category_slug')

        if category_slug:
            category=Category.objects.get(slug=category_slug)
            return Service.objects.filter(category=category)

        return Service.objects.all()  

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        # context['service'] = Service.objects.all()
        return context   

# class Homeview(ListView):
#     model = Service
#     template_name = 'home.html'
#     context_object_name = 'services'  # Renamed from 'data' to 'services'
    
#     def get_queryset(self):
#         category_slug = self.kwargs.get('category_slug')

#         if category_slug:
#             category = Category.objects.get(slug=category_slug)
#             return Service.objects.filter(category=category)

#         return Service.objects.all()

#     def get_context_data(self, **kwargs): 
#         context = super().get_context_data(**kwargs)
#         context['categories'] = Category.objects.all()
#         return context


def ContactUs(request):
    if request.method=='POST':
        fm=forms.ContactForm(request.POST)
        if fm.is_valid():
            fm.save()
            messages.success(request,'Thanks For Contact Us')
            return redirect("homepage")
    else:
        fm=forms.ContactForm()
    return render(request,'contact.html',{'form':fm})


def About_us(request):
    return render(request,'about_us.html')    