import json
from django.core import serializers
from django.shortcuts import render
from django.contrib.auth import  authenticate, login
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from core.models import Tea, User, UserProfile, Review
from core.models import Category, Tea, Review, UserProfile, SavedTea
from core.forms import UserForm, UserProfileForm

def home(request):
    return render(request, 'tea/home.html')

# def search(request):
#     tea_list = Tea.objects.order_by('-name')[:5]
#     context_dict = {'tea': tea_list}
#     return render(request, 'tea/search.html', context_dict)

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
 
    return render(request, 'tea/search.html', matches)

def faq(request):
    return render(request, 'tea/faq.html')

def teas(request):
    review_list = Review.objects.order_by('-date')[:5]
    context_dict = {'review': review_list}
    return render(request, 'tea/specific_tea.html', context_dict)


def show_account(request):

# i had this in mine but it wasn't fully working    
#     review_list = Review.objects.order_by('-date')[:1]
#     context_dict = {'review': review_list, 'fav': favtea_list}
    
    account = {}
    # TO BE REMOVED 
    # This line is for development purposes only
    # MeghanBright account 
    meghan = "MeghanBright"
    try:
        user = User.objects.get(username=meghan)
        profile = UserProfile.objects.get(user=user)
        reviews = Review.objects.filter(user=user).order_by('date')
        favtea_list = SavedTea.objects.filter(user=user).order_by('-tea')[:5]
        account = {"user": user, "profile": profile, 
        			"reviews": reviews, "favourites": favtea_list}
    except User.DoesNotExist:
        account["user"], account["profile"], account["reviews"],
        account["favourites"] = None

    return render(request, 'tea/account.html', account)


def show_catalog(request):
	context_dict = {}
	try:
		teaList = Tea.objects.order_by('name')
		context_dict["teas"] = teaList
	except Tea.DoesNotExist:
		teaList["teas"] = None

	response = render(request, 'tea/tea_catalog.html', context_dict)
	return response

def most_popular(request):
	if request.method == 'GET':
		teaList = serializers.serialize("json", Tea.objects.order_by('-views'))
		data = {"data": teaList}

	return JsonResponse(data, safe=False)

def register(request):
    # Boolean saying whether registration is successful. False initially.
    registered = False
    
    if request.method == 'POST':
        # Take information from both forms.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
    
        if user_form.is_valid() and profile_form.is_valid():
            # Save user data to database and hash passwrod.
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            # Save userprofil form data, delaying commiting until user foreign key is fileld.
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.profile_pic = request.FILES['picture']
            profile.save()
            
            registered = True
        else:
            # Print problems to the terminal.
            print(user_form.errors, profile_form.errors)
            return HttpResponse("The username or password you entered is wrong.")
    else:
        # Not form submitting, render blank forms isntead.
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'registration/registration_form.html', {'user_form': user_form, 'profile_form': profile_form,'registered': registered})  

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username, password = password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse("Your account is not active")
        else:
            print("Your username or password is wrong")
            return HttpResponse("The username or password you entered is wrong.")
    else:
        return render(request, 'registration/login.html')