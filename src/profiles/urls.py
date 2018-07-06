from . views import ProfileDetailsView

from django.conf.urls import include, url


urlpatterns = [
    url(r'^(?P<username>[\w-]+)$', ProfileDetailsView.as_view(), name='detail'),
]
