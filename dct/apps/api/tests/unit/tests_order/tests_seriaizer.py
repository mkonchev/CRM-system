from django.test import TestCase
from apps.car.models.CarModel import Car
from apps.core.models.UserModel import User
from apps.api.serializers.OrderSerializer import OrderSerializer
from apps.order.models.OrderModel import Order
from rest_framework.test import APIClient
from django.utils import timezone


class OrderSerializerTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.owner = User.objects.create(
            email='owner@example.com',
            first_name='Иван',
            last_name='Иванов',
        )
        self.worker = User.objects.create(
            email='worker@work.com',
            first_name='Петр',
            last_name='Петрович',
            role=1
        )
        self.car = Car.objects.create(
            number='A123BC',
            mark='Toyota',
            model='Camry',
            vin='1234567890ABCDEFG',
            year=2020,
            owner=self.owner
        )
        self.order_data = {
            'owner': self.owner,
            'car': self.car,
            'worker': self.worker,
            'start_date': timezone.now(),
            'is_completed': False
        }
        self.order_data_for_setialize = {
            'owner': self.owner.id,
            'car': self.car.id,
            'worker': self.worker.id,
            'start_date': timezone.now(),
            'is_completed': False
        }
        self.order = Order.objects.create(**self.order_data)
        self.serializer = OrderSerializer(instance=self.order)

    def test_order_serializer_data(self):

        expected_fields = [
            'id', 'owner', 'car', 'worker',
            'start_date', 'end_date', 'is_completed'
        ]
        self.assertCountEqual(self.serializer.data.keys(), expected_fields)
        self.assertEqual(self.serializer.data['owner'], self.owner.id)
        self.assertEqual(self.serializer.data['worker'], self.worker.id)
        self.assertEqual(self.serializer.data['car'], self.car.id)
        self.assertEqual(self.serializer.data['is_completed'], False)

    def test_order_deserializer_invalid_data(self):
        invalid_data = {
            'owner': 999,
            'car': 999,
            'worker': self.owner.id
        }
        serializer = OrderSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())

        self.assertIn('owner', serializer.errors)
        self.assertIn('car', serializer.errors)
        self.assertIn('worker', serializer.errors)

    def test_read_only_fields(self):
        data = self.order_data_for_setialize.copy()
        data['id'] = 100
        serializer = OrderSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        order = serializer.save()
        self.assertNotEqual(order.id, 100)

    def test_nullable_fields(self):
        data = self.order_data_for_setialize.copy()
        data.pop('end_date', None)
        serializer = OrderSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        order = serializer.save()
        self.assertIsNone(order.end_date)
