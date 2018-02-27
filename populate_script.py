import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
	'leaf_it_to_us.settings')

import django
django.setup()
from django.contrib.auth.models import User
from core.models import Tea, Review, SavedTea, Category, UserProfile
from django.contrib.auth.hashers import make_password
from django.utils import timezone

def populate_users():
    print("Populating users...")

    users = [
        {
            "username": "admin",
            "first_name": "",
            "last_name": "",
            "email": "",
            "password": make_password("admin"),
            "is_staff": True,
            "is_admin": True,
            "is_superuser": True
        },
        {
            "username": "BobbyRenson",
            "first_name": "Bobby",
            "last_name": "Renson",
            "email": "bobby@example.com",
            "password": make_password("test"),
            "is_staff": False,
            "is_admin": False,
            "is_superuser": False
        },
        {
            "username": "MeghanBright",
            "first_name": "Meghan",
            "last_name": "Bright",
            "email": "meghan@example.com",
            "password": make_password("test"),
            "is_staff": False,
            "is_admin": False,
            "is_superuser": False

        },
        {
            "username": "VictoireVert",
            "first_name": "Victoire",
            "last_name": "Vert",
            "email": "victoire@example.com",
            "password": make_password("test"),
            "is_staff": False,
            "is_admin": False,
            "is_superuser": False
        }
    ]

    for data in users:
        user, created = User.objects.get_or_create(username=data['username'])

        if created:
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.email = data['email']
            user.password = data['password']
            user.is_staff = data['is_staff']
            user.is_admin = data['is_admin']
            user.is_superuser = data['is_superuser']
            user.save()

            profile = UserProfile(
                user=User.objects.get(username=data['username']),
                profile_pic="profile_images/" + data['username'].lower() + "-profile.jpg"
            )
            profile.save()

def populate_categories():
	print("Populating categories...")

	categories = [
		{'name': 'Black', 'description': 'Generally stronger in flavour than the less oxidized teas'},
		{'name': 'Green', 'description': 'Green tea is a type of tea that is made from Camellia sinensis leaves that have not undergone the same withering and oxidation process used to make oolong teas and black teas' },
		{'name': 'Oolong', 'description':'Oolong is a traditional Chinese tea produced through a process including withering the plant under strong sun and oxidation before curling and twisting'},
		]

	for cat in categories:
		add_category(cat['name'], cat['description'])

# ratings needs to be an average sum 

def populate_teas():
	print("Populating teas...")
	black_cat = Category.objects.get(name="Black")
	green_cat = Category.objects.get(name="Green")
	some_teas = [
			{'name': 'Breakfast Tea','price':4.40, 'description':'Traditional Breakfast Tea', 'origin':'Kenya',
			'temperature': 55.3, 'category': black_cat, 'views': 202, 'slug': 'breakfast-tea', 'image': 'tea_images/breakfast_tea.jpg'},
			{
			'name': 'Moroccan Mint',
			'price':8.20,
			'description': 'Traditionally a blend of Chinese Gunpowder green tea and fresh mint leaves',
			'origin': 'morocco',
			'temperature': 65.5,
			'category':green_cat,
			'views': 67,
			'slug': 'moroccan-mint',
			'image': 'tea_images/moroccan_tea.jpg'
			},
			{'name': 'Darjeeling First Flush',
			'price': 12.40,
			'description': 'Made from the most fresh leaves and available in black, green, white, and oolong.',
			'origin': 'India',
			'temperature': 90, 'category': black_cat, 'views': 109, 'slug': 'darjeeling',
			'image': 'tea_images/darjeeling.jpg'},
			{'name': 'Arctic Fire', 'price': 5.20,
			 'description': 'Scented black tea with cornflowers',
			 'origin': 'China',
			 'temperature': 92, 'category': black_cat, 'views': 87, 'slug': 'arctic-fire',
			 'image': 'tea_images/arctic_fire.jpg'},
			{'name': 'Caramel Tea', 'price': 7.90,
			 'description': 'Scented black tea',
			 'origin': 'China',
			 'temperature': 92, 'category': black_cat, 'views': 56, 'slug': 'caramel',
			 'image': 'tea_images/caramel.jpg'},
			{'name': 'Organic Jasmin', 'price': 10.00,
			 'description': 'Glorious scented green tea',
			 'origin': 'China',
			 'temperature': 80, 'category': green_cat, 'views': 188, 'slug': 'organic-jasmin',
			 'image': 'tea_images/organic_jasmin.jpg'},
			{'name': 'Sencha', 'price': 10.00,
			 'description': 'Tea that brings a lot of health benefits',
			 'origin': 'China',
			 'temperature': 60, 'category': green_cat, 'views': 188, 'slug': 'sencha',
			 'image': 'tea_images/sencha.jpg'},
			{'name': 'Earl grey', 'price': 6.40,
			 'description': 'Tea blend flavoured with oil of bergamot',
			 'origin': 'China',
			 'temperature': 100, 'category': black_cat, 'views': 122, 'slug': 'earl-grey',
			 'image': 'tea_images/earl_grey.jpg'},
			{'name': 'Mate IQ', 'price': 4.80,
			 'description': 'Stimulating and great for digestion',
			 'origin': 'Argentina',
			 'temperature': 90, 'category': green_cat, 'views': 74, 'slug': 'mate',
			 'image': 'tea_images/mate.jpg'},
			{
			'name': 'Genmai Cha', 'price': 9.40,
			 'description': 'Popcorn tea good to drink all day long',
			 'origin': 'Japan',
			 'temperature': 82, 'category': green_cat, 'views': 102, 'slug': 'genmai-cha',
			 'image': 'tea_images/genmai_cha.jpg'
			 },
		]
	# name, price, description, origin, temperature, category, views, slug, image
	for tea in some_teas:
		add_tea(
			tea['name'], 
			tea['price'], 
			tea['description'],
			tea['origin'],
			tea['temperature'],
			tea['category'],
			tea['views'],
			tea['slug'],
			tea['image']
		)

