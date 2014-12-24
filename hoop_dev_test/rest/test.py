"""
Here I have a fairly basic set of tests, just trying to perform CRUD operations
on Event Location and Category endpoints both as an authenticated user and an
anonymous user - obviously more sophisticated tests could be wanted such as
behaviour driven tests which test the ability to perform user-centric tasks
which may involve consuming a sequence of endpoints in a consistent manner.
"""
from functools import wraps
import json
from abc import ABCMeta

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.status import *
from nose.tools import assert_equal, assert_is_none

from hoop_dev_test.data.models import Event, Location, Category
from hoop_dev_test.test_data import TestData


def assert_status(code):
    """
    A simple decorator for any test that returns a response object
    """
    def decorator(fn):
        @wraps(fn)
        def _inner(*args, **kwargs):
            response = fn(*args, **kwargs)
            assert_equal(response.status_code, code)
            return response
        return _inner
    return decorator


class APIBase(object):
    """
    This abstract class contains the operations we want to run using our two
    concrete classes - we can then assert different behaviour based on whether
    we are authenticated or not.
    """
    __metaclass__ = ABCMeta
    client = None

    # noinspection PyPep8Naming,PyAttributeOutsideInit
    @classmethod
    def _setUpClass(cls):
        """
        Ensure that these tests always start from a blank slate
        """
        cls.data = TestData()

        for model in Event, Location, Category:
            map(model.delete, model.objects.all())

        cls.event = cls.data.next.get_or_create()

    @property
    def location(self):
        return self.event.location

    @property
    def category(self):
        return self.event.category

    @staticmethod
    def _assert_single(obj):
        assert_equal(obj.data["count"], 1)
        assert_is_none(obj.data["next"])
        assert_is_none(obj.data["previous"])

    # Test event endpoints
    def test_get_event_list(self):
        entries = self.client.get('/rest/event/')
        self._assert_single(entries)
        event = entries.data["results"][0]
        assert_equal(event["eventID"], self.event.eventID)
        assert_equal(event["name"], self.event.name)
        assert_equal(event["category"], self.event.category.name)
        return entries

    def test_post_event(self):
        return self.client.post('/rest/event/', self.data.next.to_dict)

    def test_get_event(self):
        event = self.client.get('/rest/event/{0}/'.format(self.event.pk))
        assert_equal(event.data['name'], self.event.name)
        assert_equal(event.data['category'], self.event.category.name)
        assert_equal(event.data['location'], self.event.location.name)
        return event

    def test_put_event(self):
        return self.client.put('/rest/event/{0}/'.format(self.event.pk),
                               self.data.next.to_json,
                               content_type='application/json')

    def test_delete_event(self):
        return self.client.delete('/rest/event/{0}/'.format(self.event.pk))

    # Test location endpoints

    def test_get_location_list(self):
        locations = self.client.get('/rest/location/')
        self._assert_single(locations)
        location = locations.data["results"][0]
        assert_equal(location["name"], self.location.name)
        return locations

    def test_post_location(self):
        return self.client.post('/rest/location/', {'name': 'Nowhere'})

    def test_get_location(self):
        location = self.client.get('/rest/location/{0}/'.format(
            self.location.pk))
        assert_equal(location.data['name'], self.location.name)
        return location

    def test_put_location(self):
        return self.client.put('/rest/location/{0}/'.format(self.location.pk),
                               json.dumps({'name': 'Nowhere'}),
                               content_type='application/json')

    def test_delete_location(self):
        return self.client.delete('/rest/location/{0}/'.format(
            self.location.pk))

    # Test category endpoints
    def test_get_category_list(self):
        categories = self.client.get('/rest/category/')
        self._assert_single(categories)
        category = categories.data["results"][0]
        assert_equal(category["name"], self.category.name)
        return categories

    def test_post_category(self):
        return self.client.post('/rest/category/', {'name': 'Nowhere'})

    def test_get_category(self):
        category = self.client.get('/rest/category/{0}/'.format(
            self.category.pk))
        assert_equal(category.data['name'], self.category.name)
        return category

    def test_put_category(self):
        return self.client.put('/rest/category/{0}/'.format(self.category.pk),
                               json.dumps({'name': 'Nothing'}),
                               content_type='application/json')

    def test_delete_category(self):
        return self.client.delete('/rest/category/{0}/'.format(
            self.category.pk))


