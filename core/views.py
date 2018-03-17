import json
from django.core import serializers
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from core.models import Tea, User, UserProfile, Review
from core.models import Category, Tea, Review, UserProfile, SavedTea

def home(request):
    return render(request, 'tea/home.html')

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

def specific_tea(request, tea_name_slug):
    context_dict = {}
    try:
        tea = Tea.objects.get(slug=tea_name_slug)
        tea_review = Review.objects.filter(tea=tea)
        context_dict = {'tea': tea, 'review': tea_review}
    except Tea.DoesNotExist:
        teaList["teas"] = None 
        
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
            model_to_json =  Tea.objects.order_by('category')
    elif request.method == 'POST':
            received_json_data = json.loads(request.body.decode("utf-8"))
            for item in received_json_data["tea_id"]:
               pk_list.append(int(item))
               queryset = Tea.objects.filter(pk__in=pk_list).order_by("category")
               model_to_json = serializers.serialize("json", queryset, fields = ('id', 'name', 'price', 'description', 
                'origin', 'rating', 'temperature', 'category', 'views', 'slug', 'image'))
    
    return JsonResponse(model_to_json, safe=False)

@csrf_exempt
def origin(request):
    response_json_dict = {}
    pk_list = []
    if request.method == 'GET':
            model_to_json =  Tea.objects.order_by('origin')
    elif request.method == 'POST':
            received_json_data = json.loads(request.body.decode("utf-8"))
            for item in received_json_data["tea_id"]:
               pk_list.append(int(item))
               queryset = Tea.objects.filter(pk__in=pk_list).order_by("origin")
               model_to_json = serializers.serialize("json", queryset, fields = ('id', 'name', 'price', 'description', 
                'origin', 'rating', 'temperature', 'category', 'views', 'slug', 'image'))

    return JsonResponse(model_to_json, safe=False)

def user_login(request):
    return render(request, 'registration/login.html')