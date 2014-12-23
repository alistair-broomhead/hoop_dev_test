"""
The models for our event data.

We will inevitably want to be able to filter or sort by location or category, so
these must be indexed - as we're likely to have many identical entries I have
made locations and categories models in their own right - not only should this
save database space, but should also make it easier to spot and correct
mis-entered data (i.e. incorrect capitalisation, mis-spellings).

Ideally we should have some constraints on the length of a name, however without
this I have made the name fields TextField rather than CharField - this is less
efficient but more flexible.
"""
from django.db import models


class Location(models.Model):
    name = models.TextField(unique=True, db_index=True)


class Category(models.Model):

    class Meta:
        verbose_name_plural = "categories"

    name = models.TextField(unique=True, db_index=True)


class Event(models.Model):

    class Meta:
        verbose_name_plural = "entries"

    @property
    def eventID(self):
        return self.id

    name = models.TextField(unique=True)
    location = models.ForeignKey(Location, db_index=True, related_name="events")
    category = models.ForeignKey(Category, db_index=True, related_name="events")