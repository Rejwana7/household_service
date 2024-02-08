from django.db import models
from account.models import ClientAccount
from services.models import Service, Cart
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
# Create your models here.


class Order(models.Model):
    user=models.ForeignKey(ClientAccount,on_delete=models.CASCADE)
    service= models.ForeignKey(Service,on_delete=models.CASCADE, related_name = 'order')
    created_at = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES=[
        ('PENDING','Pending'),
        ('APPROVED','Approved'),
        ('CANCELLED','Cancelled'),
    ]
    status=models.CharField(max_length=20,choices=STATUS_CHOICES)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    address=models.CharField(null=True,blank=True,max_length=200)
    phone=models.CharField(null=True,blank=True,max_length=12)
    quantity=models.PositiveIntegerField( default=1,null=True,blank=True)

    def calculate_total_amount(self):
        total_amount=self.quantity *self.service.selling_price
        self.total_amount=total_amount
        self.save()
    
    
   

   