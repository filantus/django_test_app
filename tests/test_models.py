from django.test import TestCase
from apps.test_app.models import Car, Component
import uuid


def version_uuid(uuid_string: str):
    try:
        return uuid.UUID(str(uuid_string)).version
    except ValueError:
        pass


class TestClass(TestCase):

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
            'year': -1,
            'vendor': '',
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

    def tearDown(self):
        """Run after every test method"""
        pass

    def create_component_with_car(self, with_car2=False) -> tuple:
        car = Car.objects.create(**self.car_data)

        tmp_component_data = self.component_data.copy()
        tmp_component_data['car'] = car

        component = Component(**tmp_component_data)
        component.save()

        if with_car2:
            car2 = Car.objects.create(**self.car_data2)
            return car, car2, component
        return car, component

    def test_car_create(self):
        """Создание объекта машины и сохранение его в базе данных"""
        car = Car(**self.car_data)
        car.save()
        self.assertGreater(version_uuid(car.uid), 0)
        self.assertEqual(car.vendor, self.car_data['vendor'])

    def test_component_create(self):
        """Создание объекта компонента и сохранение его в базе данных"""
        component = Component(**self.component_data)
        component.save()

        self.assertGreater(version_uuid(component.uid), 0)
        self.assertEqual(component.number, self.component_data['number'])

    def test_component_create_with_car(self):
        """Создание машины, а затем компонента с привязкой к этой машине."""
        car, component = self.create_component_with_car()
        self.assertGreater(version_uuid(component.uid), 0)

    def test_component_get_car(self):
        """Свойство компонента "car" должно возвращать либо None либо объект
           типа <class 'main.models.Car'>
        """
        car, component = self.create_component_with_car()
        self.assertTrue(isinstance(component.car, Car))

    def test_component_set_car(self):
        """У компонента есть свойство "car", оно должно иметь возможность принимать
          значение типа: <class 'main.models.Car'> или <class 'NoneType'>.
        """
        car, car2, component = self.create_component_with_car(with_car2=True)

        component.car = car2
        self.assertEqual(component.car.uid, car2.uid)
        self.assertTrue(isinstance(component.car, Car))

    def test_component_unset_car(self):
        car, component = self.create_component_with_car()
        component.car = None
        self.assertIsNone(component.car)
