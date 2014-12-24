"""
Plumb in both the rest service and the auth service that comes as part of
django rest framework.
"""
from django.conf.urls import include, url
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^rest/', include('hoop_dev_test.rest.urls')),
    url(r'$', RedirectView.as_view(url='rest/', permanent=False)),
    url(r'^', include('rest_framework.urls', namespace='rest_framework'))
]