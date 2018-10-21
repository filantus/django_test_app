from django.db import models
from django.forms.models import model_to_dict
import uuid
import json


class DataModel():
    def data(self):
        data = model_to_dict(self)
        for key in data:
            value = data[key]
            if isinstance(value, uuid.UUID):
                data[key] = str(value)
        return data

    def json(self):
        return json.dumps(self.data(), indent=4)


class Car(models.Model, DataModel):
    class Meta:
        verbose_name = 'Car'
        verbose_name_plural = 'Cars'
        ordering = ['uid']

    uid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    color = models.CharField(max_length=100, blank=True, null=True)
    trip = models.FloatField(blank=True, null=True)
    year = models.PositiveSmallIntegerField(blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)
    vendor = models.CharField(max_length=100, blank=True, null=True)


class Component(models.Model, DataModel):
    class Meta:
        verbose_name = 'Component'
        verbose_name_plural = 'Components'
        ordering = ['uid']

    uid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    type = models.CharField(max_length=100, blank=True, null=True)
    number = models.CharField(max_length=100, blank=True, null=True)
    car = models.ForeignKey(Car, on_delete=models.PROTECT, blank=True, null=True)
