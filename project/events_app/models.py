from enum import Enum

from django.contrib.auth.models import User
from django.db import models


class FieldsParser(Enum):
    @classmethod
    def parse_as_tuple(cls):
        return tuple(
            (i.name, i.value)
            for i in cls
        )

    @classmethod
    def parse_as_dict(cls):
        return {
            i.name: i.value
            for i in cls
        }


class EventCategories(FieldsParser):
    CONFERENCE = 'Conference'
    SEMINAR = 'Seminar'
    CONGRESS = 'Congress'
    COURSE = 'Course'


class Event(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    name = models.TextField()
    place = models.TextField()
    address = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_virtual = models.BooleanField(default=False)

    category = models.CharField(
        max_length=10,
        choices=EventCategories.parse_as_tuple(),
        default=EventCategories.CONFERENCE
    )

    created_at = models.DateTimeField()

    def __str__(self):
        return """
            id: '{id}'
            user: '{user}'
            name: '{name}'
            place: '{place}'
            address: '{address}'
            start_date: '{start_date}'
            end_date: '{end_date}'
            is_virtual: '{is_virtual}'
            category: '{category}'
        """.format(
            id=self.id,
            user=self.user,
            name=self.name,
            place=self.place,
            address=self.address,
            start_date=self.start_date,
            end_date=self.end_date,
            is_virtual=self.is_virtual,
            category=self.category
        )
