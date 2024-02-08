from django.contrib import admin
from . import models

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields ={'slug': ('name',)}
    list_display= ['name','slug']

admin.site.register(models.Category,CategoryAdmin)   


admin.site.register(models.Service)
admin.site.register(models.Cart)
admin.site.register(models.ReviewRating)