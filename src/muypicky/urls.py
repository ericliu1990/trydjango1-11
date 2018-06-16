"""MuyPicky URL Configuration

The 'urlpatterns' list routes URLs to views. for more details:
http://docs.djangoproject.com/en/1.11/topics/http/urls/

example:
function views
1. add import: from my_app import views
2. add a url to urlpatterns: url(r'^$', views.home, name='home')

class-based views
1. add an import: from other_app.views import Home
2. add a url to urlpatterns: url(r'^$', Home.as_view(), name='home')

including another URLconf
1. import the include() function: from django.conf.urls import url, include
2. add a url to urlpatterns: url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import include, url
from django.contrib import admin
#from restaurants.views import HomeView 
from django.views.generic.base import TemplateView
from restaurants.views import (
	# restaurant_listview,
	RestaurantsListView,
	# MexicanRestaurantsListView,
	# AsianRestaurantsListView,
	SearchRestaurantsListView,
	RestaurantsDetailView
)

urlpatterns = [
    # Examples:
    # url(r'^$', 'muypicky.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    #url(r'^$', HomeView.as_view()), #this need to be used like this because it contains context in views.py
    url(r'^$', TemplateView.as_view(template_name='home.html')),
    #url(r'^restaurants$', restaurant_listview),
    url(r'^restaurants/$', RestaurantsListView.as_view()),
    
    # url(r'^restaurants/(?P<slug>\w+)$', SearchRestaurantsListView.as_view()),
    #url(r'^restaurants/(?P<pk>\w+)$', RestaurantsDetailView.as_view()),
    # url(r'^restaurants/(?P<rest_id>\w+)$', RestaurantsDetailView.as_view()),
    url(r'^restaurants/(?P<slug>[\w-]+)$', RestaurantsDetailView.as_view()),
    #url(r'^restaurants/mexican$', MexicanRestaurantsListView.as_view()),
    #url(r'^restaurants/asian$', AsianRestaurantsListView.as_view()),
    
    # url(r'^about$', AboutView.as_view()),
    # # url(r'^contact/(?P<Id>\d+)$', ContactView.as_view()),
    # url(r'^contact$', ContactView.as_view())
    url(r'^about$', TemplateView.as_view(template_name='about.html')),
    url(r'^contact$', TemplateView.as_view(template_name='contact.html'))
]
