from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
# Create your views here.
from .models import Items
from .forms import ItemsForm

class ItemsListView(ListView):
	def get_queryset(self):
		return Items.objects.filter(user=self.request.user)

class ItemsDetailView(DetailView):
	def get_queryset(self):
		return Items.objects.filter(user=self.request.user)

from django.contrib.auth.mixins import LoginRequiredMixin

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