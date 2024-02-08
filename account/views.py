from django.shortcuts import render,redirect
from  .forms import UserRegistrationForm,MakeAdminForm, UserUpdateForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from account.models import ClientAccount
from django.contrib.auth import login,logout
from django.views.generic import FormView
from django.views.generic import ListView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView,PasswordChangeView
from order.models import Order
from django.contrib.auth.models import User
from django.db.models import Avg,Count
from django.http import HttpResponse
from django.views.generic import DetailView
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.decorators import method_decorator 
from django.urls  import reverse_lazy
from django.views.generic import UpdateView
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string

def send_order_confirmation_email(user,order,subject,template):
    message = render_to_string(template,{
        'user':user,
        'order':order,

    })
    send_email=EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()

class UserRegistrationView(FormView):
    template_name= "register.html"
    form_class=UserRegistrationForm
    success_url=reverse_lazy('profile_update')

    def form_valid(self, form):
        user=form.save() #save method call
        
        login(self.request,user) 
        messages.success(self.request, "Registration Successfull")
        send_order_confirmation_email(user, '', 'Registration Confirmation', 'registration_confirmation_email.html')

        print(user)
        return super().form_valid(form)

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['type'] = 'Register'
        return context   


class UserLoginView(LoginView):
    template_name='login.html'
    def get_success_url(self):
        return reverse_lazy('homepage')

    def form_valid(self, form):
        messages.success(self.request, "Logged in Successful")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.success(self.request, "Please Enter valid information")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
          context = super().get_context_data(**kwargs)
          context['user'] = self.request.user
          context['type'] = 'Log In'
          return context           


@login_required
def user_logout(request):
    if request.user.is_authenticated:
            logout(request)
    return redirect('homepage')   


@login_required
def admin_dashboard(request):
    user_count=ClientAccount.objects.count()
    order_count=Order.objects.count()

    context={
        'user_count':user_count,
        'order_count':order_count,
    }

    return render(request, 'admin_dashboard.html', context)

# def make_admin(request,user_id):
#     user_to_make_admin =ClientAccount.objects.get(id=user_id)

#     if request.method=='POST':
#         form =MakeAdminForm(request.POST)

#         if form.is_valid():
#             user_to_make_admin.is_admin =True 
#             user_to_make_admin.is_staff=True 
#             user_to_make_admin.save()
#             return redirect('homepage')

#     else:
#         form =MakeAdminForm(initial={'user_id':user_id})

#         return render(request,'make_admin.html',{'form':form, 'user_to_make_admin':user_to_make_admin})          



def make_admin(request):
   

    if request.method=='POST':
        form =MakeAdminForm(request.POST)

        if form.is_valid():
            user_to_make_admin = form.cleaned_data['user_to_make_admin']
            user_to_make_admin.is_admin =True 
            user_to_make_admin.is_staff=True 
            user_to_make_admin.save()
            return redirect('homepage')

    else:
       
        form =MakeAdminForm()

    return render(request,'make_admin.html',{'form':form})          


def all_order_show(request):
    # all_orders=Order.objects.select_related('service').all()
    all_orders=Order.objects.all()
    context={
        'all_orders':all_orders
        }
    return render(request,'all_order_show.html',context)    

def Approve_order(request,order_id):
    order=Order.objects.get(id=order_id)

    if order.status =='PENDING':
        order.status ='APPROVED'
        order.save()
        messages.success(request,"This Order Approved")
        send_order_confirmation_email(order.user,order,'approve_order','order_approve_email.html')
        return redirect('admin_dashboard')
    if order.status =='CANCELLED':
        order.status ='PENDING'
        order.save()
        messages.success(request,"This Order you can  Re-Approved")
        return redirect('admin_dashboard')    
    # Return a response indicating that the order is not pending
    # return HttpResponse("This order is not pending and can be re-approved.")    

def Cancelled_order(request,order_id):
    order=Order.objects.get(id=order_id)

    if order.status =='PENDING':
        order.status ='CANCELLED'
        order.save()
        messages.success(request,"This Order Cancel")
        send_order_confirmation_email(order.user,order,'cancel_order','order_cancel_email.html')
        return redirect('admin_dashboard')
        
class UserProfileView(DetailView):
    template_name ='profile.html'
    model = ClientAccount
    context_object_name ='profile'
    def get_object(self, queryset=None):
        return self.request.user


@method_decorator(login_required,name='dispatch')
class EditPasswordView(PasswordChangeView):
    template_name='edit_pass.html'
   
    def get_success_url(self):
        return reverse_lazy('profile_view')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Password Change Successful")
        return super().form_valid(form)


class UpdateProfileView(UpdateView):
    model = ClientAccount
    form_class=UserUpdateForm
    template_name ='profile_update.html'

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        u_form = self.form_class(instance=self.object)
        return render(request,'profile_update.html',{'form':u_form})
    

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        u_form = self.form_class(request.POST,request.FILES,instance=self.object)

        if u_form.is_valid():
            u_form.save()
            messages.success(request, 'Your Profile has been updated!')
            return redirect('profile_view')
        return render(request,'profile_update.html',{'form':u_form})        


