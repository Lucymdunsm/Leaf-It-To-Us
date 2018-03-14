import json
from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from core.models import Tea, User, UserProfile

from core.models import Category, Tea, Review, UserProfile, SavedTea


def home(request):
    return render(request, 'tea/home.html')

<<<<<<< HEAD
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
=======
def faq(request):
    return render(request, 'tea/faq.html')

def show_catalog(request):
	context_dict = {}
	try:
		teaList = Tea.objects.order_by('name')
		context_dict["teas"] = teaList
	except Tea.DoesNotExist:
		teaList["teas"] = None

	response = render(request, 'tea/catalog.html', context_dict)
	return response

def most_popular(request):
	context_dict = {}
	if request.method == 'GET':
		try:
			teaList = Tea.objects.order_by('-views')
			context_dict["teas"] = teaList
		except Tea.DoesNotExist:
			teaList["teas"] = None
			context_dict["teas"] = teaList

	Tea_json = serializers.serialize("json", teaList)
	data = {"data": Tea_json}
	return JsonResponse(data)

def search(request):
	matches = {}
	if request.method == 'POST':
	# make client's request lowercase
		query = request.POST.get('query').lower()
		print(query)
		try:
		# interface with db
			results = Tea.objects.filter(name__icontains=query)
			matches["results"] = results 
		except Tea.DoesNotExist:
		# Execption, return nothing
			matches["results"] = None

	print(matches["results"])
	return render(request, 'tea/search.html', matches)

def show_account(request):
	account = {}
	# TO BE REMOVED 
	# This line is for development purposes only
	# MeghanBright account 
	meghan = "MeghanBright"
	try:
		user = User.objects.get(username=meghan)
		profile = UserProfile.objects.get(user=user)
		account = {"user": user, "profile": profile}
	except User.DoesNotExist:
		account = {"user": None, "profile": None}

	return render(request, 'tea/account.html', account)
>>>>>>> 87b51f68ffcfa115214cf234443868f368128a18
