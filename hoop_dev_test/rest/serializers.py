from hoop_dev_test.data.models import Event, Location, Category
from rest_framework import serializers


class NameField(serializers.CharField):
    """
    In order to mask the fact that Location and Category objects are in fact
    models themselves, this field type gives only the name of the object it
    represents, rather than the full details.
    """

    def to_representation(self, value):
        from django.utils import six
        return six.text_type(value.name)


class EventSerializer(serializers.HyperlinkedModelSerializer):
    """
    Handle the serialisation and de-serialisation of our event models. I chose
    to use a HyperlinkedModelSerializer so that for the most part our API
    follows a HATEOAS design - this makes it far easier to discover.
    """

    class Meta:
        model = Event
        fields = ('eventID', 'url', 'name', 'location', 'category')


    eventID = serializers.PrimaryKeyRelatedField(read_only=True)
    name = serializers.CharField()
    category = NameField()
    location = NameField()

    @staticmethod
    def _get_location(data):
        return Location.objects.get_or_create(name=data['location'])[0]

    @staticmethod
    def _get_category(data):
        return Category.objects.get_or_create(name=data['category'])[0]

    def create(self, data):
        name = data['name']
        location = self._get_location(data)
        category = self._get_category(data)
        return Event.objects.create(name=name,
                                    location=location,
                                    category=category)

    def update(self, instance, data):
        instance.name = data['name']
        instance.location = self._get_location(data)
        instance.category = self._get_category(data)
        instance.save()
        return instance


class RelatedListField(serializers.ListField):
    """
    Another simple field - ListField does almost what I want, but isn't designed
    for lists of relations - I couldn't easily find one that did, so I adapted
    ListField by simply changing the list comprehension in to_representation to
    iterate over `data.all()` rather than `data`. As this operates on a
    relationship I renamed the parameter to be more descriptive.
    """
    pass

    def to_representation(self, related):
        return [self.child.to_representation(item) for item in related.all()]


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    """ This is really just to make the Location endpoints nice - bonus """

    class Meta:
        model = Location
        fields = ('url', 'name', 'events')

    events = RelatedListField(child=EventSerializer(), required=False)


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    """ This is really just to make the Category endpoints nice - bonus """

    class Meta:
        model = Category
        fields = ('url', 'name', 'events')

    events = RelatedListField(child=EventSerializer(), required=False)

__all__ = ['LocationSerializer',
           'CategorySerializer',
           'EventSerializer']