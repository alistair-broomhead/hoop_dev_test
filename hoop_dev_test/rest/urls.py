"""
Just hook up the REST views to urls - having used ViewSet this is mostly done
for us.
"""

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('event', views.EntryViewSet)
router.register('category', views.CategoryViewSet)
router.register('location', views.LocationViewSet)


urlpatterns = [
    url(r'^$', views.api_root),
    url(r'^', include(router.urls))
]