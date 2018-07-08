from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, View, CreateView
from django.contrib.auth import get_user_model
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin 

from restaurants.models import RestaurantLocation
from menus.models import Items
# Create your views here.

from .forms import RegisterForm
from .models import Profile

User = get_user_model()

class RegisterView(CreateView):
	form_class = RegisterForm
	template_name = 'registration/register.html'
	success_url = '/'

	def dispatch(self, *args, **kwargs):
		# if self.request.user.is_authenticated():
		# 	return redirect("/logout")
		return super(RegisterView, self).dispatch(*args, **kwargs)

#create a template tag filter after creating the in point
class ProfileFollowToggle(LoginRequiredMixin, View):
	def post(self, request, *args, **kwargs):
		#print(request.data)
		# print(request.POST)
		username_to_toggle = request.POST.get("username")

		_profile, is_following = Profile.objects.toggle_follow(request.user, username_to_toggle)

		# print(user_to_toggle)
		# _profile = Profile.objects.get(user__username__iexact=user_to_toggle)
		# user = request.user
		# if user in _profile.followers.all():
		# 	_profile.followers.remove(user)
		# else:
		# 	_profile.followers.add(user)

		return redirect(f"/profile/{_profile.user.username}")

class ProfileDetailsView(DetailView):
	queryset = User.objects.filter(is_active=True)
	template_name  = 'profiles/user.html'

	def get_object(self):
		username = self.kwargs.get("username")
		if username is None:
			 raise Http404
		return get_object_or_404(User, username__iexact=username, is_active=True)

	def get_context_data(self, *args, **kwargs):
		context = super(ProfileDetailsView,self).get_context_data(*args,**kwargs)
		user = context['user']
		#check whether the requested user is following the user in profile
		is_following = False
		if user.profile in self.request.user.is_following.all():
			is_following=True
		context['is_following'] = is_following

		query = self.request.GET.get('q')
		
		item_exists = Items.objects.filter(user=user).exists()
		qs = RestaurantLocation.objects.filter(owner=user).search(query)
		# if query: #this part has been moved to models.py under restaurants
		# 	qs = qs.search(query)
			#qs = RestaurantLocation.objects.search(query)
		if item_exists and qs.exists():
			context['locations'] = qs
		return context