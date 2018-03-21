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
	#ratings = GenericRelation(Rating, related_query_name='reviews')
	user = models.ForeignKey(User,
		on_delete = models.CASCADE, null=True)
	tea = models.ForeignKey(Tea,
		on_delete = models.CASCADE, related_name='reviews', null=True)
	slug = models.SlugField(unique=True)

	def save(self, *args, **kwargs): 
		slug_str = "%s %s" % ( self.date, self.rating) 
		self.slug = slugify(slug_str)
		super(Review, self).save(*args, **kwargs)

	def __str__(self):
		return str(self.tea)
#Review.objects.filter(ratings__isnull=False).order_by('ratings__average')

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
		return str(self.user)

@receiver(post_save)
def callback(sender, **kwargs):

    if kwargs['created']:
    	r = kwargs['instance']
    	if (isinstance(r, Review)):
    		try:
    			r.tea.update_rating()
    		except Exception as e:
		    	print('fail')
		    	print(e)