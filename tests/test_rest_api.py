from django.test import TestCase
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status
from apps.test_app.models import Car, Component
from apps.test_app.views import CarViewSet, ComponentViewSet
import uuid


def version_uuid(uuid_string: str):
    try:
        return uuid.UUID(str(uuid_string)).version
    except ValueError:
        pass


class TestClass(APITestCase, TestCase):

    @classmethod
    def setUpTestData(cls):
        """Run once to set up non-modified data for all class methods."""
        print('#'*100, f'\nsetUpTestData {__name__}...', sep='')
        cls.car_data = {
            'color': 'yellow',
            'trip': 20000,
            'year': 2010,
            'vendor': 'Hyundai',
            'model': 'Getz',
        }

        cls.car_data2 = {
            'color': 'null',
            'trip': 0,
            'year': '-1',
            'vendor': 0,
            'model': None,
        }

        cls.component_data = {
            'type': 'engine',
            'number': 'VIN1234',
            'car': None,
        }

    @classmethod
    def tearDownClass(cls):
        """Run once after all test methods"""
        print()

    def setUp(self):
        """Run before every test method"""
        print(f'\nTest: {self._testMethodName}...')

        views = {
            'car': CarViewSet,
            'component': ComponentViewSet,
        }
        self.view = views.get(self._testMethodName.split('test_', 1)[-1].split('_', 1)[0])

    def tearDown(self):
        """Run after every test method"""
        pass

    def rest(self, urn: str, pk: str=None, data: dict=None, method: str='GET', view=None):
        urn = urn.replace('<pk>', str(pk)) if pk else urn
        method = method.upper() if isinstance(method, str) else method
        view = view or self.view or None
        print('Request', method, urn)

        actions = {
            'get': 'retrieve',
            'post': 'create',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        }

        view = view.as_view(actions)
        factory = APIRequestFactory()

        request = None
        if method in ('GET', 'DELETE'):
            request = getattr(factory, method.lower())(urn)
        elif data and method in ('POST', 'PUT', 'PATCH'):
            request = getattr(factory, method.lower())(urn, data=data, format='json')

        if request:
            response = view(request, pk=str(pk)).render()
            print(response)
            print(response.data)
            return response

    def rest_get(self, urn: str, pk: str, view=None):
        return self.rest(urn, pk=pk, method='GET', view=view)

    def rest_post(self, urn: str, data: dict, view=None):
        return self.rest(urn, data=data, method='POST', view=view)

    def rest_put(self, urn: str, data: dict, pk: str, view=None):
            return self.rest(urn, pk=pk, data=data, method='PUT', view=view)

    def rest_patch(self, urn: str, data: dict, pk: str, view=None):
        return self.rest(urn, pk=pk, data=data, method='PATCH', view=view)

    def rest_delete(self, urn: str, pk: str, view=None):
        return self.rest(urn, pk=pk, method='DELETE', view=view)

    def test_car_create(self):
        response = self.rest_post('/api/car', self.car_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data.get('uid'))
        self.assertGreater(version_uuid(response.data.get('uid')), 0)

    def test_car_get(self):
        car = Car.objects.create(**self.car_data)
        response = self.rest_get('/api/car/<pk>', pk=car.uid)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data.get('uid'))
        self.assertEqual(response.data['uid'], str(car.uid))

    def test_car_put(self):
        car = Car.objects.create()
        response = self.rest_put('/api/car/<pk>', pk=car.uid, data=self.car_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('color'), self.car_data['color'])

    def test_car_patch(self):
        car = Car.objects.create()
        response = self.rest_patch('/api/car/<pk>', pk=car.uid, data=self.car_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('color'), self.car_data['color'])

    def test_car_delete(self):
        car = Car.objects.create(**self.car_data)
        response = self.rest_delete('/api/car/<pk>', pk=car.uid)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)

    def test_component_create(self):
        response = self.rest_post('/api/component', self.component_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data.get('uid'))
        self.assertGreater(version_uuid(response.data.get('uid')), 0)

    def test_component_get(self):
        component = Component.objects.create(**self.component_data)
        response = self.rest_get('/api/component/<pk>', pk=component.uid)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data.get('uid'))
        self.assertEqual(response.data['uid'], str(component.uid))

    def test_component_put(self):
        component = Component.objects.create()
        response = self.rest_put('/api/component/<pk>', pk=component.uid, data=self.component_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('type'), self.component_data['type'])

    def test_component_patch(self):
        component = Component.objects.create()
        response = self.rest_patch('/api/component/<pk>', pk=component.uid, data=self.component_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('type'), self.component_data['type'])

    def test_component_delete(self):
        component = Component.objects.create(**self.component_data)
        response = self.rest_delete('/api/component/<pk>', pk=component.uid)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)

    def test_component_set_car(self):
        car = Car.objects.create(**self.car_data)
        component = Component.objects.create(**self.component_data)
        component_data = self.component_data
        component_data['car'] = car.uid
        response = self.rest_patch('/api/component/<pk>', pk=component.uid, data=component_data)
        self.assertIsNotNone(response.data.get('car'))
        self.assertEqual(response.data['car'].get('uid'), str(car.uid))
