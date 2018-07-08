from django.shortcuts import render
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView
# Create your views here.
from .models import Items
from .forms import ItemsForm
from django.contrib.auth.mixins import LoginRequiredMixin 

class HomeView(LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return render(request, "home.thml", {})
		else:
			user = self.request.user
			is_following_user_id = [x.user.id for x in user.is_following.all()] 
			qs = Items.objects.filter(user__id__in = is_following_user_id, public=True).order_by("-updated")[:10] #first 3 latest

			return render(request, "menus/home-feed.html", {'object_list':qs})

class ItemsListView(LoginRequiredMixin, ListView):
	def get_queryset(self):
		return Items.objects.filter(user=self.request.user)

class ItemsDetailView(LoginRequiredMixin, DetailView):
	def get_queryset(self):
		return Items.objects.filter(user=self.request.user)

class ItemsCreateView(LoginRequiredMixin, CreateView):
	template_name = 'form.html'
	form_class = ItemsForm

	def get_queryset(self):
		return Items.objects.filter(user=self.request.user)

	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.user = self.request.user #anonymousUser
		#instance.save()
		return super(ItemsCreateView, self).form_valid(form)

	def get_context_data(self, *args, **kwargs):
		context = super(ItemsCreateView, self).get_context_data(*args, **kwargs)
		context['title'] = 'Create Item'
		return context

	#get args that passed into form_class
	def get_form_kwargs(self):
		kwargs = super(ItemsCreateView, self).get_form_kwargs()
		kwargs['user']=self.request.user
		# kwargs['instance']=Items.objects.filter(user=self.request.user).first()
		return kwargs 

class ItemsUpdateView(LoginRequiredMixin, UpdateView):
	template_name = 'menus/detail-update.html'
	form_class = ItemsForm

	def get_queryset(self):
		return Items.objects.filter(user=self.request.user)

	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.user = self.request.user #anonymousUser
		#instance.save()
		return super(ItemsUpdateView, self).form_valid(form)

	def get_context_data(self, *args, **kwargs):
		context = super(ItemsUpdateView, self).get_context_data(*args, **kwargs)
		context['title'] = 'Update Item'
		return context

	def get_form_kwargs(self):
		kwargs = super(ItemsUpdateView, self).get_form_kwargs()
		kwargs['user']=self.request.user
		# kwargs['instance']=Items.objects.filter(user=self.request.user).first()
		return kwargs 