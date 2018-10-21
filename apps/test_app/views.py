from django.shortcuts import render
from rest_framework import viewsets
from .models import Car, Component
from .serializers import CarSerializer, ComponentSerializer


def index(request):
    context = {
    }
    return render(request, 'test_app/index.html', context)


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class ComponentViewSet(viewsets.ModelViewSet):
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer
