from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'tea/base.html') #have this direct to home once that's been made

def search(request):
    return render(request, 'tea/search.html')

def faq(request):
    return render(request, 'tea/faq.html')

def teas(request):
    return render(request, 'tea/teas.html')