
from django.contrib import admin
# Import models here.
from core.models import Category, Tea, Review, UserProfile, SavedTea

# Register models here.
register_model_list = [Category, Tea, Review, UserProfile, SavedTea]
admin.site.register(register_model_list)
