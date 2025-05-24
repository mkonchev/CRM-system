from django.test import TestCase
from apps.car.models import Car
from django.core.exceptions import ValidationError
from apps.work.models import Work


class WorkModelTestCase(TestCase):

    def setUp(self):
        self.car = Car.objects.create(
            mark='Toyota',
            model='Camry',
            year=2020,
            vin='XTA21099734455321'
        )

        self.work_data = {
            'name': 'Замена масла',
            'description': 'Полная замена моторного масла и фильтра',
            'car': self.car,
            'price': 5000
        }

    def test_work_creation(self):
        work = Work.objects.create(**self.work_data)

        self.assertEqual(work.name, 'Замена масла')
        self.assertEqual(work.description,
                         'Полная замена моторного масла и фильтра')
        self.assertEqual(work.car, self.car)
        self.assertEqual(work.price, 5000)

    def test_str_representation(self):
        work = Work.objects.create(**self.work_data)
        self.assertEqual(str(work), f'Замена масла ({self.car})')

    def test_car_relation(self):
        work = Work.objects.create(**self.work_data)
        self.assertEqual(work.car, self.car)
        self.assertIn(work, self.car.car_works.all())

    def test_price_validation(self):
        with self.assertRaises(ValidationError):
            work = Work(name='Диагностика', price=-1000)
            work.full_clean()
