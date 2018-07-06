from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from django.contrib.auth import get_user_model
from django.http import Http404


from restaurants.models import RestaurantLocation
from menus.models import Items
# Create your views here.

User = get_user_model()

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
		query = self.request.GET.get('q')
		
		item_exists = Items.objects.filter(user=user).exists()
		qs = RestaurantLocation.objects.filter(owner=user).search(query)
		# if query: #this part has been moved to models.py under restaurants
		# 	qs = qs.search(query)
			#qs = RestaurantLocation.objects.search(query)
		if item_exists and qs.exists():
			context['locations'] = qs
		return context