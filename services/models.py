from django.db import models
from account.models import ClientAccount
from django.db.models import Avg,Count
# Create your views here.

class Category(models.Model):
    name=models.CharField(max_length=100,verbose_name='Service Name', null=True,blank=True)
    slug=models.SlugField(max_length=200)

    def __str__(self):
        return self.name


class Service(models.Model):
    service_name= models.CharField(max_length=200) 
    image= models.ImageField(upload_to='services/media/uploads/')
    description=models.TextField()
    original_price=models.FloatField()
    selling_price= models.FloatField()
    quantity= models.IntegerField(null=True,blank=True)
    
    category=models.ManyToManyField(Category)
    created_at = models.DateTimeField(auto_now_add=True)
     
    def __str__(self):
        return self.service_name

    def averageReview(self):
        reviews= ReviewRating.objects.filter(service=self,status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average']  is not None:
            avg= float(reviews['average'])
            return avg  
    def CountReview(self):
        reviews= ReviewRating.objects.filter(service=self,status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count']  is not None:
            count= int(reviews['count'])
            return count    
class Cart(models.Model):
    user=models.ForeignKey(ClientAccount,on_delete=models.CASCADE)
    service= models.ForeignKey(Service,on_delete=models.CASCADE, related_name = 'service')
    service_qty= models.PositiveIntegerField( default=1,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.service.service_name} -{self.user.username}"
    @property
    def total_cost(self):
        return self.service_qty*self.service.selling_price    
class ReviewRating(models.Model):
    service= models.ForeignKey(Service,on_delete=models.CASCADE)
    user=models.ForeignKey(ClientAccount,on_delete=models.CASCADE)
   
    review= models.TextField()
    rating= models.FloatField()
    status= models.BooleanField(default=True)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.service.service_name} -{self.user.username}"

