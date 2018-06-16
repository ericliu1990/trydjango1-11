import random
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.views.generic.base import TemplateView
# Create your views here.
# function based view 
# def home(request):
# 	html_var = 'f strings'
# 	html_= f"""<!DOCTYPE html>
# 	<html lang=en>
# 	<head>
# 	</head>
# 	<body>
# 	<h1>Hello World!</h1>
# 	<p>This is {html_var} coming through</p>
# 	</body>
# 	</html>

# 	"""
# 	#f strings 

# 	return HttpResponse(html_)
# 	#render(request, "template", {context of the template})#response
# 	#return render(request, "home.html", {})#response

def home(request):
	num = random.randint(0,10000);
	some_list = [num, random.randint(0,100000), random.randint(0,100000)]
	context = {
		"html_var":"context variable", 
		"random_num":num, 
		"bool_item":True,
		"some_list":some_list
	}
	return render(request, "home.html", context)#response

def about(request):
	context = {
	}
	#redering a template
	return render(request, "about.html", context)#response

def contact(request):
	context = {
	}
	return render(request, "contact.html", context)#response

# class ContactView(View):
# 	def get(self, request, *args, **kwargs):  
# 		print(kwargs) #it will print out the  number of the url from url(r'^contact/(?P<Id>\d+)$', ContactView.as_view()),
# 		context = {}
# 		return render(request, "contact.html", context) 

class HomeView(TemplateView):
	template_name = 'home.html'
	#overwirite the predefined method
	def get_context_data(self, *args, **kwargs):
		context = super(HomeView, self).get_context_data(*args, **kwargs)
		#print(context)
		num = random.randint(0,10000);
		some_list = [num, random.randint(0,100000), random.randint(0,100000)]
		context = {
			"html_var":"context variable", 
			"random_num":num, 
			"bool_item":True,
			"some_list":some_list
		}
		return context

# the following two parts can be replaced by using the following url config in urls.py
# url(r'^about$', TemplateView.as_view(template_name='about.html')),
# url(r'^contact$', TemplateView.as_view(template_name='contact.html'))
# class AboutView(TemplateView):
# 	template_name = 'about.html'

# class ContactView(TemplateView):
# 	template_name = 'contact.html'



	# def post(self, request, *args, **kwargs):
	# 	print(kwargs)
	# 	context = {}
	# 	return render(request, "contact.html", context) 
	# def put(self, request, *args, **kwargs):
	# 	print(kwargs)
	# 	context = {}
	# 	return render(request, "contact.html", context) 

from .models import RestaurantLocation
from django.views.generic import ListView, DetailView
from django.db.models import Q

def restaurant_listview(request):
	template_name = 'restaurants/restaurants_list.html'
	queryset = RestaurantLocation.objects.all()
	context = {
		"object_list":queryset
	}
	return render(request, template_name, context)

class RestaurantsListView(ListView):
	def get_queryset(self):
		print (self.kwargs)
		slug = self.kwargs.get("slug")
		if slug:
			queryset = RestaurantLocation.objects.filter(
				Q(category__iexact=slug) | Q(category__icontains=slug))
		else:
			queryset = RestaurantLocation.objects.all()
		return queryset


# class MexicanRestaurantsListView(ListView):
# 	template_name = 'restaurants/restaurants_list.html'
# 	queryset = RestaurantLocation.objects.filter(category__iexact='west')

# class AsianRestaurantsListView(ListView):
# 	template_name = 'restaurants/restaurants_list.html'
# 	queryset = RestaurantLocation.objects.filter(category__iexact='chicken')

class SearchRestaurantsListView(ListView):
	#it will use the default <model name>_list.html as template
	def get_queryset(self):
		print (self.kwargs)
		slug = self.kwargs.get("slug")
		if slug:
			queryset = RestaurantLocation.objects.filter(
				Q(category__iexact=slug) | Q(category__icontains=slug))
		else:
			queryset = RestaurantLocation.objects.none
		return queryset


class RestaurantsDetailView(DetailView):
	queryset = RestaurantLocation.objects.all()
	# def get_context_data(self, *args, **kwargs):
	# 	print(self.kwargs)
	# 	context=super(RestaurantsDetailView, self).get_context_data(*args, **kwargs)
	# 	print(context)
	# 	return context

	# def get_object(self, *args, **kwargs):
	# 	rest_id = self.kwargs.get('rest_id')
	# 	obj = get_object_or_404(RestaurantLocation, id=rest_id) # pk = rest_id
	# 	return obj