class AnonymousAPITest(APIBase, TestCase):

    @classmethod
    def setUpClass(cls):
        cls._setUpClass()

    @assert_status(HTTP_200_OK)
    def test_get_location_list(self):
        return super(AnonymousAPITest, self).test_get_location_list()

    @assert_status(HTTP_200_OK)
    def test_get_category_list(self):
        return super(AnonymousAPITest, self).test_get_category_list()

    @assert_status(HTTP_200_OK)
    def test_get_event_list(self):
        return super(AnonymousAPITest, self).test_get_event_list()

    @assert_status(HTTP_200_OK)
    def test_get_category(self):
        return super(AnonymousAPITest, self).test_get_category()

    @assert_status(HTTP_200_OK)
    def test_get_location(self):
        return super(AnonymousAPITest, self).test_get_location()

    @assert_status(HTTP_403_FORBIDDEN)
    def test_post_event(self):
        return super(AnonymousAPITest, self).test_post_event()

    @assert_status(HTTP_403_FORBIDDEN)
    def test_put_event(self):
        return super(AnonymousAPITest, self).test_put_event()

    @assert_status(HTTP_403_FORBIDDEN)
    def test_delete_event(self):
        return super(AnonymousAPITest, self).test_delete_event()

    @assert_status(HTTP_403_FORBIDDEN)
    def test_post_location(self):
        return super(AnonymousAPITest, self).test_post_location()

    @assert_status(HTTP_403_FORBIDDEN)
    def test_put_location(self):
        return super(AnonymousAPITest, self).test_put_location()

    @assert_status(HTTP_403_FORBIDDEN)
    def test_delete_location(self):
        return super(AnonymousAPITest, self).test_delete_location()

    @assert_status(HTTP_403_FORBIDDEN)
    def test_post_category(self):
        return super(AnonymousAPITest, self).test_post_category()

    @assert_status(HTTP_403_FORBIDDEN)
    def test_put_category(self):
        return super(AnonymousAPITest, self).test_put_category()

    @assert_status(HTTP_403_FORBIDDEN)
    def test_delete_category(self):
        return super(AnonymousAPITest, self).test_delete_category()


class AuthenticatedAPITest(APIBase, TestCase):

    username = 'admin'
    password = 'admin'

    @classmethod
    def setUpClass(cls):
        """
        Ensure that these tests always start from a blank slate
        """
        User.objects.create_user(username=cls.username, password=cls.password)
        cls._setUpClass()

    def setUp(self):
        self.client.login(username=self.username, password=self.password)

    @assert_status(HTTP_200_OK)
    def test_get_location_list(self):
        return super(AuthenticatedAPITest, self).test_get_location_list()

    @assert_status(HTTP_200_OK)
    def test_get_category_list(self):
        return super(AuthenticatedAPITest, self).test_get_category_list()

    @assert_status(HTTP_200_OK)
    def test_get_event_list(self):
        return super(AuthenticatedAPITest, self).test_get_event_list()

    @assert_status(HTTP_200_OK)
    def test_get_category(self):
        return super(AuthenticatedAPITest, self).test_get_category()

    @assert_status(HTTP_200_OK)
    def test_get_location(self):
        return super(AuthenticatedAPITest, self).test_get_location()

    @assert_status(HTTP_201_CREATED)
    def test_post_event(self):
        return super(AuthenticatedAPITest, self).test_post_event()

    @assert_status(HTTP_200_OK)
    def test_put_event(self):
        return super(AuthenticatedAPITest, self).test_put_event()

    @assert_status(HTTP_204_NO_CONTENT)
    def test_delete_event(self):
        return super(AuthenticatedAPITest, self).test_delete_event()

    @assert_status(HTTP_201_CREATED)
    def test_post_location(self):
        return super(AuthenticatedAPITest, self).test_post_location()

    @assert_status(HTTP_200_OK)
    def test_put_location(self):
        return super(AuthenticatedAPITest, self).test_put_location()

    @assert_status(HTTP_204_NO_CONTENT)
    def test_delete_location(self):
        return super(AuthenticatedAPITest, self).test_delete_location()

    @assert_status(HTTP_201_CREATED)
    def test_post_category(self):
        return super(AuthenticatedAPITest, self).test_post_category()

    @assert_status(HTTP_200_OK)
    def test_put_category(self):
        return super(AuthenticatedAPITest, self).test_put_category()

    @assert_status(HTTP_204_NO_CONTENT)
    def test_delete_category(self):
        return super(AuthenticatedAPITest, self).test_delete_category()