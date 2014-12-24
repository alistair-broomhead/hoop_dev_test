"""
For the most part these are standard ViewSets, but with some added control over
the display formatting. There could be some merit in the future to adding xml
support etc - for now JSON will do.
"""
from collections import OrderedDict

from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework import viewsets

from hoop_dev_test.data.models import Event, Location, Category
from .serializers import *


def ensure_data():
    """
    A bit of a cheat - before we list any sort of data, make sure we've added
    the example events.
    """
    if Event.objects.count() == 0:
        from hoop_dev_test.test_data import TestData
        TestData().create_all()


@api_view(('GET',))
def api_root(request, format_=None):
    """
    This is the root of our API, the main part of this lies under `event`, but
    `location` and `category` are provided for convenience.
    """
    ensure_data()
    return Response({
        'events': reverse('event-list', request=request, format=format_),
        'locations': reverse('location-list', request=request, format=format_),
        'categories': reverse('category-list', request=request, format=format_)
    })


class EntryViewSet(viewsets.ModelViewSet):
    """
    A ViewSet of our Entry objects - the spec called for some customisation of
    the list display, to only show the id, name and category. I have disobeyed
    this slightly by including the url to an event to make browsing the API
    easier.

    For the list part I have implemented sorting using the query string
    'order_by' which I've tested using location and category. As a bonus I've
    added a query string for each to allow filtering by location or category.

    i.e.

    <a href="/rest/event/?order_by=location&category=sports">?order_by=location&category=sports</a>

    <a href="/rest/event/?order_by=category&location=London">?order_by=category&location=London</a>

    <a href="/rest/event/?location=London&category=arts%20and%20craft">?location=London&category=arts%20and%20craft</a>
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = permissions.IsAuthenticatedOrReadOnly,

    def list(self, request, *args, **kwargs):
        """
        This has had some method calls added to change the list representation -
        please see the individual methods for a description.
        """
        ensure_data()
        queryset = self.get_queryset()

        queryset = self.order(request, queryset)
        queryset = self.location(request, queryset)
        queryset = self.category(request, queryset)

        instance = self.filter_queryset(queryset)
        page = self.paginate_queryset(instance)
        if page is not None:
            serializer = self.get_pagination_serializer(page)
        else:
            serializer = self.get_serializer(instance, many=True)

        results = serializer.data['results']

        for result in results:
            self.reduce_result(result)

        return Response(serializer.data)

    @staticmethod
    def reduce_result(result):
        """
        For each event in the listing we shall only show:
            - url
            - eventID
            - name
            - category
        Other than having added the url, this is what was specified in the spec.
        """
        reduced = OrderedDict()
        reduced['url'] = result.pop('url')  # For HATEOAS
        reduced['eventID'] = result.pop('eventID')
        reduced['name'] = result.pop('name')
        reduced['category'] = result.pop('category')
        result.clear()
        result.update(reduced)

    @staticmethod
    def order(request, query_set):
        """ Allow events to be ordered by location or category """
        by = request.QUERY_PARAMS.get('order_by', None)
        if by is None:
            return query_set
        if by in {'location', 'category'}:  # Use the location/category name
            by += '__name'                  # as opposed to its primary key...
        return query_set.order_by(by)

    @staticmethod
    def location(request, query_set):
        """ Filter for a location """
        location = request.QUERY_PARAMS.get('location', None)
        if location is None:
            return query_set
        return query_set.filter(location__name=location)

    @staticmethod
    def category(request, query_set):
        """ Filter for a category """
        category = request.QUERY_PARAMS.get('category', None)
        if category is None:
            return query_set
        return query_set.filter(category__name=category)


def collapse_events_in_list(self):
    """
    A bit of fun - there was a lot on category/location lists, so replace the
    list of events with simply a count of how many there are.
    """
    ensure_data()
    instance = self.filter_queryset(self.get_queryset())
    page = self.paginate_queryset(instance)
    if page is not None:
        serializer = self.get_pagination_serializer(page)
    else:
        serializer = self.get_serializer(instance, many=True)

    results = serializer.data['results']

    for result in results:
        events = result.pop('events')
        result['numEvents'] = len(events)

    return Response(serializer.data)


class LocationViewSet(viewsets.ModelViewSet):
    """ Seeing as it's so easy, I may as well expose Locations """
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = permissions.IsAuthenticatedOrReadOnly,

    def list(self, request, *args, **kwargs):
        return collapse_events_in_list(self)


class CategoryViewSet(viewsets.ModelViewSet):
    """ Seeing as it's so easy, I may as well expose Categories """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = permissions.IsAuthenticatedOrReadOnly,

    def list(self, request, *args, **kwargs):
        return collapse_events_in_list(self)