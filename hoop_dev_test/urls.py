"""
Plumb in both the rest service and the auth service that comes as part of
django rest framework.
"""
from django.conf.urls import include, url

urlpatterns = [
    url(r'^rest/', include('hoop_dev_test.rest.urls')),
    url(r'^', include('rest_framework.urls', namespace='rest_framework'))
]