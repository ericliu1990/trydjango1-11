
from django.conf.urls import include, url

from .views import (
	RestaurantsListView,
	RestaurantsDetailView,
	RestaurantCreateView,
	RestaurantUpdateView,
)

urlpatterns = [

    url(r'^$', RestaurantsListView.as_view(), name='list'),
    url(r'^create$', RestaurantCreateView.as_view(),  name='create'),
    # url(r'^(?P<slug>[\w-]+)/edit/$', RestaurantUpdateView.as_view(), name='edit'),
    url(r'^(?P<slug>[\w-]+)$', RestaurantUpdateView.as_view(), name='detail')
]
