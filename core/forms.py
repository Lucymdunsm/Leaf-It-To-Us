# Review class 
from django import forms
from django.contrib.auth.models import User
from core.models import UserProfile, Review, User, Tea
from datetime import datetime

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('profile_pic',)

class ReviewForm(forms.ModelForm):
    content = forms.CharField(max_length=500,
							error_messages={'required': 'is missing, please enter your review'},
							widget=forms.Textarea(attrs={'placeholder': 'Leave a review', 'cols': 70, 'rows': 5}))
    rating = forms.IntegerField(initial=0,
							error_messages={'required': 'is missing, please try again'})

    class Meta:
        model = Review
        fields = ('content',
                  'rating',)