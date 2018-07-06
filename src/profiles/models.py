from django.db import models
from django.conf import settings
from django.db.models.signals import post_save

User = settings.AUTH_USER_MODEL

# Create your models here.
class Profile(models.Model):
	user 		= models.OneToOneField(User) #user.profile
	followers	= models.ManyToManyField(User, related_name='is_following', blank='True') # user.followers
	#following	= models.ManyToManyField(User, related_name='following', blank='True') # user.following
	activated	= models.BooleanField(default=False)
	timestamp	= models.DateTimeField(auto_now_add=True)
	update 		= models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.user.username


def post_save_user_reveiver(sender, instance, created, *args, **kwargs):
	if created:
		profile, is_created  = Profile.objects.get_or_create(user=instance)
		default_user_profile = Profile.objects.get_or_create(user__id=1)[0] #user__username=''
		#newly created user profile and the first user will be followed each other
		default_user_profile.followers.add(instance)
		profile.followers.add(default_user_profile.user)
		#profile.followers.add(2)

post_save.connect(post_save_user_reveiver, sender=User)