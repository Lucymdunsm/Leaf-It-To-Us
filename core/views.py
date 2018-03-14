from django.shortcuts import render
from django.http import HttpResponse

from core.models import Category, Tea, Review, UserProfile, SavedTea


def home(request):
    return render(request, 'tea/home.html')

def search(request):
    tea_list = Tea.objects.order_by('-name')[:5]
    context_dict = {'tea': tea_list}
    return render(request, 'tea/search.html', context_dict)

def faq(request):
    return render(request, 'tea/faq.html')

def teas(request):
    review_list = Review.objects.order_by('-date')[:5]
    context_dict = {'review': review_list}
    return render(request, 'tea/teas.html', context_dict)

def show_account(request):
    review_list = Review.objects.order_by('-date')[:1]
    favtea_list = SavedTea.objects.order_by('-tea')[:5]
    context_dict = {'review': review_list, 'fav': favtea_list}
    return render(request, 'tea/profile.html', context_dict)