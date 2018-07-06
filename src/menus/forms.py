from django import forms 
from .models import Items
from restaurants.models import RestaurantLocation

class ItemsForm(forms.ModelForm):
	class Meta:
		model = Items
		fields = [
			'restaurant',
			'name',
			'contents',
			'excludes',
			'public'
		]

	def __init__(self, user=None, *args, **kwargs):
		print(user)
		# print(kwargs.pop('instance'))
		print(kwargs)
		super(ItemsForm, self).__init__(*args, **kwargs)
		self.fields['restaurant'].queryset = RestaurantLocation.objects.filter(owner=user)#.exclude(items__isnull=False)