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
    content = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'placeholder': 'Leave a review'}))
    rating = forms.IntegerField(initial=0)
    date = forms.DateTimeField(widget=forms.HiddenInput(), disabled=True)
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput(), disabled=True)
    tea = forms.ModelChoiceField(queryset=Tea.objects.all(), widget=forms.HiddenInput(), disabled=True)
    slug = forms.CharField(widget=forms.HiddenInput(), required =False)

    class Meta:
        model = Review
        fields = ('content',
                  'rating',
                  'date',)