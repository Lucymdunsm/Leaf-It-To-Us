
from django.contrib import admin
from core.models import UserProfile

admin.site.register(UserProfile)

# Register your models here.

# from django.contrib import admin
# from core.models import Category, Tea, Review
#   
#   
# class CategoryAdmin(admin.ModelAdmin):
#     prepopulated_fields = {'slug':('name',)}
#  
# admin.site.register(Category, CategoryAdmin)

