from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from apps.order.models import Order
from apps.car.models import Car
from apps.core.models import User


class OrderModelTestCase(TestCase):
    def setUp(self):

        self.owner = User.objects.create(
            email='owner@example.com',
            first_name='Иван',
            last_name='Иванов'
        )
        self.worker = User.objects.create(
            email='worker@example.com',
            first_name='Петр',
            last_name='Петров',
            role=1
        )
        self.car = Car.objects.create(
            mark='Toyota',
            model='Camry',
            year=2020,
            vin='XTA21099734455321',
            owner=self.owner
        )

        self.order_data = {
            'owner': self.owner,
            'car': self.car,
            'worker': self.worker,
            'end_date': timezone.now() + timezone.timedelta(days=1)
        }

    def test_order_creation(self):
        """Тест создания объекта Order"""
        order = Order.objects.create(**self.order_data)

        self.assertEqual(order.owner, self.owner)
        self.assertEqual(order.car, self.car)
        self.assertEqual(order.worker, self.worker)
        self.assertFalse(order.is_completed)
        self.assertIsNotNone(order.start_date)
        self.assertIsNotNone(order.end_date)

    def test_str_representation(self):
        """Тест строкового представления"""
        order = Order.objects.create(**self.order_data)
        self.assertEqual(str(order), f'{self.car} {self.worker}')

    def test_relations(self):
        """Тест связей между моделями"""
        order = Order.objects.create(**self.order_data)

        self.assertEqual(order.owner, self.owner)
        self.assertIn(order, self.owner.order_owner.all())

        self.assertEqual(order.car, self.car)
        self.assertIn(order, self.car.orders.all())

        self.assertEqual(order.worker, self.worker)
        self.assertIn(order, self.worker.orders.all())

    def test_worker_limit_choices(self):

        non_worker = User.objects.create(email='nonworker@example.com', role=2)

        with self.assertRaises(ValidationError):
            order = Order(car=self.car, worker=non_worker)
            order.full_clean()
