import json
from django.core import serializers
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth import  authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from social_django.models import UserSocialAuth
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from core.models import Category, Tea, Review, UserProfile, SavedTea, User
from django.contrib.auth.decorators import login_required
from core.forms import UserForm, UserProfileForm, ReviewForm

def home(request):
    context_dict = {}
    try:
        tea_image = Tea.objects.order_by('?')[0]
        context_dict = {'tea': tea_image}
    except Tea.DoesNotExist:
        context_dict = None
    return render(request, 'tea/home.html', context_dict)

def search(request):
    matches = {}
    if request.method == 'POST':
    # make client's request lowercase
        query = request.POST.get('query').lower()
        if query != '':
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

def specific_tea(request, tea_name_slug):
    tea_model = None
    context_dict = {}
    try:
        tea_model = Tea.objects.get(slug=tea_name_slug)
        tea_review = Review.objects.filter(tea=tea_model)
        context_dict = {'tea': tea_model, 'review': tea_review, 'is_user_favourite': is_user_favourite(tea_model, request.user) }
    except Tea.DoesNotExist:
        context_dict = None 
        
    if tea_model:
        increment_tea_page_views(tea_model)
    return render(request, 'tea/specific_tea.html', context_dict)


def is_user_favourite(tea_model, user):
        if not user.is_anonymous:
            try:
                is_tea_found = SavedTea.objects.filter(tea=tea_model, user=user).exists()
                if is_tea_found:
                    return True
            except Exception as e:
                return False
        else: 
            return False

        return False



def increment_tea_page_views(tea):
        # Update the tea's number of views by 1
        tea.views += 1
        tea.save()

@login_required
def show_account(request):
    account = {}
    try:
        userReq = request.user
        user = User.objects.get(username=userReq)
        profile = UserProfile.objects.get(user=user)
        reviews = Review.objects.filter(user=user).order_by('date')
        favtea_list = SavedTea.objects.filter(user=user).order_by('tea')[:5]
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

	return render(request, 'tea/tea_catalog.html', context_dict)

@csrf_exempt
def most_popular(request):
    response_json_dict = {}
    pk_list = []
    if request.method == 'GET':
            model_to_json =  Tea.objects.order_by('-views')
    elif request.method == 'POST':
            received_json_data = json.loads(request.body.decode("utf-8"))
            for item in received_json_data["tea_id"]:
               pk_list.append(int(item))
            queryset = Tea.objects.filter(pk__in=pk_list).order_by("-views")
    
    model_to_json = serializers.serialize("json", queryset, fields = ('id', 'name', 'price', 'description', 
                'origin', 'rating', 'temperature', 'category', 'views', 'slug', 'image'))
    
    return JsonResponse(model_to_json, safe=False)

@csrf_exempt
def type(request):
    response_json_dict = {}
    pk_list = []
    if request.method == 'GET':
            context_dict = {}
            context_dict["teas"] = Tea.objects.order_by('category')
            return render(request, 'tea/tea_catalog.html', context_dict)
    elif request.method == 'POST':
            received_json_data = json.loads(request.body.decode("utf-8"))
            for item in received_json_data["tea_id"]:
               pk_list.append(int(item))

            queryset = Tea.objects.filter(pk__in=pk_list).order_by("category")

    model_to_json = serializers.serialize("json", queryset, fields = ('id', 'name', 'price', 'description', 
                'origin', 'rating', 'temperature', 'category', 'views', 'slug', 'image'))
    
    return JsonResponse(model_to_json, safe=False)

@csrf_exempt
def top_rated(request):
    context_dict = {}
    if request.method == 'GET':
            context_dict["teas"] = Tea.objects.order_by('-rating')

    return render(request, 'tea/tea_catalog.html', context_dict)

@csrf_exempt
def recently_reviewed(request):
    response_json_dict = {}
    pk_list = []
    ids = []
    if request.method == 'GET':
            review_list_model = Review.objects.all()
            for o in review_list_model:
                ids.append(int(o.id))
            print(ids)
            queryset = Tea.objects.filter(pk__in=ids)
    elif request.method == 'POST':
            received_json_data = json.loads(request.body.decode("utf-8"))
            for item in received_json_data["tea_id"]:
               pk_list.append(int(item))
            
            review_list_model = Review.objects.filter(pk__in=pk_list).all()
            for o in review_list_model:
                ids.append(int(o.id))
            print(ids)
            queryset = Tea.objects.filter(pk__in=ids)

    model_to_json = serializers.serialize("json", queryset, fields = ('id', 'name', 'price', 'description', 
                'origin', 'rating', 'temperature', 'category', 'views', 'slug', 'image'))
       
    return JsonResponse(model_to_json, safe=False)

@csrf_exempt
def origin(request):
    response_json_dict = {}
    pk_list = []
    if request.method == 'GET':
            context_dict = {}
            context_dict["teas"] = Tea.objects.order_by('origin')
            return render(request, 'tea/tea_catalog.html', context_dict)
    elif request.method == 'POST':
            received_json_data = json.loads(request.body.decode("utf-8"))
            for item in received_json_data["tea_id"]:
               pk_list.append(int(item))
            
            queryset = Tea.objects.filter(pk__in=pk_list).order_by("origin")

    model_to_json = serializers.serialize("json", queryset, fields = ('id', 'name', 'price', 'description', 
                'origin', 'rating', 'temperature', 'category', 'views', 'slug', 'image'))

    return JsonResponse(model_to_json, safe=False)

@login_required 
def add_review(request):
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return reviews(request)
        else:
            print(form.errors)

    return render(request, 'tea/specific_tea.html', {'form': form})

@login_required 
def add_favourite_tea(request): 
    tea_id = None
    if request.method == 'GET':
        tea_id = request.GET['tea_id'] 
        if tea_id:
            tea_model = Tea.objects.get(id = int(tea_id)) 
            if tea_model: 
                userReq = request.user
                user_model = User.objects.get(username=userReq)
                fav = SavedTea.objects.get_or_create(user=user_model,tea=tea_model)[0]
                fav.user=user_model
                fav.tea=tea_model
                fav.save()

    return HttpResponse(201)

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

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required
def account_settings(request):
    user = request.user

    try:
        twitter_login = user.social_auth.get(provider='twitter')
    except UserSocialAuth.DoesNotExist:
        twitter_login = None
    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None
    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    return render(request, 'tea/account.html', {'twitter_login': twitter_login, 'facebook_login': facebook_login, 'can_disconnect': can_disconnect})

@login_required
def manage_password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm
    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect(reverse('password'))
        else:
            messages.error(request, 'Invalid Password Provided')
    else:
        form = PasswordForm(request.user)
    return render(request, 'registration/password.html', {'form': form})

def contact_us(request):
    return render(request, 'tea/contact_us.html')