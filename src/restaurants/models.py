from django.db import models
from django.db.models.signals import pre_save, post_save
from django.conf import settings

from .utils import unique_slug_generator
from .validators import validate_category

from django.core.urlresolvers import reverse
from django.db.models import Q

Users = settings.AUTH_USER_MODEL

# Create your models here.
class RestaurantLocationQuerySet(models.query.QuerySet):
	def search(self,query):
		#RestaurantLocation.objects.all().search(query)
		#RestaurantLocation.objects.filter(something).search()
		if query:
			query=query.strip()
			return self.filter(
				Q(name__icontains=query)|
				Q(location__icontains=query)|
				Q(category__icontains=query)|
				Q(items__name__icontains=query)|
				Q(items__contents__icontains=query)
				).distinct()
		else:
			return self

class RestaurantLocationManager(models.Manager):
	def get_queryset(self):
		return RestaurantLocationQuerySet(self.model,using=self._db)

	def search(self,query): #RestaurantLocation.objects.search()
		return self.get_queryset().search(query)

#models.model --> derive from models
class RestaurantLocation(models.Model): 
	owner 		= models.ForeignKey(Users) #class_instance.model_set.all()  # Django Models Unleashed JOINCFE.com
	name 		= models.CharField(max_length=120)
	location 	= models.CharField(max_length=120, null=True, blank=True)
	category 	= models.CharField(max_length=120, null=True, blank=True, validators=[validate_category])
	timestamp	= models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
	update 		= models.DateTimeField(auto_now_add=True)
	slug		= models.SlugField(null=True, blank=True)

	objects = RestaurantLocationManager() #add Model.objects.all()

	def __str__(self):
		return self.name

	@property
	def title(self):
		return self.name

	def get_absolute_url(self):
		return reverse('restaurants:detail', kwargs={'slug': self.slug})
	

def rl_pre_save_receiver(sender, instance, *args, **kwargs):
	print ('saving..')
	print(instance.timestamp)
	instance.name = instance.name.capitalize()
	if not instance.slug:
	 	instance.slug = unique_slug_generator(instance)


# def rl_post_save_receiver(sender, instance, *args, **kwargs):
# 	print ('saved')
# 	print(instance.timestamp)
# 	#avoid save instance in post
# 	if not instance.slug:
# 		instance.slug = unique_slug_generator(instance)
# 		instance.save()

pre_save.connect(rl_pre_save_receiver, sender=RestaurantLocation)
# pre_save.connect(rl_post_save_receiver, sender=RestaurantLocation)