def populate_reviews():
	print("Populating reviews...")

	bobby = User.objects.get(username="BobbyRenson")
	meghan = User.objects.get(username="MeghanBright")

	breakfast = Tea.objects.get(name="Breakfast Tea")
	moroccan = Tea.objects.get(name="Moroccan Mint")

	reviews = [
		{'content':'This tea changed my life!', 'rating': 5.0, 'date': timezone.now(), 
		'user': bobby,'tea': moroccan, 'slug': 'review-{}-{}'.format(bobby.username, moroccan.name).lower().replace(' ', '-')},
		{'content':'I hate this kind of tea!', 'rating':1.0, 'date': timezone.now(), 
		'user':meghan,'tea': breakfast, 'slug': 'review-{}-{}'.format(meghan.username, breakfast.name).lower().replace(' ', '-')}
	]	

	for rvw in reviews:
		add_review(
			rvw['content'], 
			rvw['rating'], 
			rvw['date'],
			rvw['user'],
			rvw['tea'],
			rvw['slug']
	)

def populate_savedTeas():

	bobby = User.objects.get(username="BobbyRenson")
	meghan = User.objects.get(username="MeghanBright")
	victoire = User.objects.get(username="VictoireVert")

	breakfast = Tea.objects.get(name="Breakfast Tea")
	moroccan = Tea.objects.get(name="Moroccan Mint")

	saved_teas = [
	{
	'user': victoire,
	'tea': breakfast
	},
	{
	'user': bobby,
	'tea': moroccan
	},
	{
	'user': meghan,
	'tea': moroccan
	},
	]

	for st in saved_teas:
		add_savedTea(
			st['user'],
			st['tea'],
		)


def populate():
	populate_users()
	populate_categories()
	populate_teas()
	populate_reviews()
	populate_savedTeas()
	print("db populate successful")


def add_category(name, description):
	c = Category.objects.get_or_create(name=name)[0]
	c.name=name
	c.description=description
	c.save()
	return c	

def add_tea(name, price, description, origin, temperature, category, views, slug, image):
	t = Tea.objects.get_or_create(name=name,origin=origin,slug=slug)[0]
	t.name=name
	t.price=price
	t.description=description
	t.origin=origin
	t.temperature=temperature
	t.views=views
	t.slug=slug
	t.image=image
	t.category=category

	t.save()
	return t

def add_review(content,rating,date,user,tea,slug):
	r = Review.objects.get_or_create(date=date,user_id=user.id)[0]
	r.content=content
	r.rating=rating
	r.date=date
	r.user=user
	r.tea=tea
	r.slug=slug

	r.save()
	return r

def add_savedTea(user, tea):
	s = SavedTea.objects.get_or_create(user=user,tea=tea)[0]
	s.user=user
	s.tea=tea
	s.save()
	return s


if __name__=='__main__':
	print('Starting Rango population script...')
	populate()