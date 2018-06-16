from django.db import models
from django.db.models.signals import pre_save, post_save
from .utils import unique_slug_generator


# Create your models here.

#models.model --> derive from models
class RestaurantLocation(models.Model): 
	name 		= models.CharField(max_length=120)
	location 	= models.CharField(max_length=120, null=True, blank=True)
	category 	= models.CharField(max_length=120, null=True, blank=True)
	timestamp	= models.DateTimeField(auto_now=False, auto_now_add=False)
	update 		= models.DateTimeField(auto_now_add=True)
	slug		= models.SlugField(null=True, blank=True)

	def __str__(self):
		return self.name

	@property
	def title(self):
		return self.name
	

def rl_pre_save_receiver(sender, instance, *args, **kwargs):
	print ('saving..')
	print(instance.timestamp)
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