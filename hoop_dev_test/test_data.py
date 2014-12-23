# coding=utf-8
"""
A representation of the csv file of test data given - this is used in the rest
test cases, but can also be used to pre-seed the database.
"""
import json

from hoop_dev_test.data.models import Event, Location, Category


class TestData(object):
    class Example(object):
        """
        This class holds a single event's info and can be used to either produce
        a dictionary, its json representation, or an Event object. The
        dictionary and json representations should be suitable for POST/PUTing
        to the REST API.
        """
        def __init__(self, name, location, category):
            self.event_id = None
            self.name = name
            self.location = location
            self.category = category

        @property
        def to_dict(self):
            d = {
                'name': self.name,
                'location': self.location,
                'category': self.category
            }
            if self.event_id is not None:
                d['eventID'] = self.event_id
            return d

        @property
        def to_json(self):
            return json.dumps(self.to_dict)

        def get_or_create(self):
            l = Location.objects.get_or_create(name=self.location)[0]
            c = Category.objects.get_or_create(name=self.category)[0]
            e = Event.objects.get_or_create(name=self.name,
                                            location=l,
                                            category=c)[0]
            self.event_id = e.pk
            return e

    examples = (
        # Here be the examples...
        Example("John's Pottery Class", "London", "arts and craft"),
        Example("Football for 4-6 Year Olds", "London", "sports"),
        Example("French for Toddlers", "London", "language"),
        Example("Finger Painting for Two Year Olds", "Birmingham",
                "arts and craft"),
        Example("Baby Yoga at Islington Town Hall ☯", "London", "sports"),
        Example("Archery: Ages 8-12", "Manchester", "sports"),
        Example("Rugby & Football Afternoon", "Birmingham", "sports"),
        Example("Let's Learn Spanish!", "Birmingham", "language"),
        Example("¿Cómo estás?: Introduction to Spanish", "Bristol", "language"),
        Example("Advanced Portrait Painting", "Bristol", "arts and craft")
    )

    def __init__(self):
        """
        I wanted to make it easy to go through the examples, so I hold an
        iterator within each instance, as well as the current example, and a
        list of those we have visited already.
        """
        self._iter = (eg for eg in self.examples)
        self.used = []
        self.current = None

    @property
    def next(self):
        """ Get the next example once we're done with the previous """
        prev = self.current
        self.current = next(self._iter)
        if prev is not None:
            self.used.append(prev)
        return self.current

    def create_all(self):
        """ Make sure all the examples are in the database """
        for eg in self._iter:
            eg.get_or_create()