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

from django.contrib.auth.views import LoginView, LogoutView



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
	RestaurantsDetailView,
	restaurant_createview,
	RestaurantCreateView,
    restaurant_FBV_createview
)

from profiles.views import ProfileFollowToggle, RegisterView, activate_user_view
from menus.views import HomeView

urlpatterns = [
    # Examples:
    # url(r'^$', 'muypicky.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^items/', include('menus.urls', namespace='menus')),
    url(r'^restaurants/', include('restaurants.urls', namespace='restaurants')),
    url(r'^profile/', include('profiles.urls', namespace='profile')),
    #url(r'^$', HomeView.as_view()), #this need to be used like this because it contains context in views.py
    # url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^$', HomeView.as_view(), name='home'),
    #url(r'^restaurants$', restaurant_listview),
    
    #included from restaurants/urls.py
    #url(r'^restaurants/$', RestaurantsListView.as_view(), name='restaurants'),
    
    #url(r'^restaurants/create$', restaurant_createview),
    url(r'^restaurants/create_FBV$' , restaurant_FBV_createview),

    #included from restaurants/urls.py
    #url(r'^restaurants/create$', RestaurantCreateView.as_view(),  name='restaurants-create'),
    
    # url(r'^restaurants/(?P<slug>\w+)$', SearchRestaurantsListView.as_view()),
    #url(r'^restaurants/(?P<pk>\w+)$', RestaurantsDetailView.as_view()),
    # url(r'^restaurants/(?P<rest_id>\w+)$', RestaurantsDetailView.as_view()),

    #included from restaurants/urls.py
    #url(r'^restaurants/(?P<slug>[\w-]+)$', RestaurantsDetailView.as_view(), name='restaurant-detail'),

    #url(r'^restaurants/mexican$', MexicanRestaurantsListView.as_view()),
    #url(r'^restaurants/asian$', AsianRestaurantsListView.as_view()),
    
    # url(r'^about$', AboutView.as_view()),
    # # url(r'^contact/(?P<Id>\d+)$', ContactView.as_view()),
    # url(r'^contact$', ContactView.as_view())
    url(r'^about$', TemplateView.as_view(template_name='about.html'), name='about'),
    url(r'^contact$', TemplateView.as_view(template_name='contact.html'), name='contact'),

    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^profile-follow/$', ProfileFollowToggle.as_view(), name='follow'),
    url(r'^activate/(?P<code>[a-z0-9].*)/$', activate_user_view, name='activate'),
]
