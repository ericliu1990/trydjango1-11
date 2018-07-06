
from django.conf.urls import include, url

from .views import (
	ItemsListView,
	ItemsDetailView,
	ItemsUpdateView,
	ItemsCreateView,

)

urlpatterns = [

    url(r'^create$', ItemsCreateView.as_view(),  name='create'),
    # url(r'^(?P<pk>\d+)/edit$', ItemsUpdateView.as_view(), name='edit'),
    # url(r'^(?P<pk>\d+)$', ItemsDetailView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)$', ItemsUpdateView.as_view(), name='detail'),
    url(r'^$', ItemsListView.as_view(), name='list'),
]
