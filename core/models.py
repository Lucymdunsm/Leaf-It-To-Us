from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.db.models import Avg
from django.db.models.signals import post_save
from django.dispatch import receiver

class Category(models.Model):
	name = models.CharField(max_length=128)
	description = models.TextField()

	def __str__(self):
		return self.name


class Tea(models.Model):
	name = models.CharField(max_length=200)
	price = models.FloatField(default=0)
	description = models.TextField()
	origin = models.CharField(max_length=200)
	rating = models.FloatField(default=0)
	temperature = models.FloatField(default=0)
	category = models.ForeignKey(Category, on_delete = models.CASCADE, null=True)
	views = models.IntegerField(default=0)
	slug = models.SlugField(unique=True)
	image = models.ImageField(upload_to='tea_images', blank=True)

	def update_rating(self):
		print("updating rating..")
		print("yes")
		avg_ratings = self.reviews.aggregate(Avg('rating'))['rating__avg']
		self.rating = avg_ratings
		self.save()


		class Meta:
	  		model = Tea
	  		fields = ('id', 'name', 'price', 'description', 
	        	'origin', 'rating', 'temperature', 'category', 'views', 'slug', 'image')

	def __str__(self):
		return self.name


class Review(models.Model):
	content = models.TextField()
	rating = models.FloatField(default=0)
	date = models.DateField(default=timezone.now)
	user = models.ForeignKey(User,
		on_delete = models.CASCADE, null=True)
	tea = models.ForeignKey(Tea,
		on_delete = models.CASCADE, related_name='reviews', null=True)
	slug = models.SlugField(unique=True)

	def __str__(self):
		return self.tea


class SavedTea(models.Model):
	user = models.ForeignKey(User,
		on_delete = models.CASCADE,
		null=True
	)
	tea = models.ForeignKey(
		Tea, 
		on_delete = models.CASCADE,
		null=True
	)

	def __str__(self):
		return self.user + self.tea
	

class UserProfile(models.Model):
	user = models.OneToOneField(User,
		on_delete = models.CASCADE,
	)
	profile_pic = models.ImageField(upload_to='profile_images',
		default="profile_images/default.png",
		blank=True,
		null=True
	)

	def __str__(self):
		return self.user

@receiver(post_save)
def callback(sender, **kwargs):
    r = kwargs['instance']

    if (isinstance(r, Review)):
    	# if kwargs['created']:
	    	try:
	    		r.tea.update_rating()
	    	except Exception as e:
	    		print('fail')
	    		print(e)

# work around for adding User profiles automatically

def create_profile(sender,**kwargs ):
    if kwargs['created']:
        user_profile=UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile,sender=User)