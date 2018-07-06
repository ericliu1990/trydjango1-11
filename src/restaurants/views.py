import random
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.views.generic.base import TemplateView

from django.contrib.auth.decorators import login_required


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
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.db.models import Q

from .forms import RestaurantCreateForm,RestaurantLocationCreateForm

from django.contrib.auth.mixins import LoginRequiredMixin # use for class based views

def restaurant_createview(request):

	# if request.method == "GET":
	# 	print("get data")
	# 	print(request.GET)
	form = RestaurantLocationCreateForm(request.POST or None)
	errors = None
	#if request.method == "POST": #PUT
		# print("post data")
		# print(request.POST)
		# title = request.POST.get("title") # can use request.POST["title"] as well, but .get("title") means the value can be empty
		# location = request.POST.get("location")
		# cat = request.POST.get("category")

		#form = RestaurantCreateForm(request.POST)
	if(form.is_valid()):
		# obj = RestaurantLocation.objects.create(
		# 		name=form.cleaned_data.get('name'),
		# 		location=form.cleaned_data.get('location'),
		# 		category=form.cleaned_data.get('category')
		# 	)
		form.save()
		return HttpResponseRedirect("/restaurants")
	if form.errors:
		#print(form.errors)
		errors = form.errors

	template_name = 'restaurants/form.html'
	context = {
		"form":form, "errors":errors
	}
	return render(request, template_name, context)

@login_required(login_url='/login')
def restaurant_FBV_createview(request):

	# if request.method == "GET":
	# 	print("get data")
	# 	print(request.GET)
	form = RestaurantLocationCreateForm(request.POST or None)
	errors = None
	if(form.is_valid()):
		if request.user.is_authenticated():
			instance = form.save(commit=False)
			instance.owner = request.user
			instance.save()
			return HttpResponseRedirect("/restaurants")
		else:
			return HttpResponseRedirect("/login")
	if form.errors:
		errors = form.errors

	template_name = 'restaurants/form.html'
	context = {
		"form":form, "errors":errors
	}
	return render(request, template_name, context)

def restaurant_listview(request):
	template_name = 'restaurants/restaurants_list.html'
	queryset = RestaurantLocation.objects.all()
	context = {
		"object_list":queryset
	}
	return render(request, template_name, context)

# class RestaurantsListView(ListView):
# 	def get_queryset(self):
# 		print (self.kwargs)
# 		slug = self.kwargs.get("slug")
# 		if slug:
# 			queryset = RestaurantLocation.objects.filter(
# 				Q(category__iexact=slug) | Q(category__icontains=slug))
# 		else:
# 			queryset = RestaurantLocation.objects.all()
# 		return queryset

class RestaurantsListView(LoginRequiredMixin, ListView):
	def get_queryset(self):
		return RestaurantLocation.objects.filter(owner=self.request.user)

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

# class RestaurantsDetailView(DetailView):
# 	#Define RestaurantsDetailView.model, 
# 	#RestaurantsDetailView.queryset, 
# 	#or override RestaurantsDetailView.get_queryset().

# 	# Generic detail view RestaurantsDetailView must be called with either an object pk or a slug.

# 	queryset = RestaurantLocation.objects.all()
# 	# def get_context_data(self, *args, **kwargs):
# 	# 	print(self.kwargs)
# 	# 	context=super(RestaurantsDetailView, self).get_context_data(*args, **kwargs)
# 	# 	print(context)
# 	# 	return context

# 	# def get_object(self, *args, **kwargs):
# 	# 	rest_id = self.kwargs.get('rest_id')
# 	# 	obj = get_object_or_404(RestaurantLocation, id=rest_id) # pk = rest_id
# 	# 	return obj

class RestaurantsDetailView(LoginRequiredMixin, DetailView):
	def get_queryset(self):
		return RestaurantLocation.objects.filter(owner=self.request.user)


class RestaurantCreateView(LoginRequiredMixin, CreateView):
	form_class = RestaurantLocationCreateForm
	template_name = 'form.html'

	# replaced by ger_absolute_url method from models.py
	#success_url = "/restaurants";
	
	#cutimize login page name
	#login_url = '/newlogin'

	#Create view will run the form_valid method by default 
	#in the form_valid it will do form.save() by default
	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.owner = self.request.user #anonymousUser
		#instance.save()
		return super(RestaurantCreateView, self).form_valid(form)

	def get_context_data(self, *args, **kwargs):
		context = super(RestaurantCreateView, self).get_context_data(*args, **kwargs)
		context['title'] = 'Add Restaurant'
		return context

class RestaurantUpdateView(LoginRequiredMixin, UpdateView):
	form_class = RestaurantLocationCreateForm
	template_name = 'restaurants/detail-update.html'

	#no need to validate the user which has been done during the create
	def get_context_data(self, *args, **kwargs):
		context = super(RestaurantUpdateView, self).get_context_data(*args, **kwargs)
		name = self.get_object().name
		context['title'] = f'Update { name }'
		return context

	def get_queryset(self):
		return RestaurantLocation.objects.filter(owner=self.request.user)