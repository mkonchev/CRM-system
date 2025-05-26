from django.test import TestCase
from apps.car.models.CarModel import Car
from apps.core.models.UserModel import User
from apps.api.serializers.CarSerializer import CarSerializer


class CarSerializerTest(TestCase):

    def setUp(self):
        self.owner = User.objects.create(
            email='owner@example.com',
            first_name='Иван',
            last_name='Иванов'
        )
        self.car_data = {
            'number': 'A123BC',
            'mark': 'Toyota',
            'model': 'Camry',
            'vin': '1234567890ABCDEFG',
            'year': 2020,
            'owner': self.owner
        }
        self.car = Car.objects.create(**self.car_data)
        self.serializer = CarSerializer(instance=self.car)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['id',
                                            'number',
                                            'mark',
                                            'model',
                                            'vin',
                                            'year',
                                            'owner'])

    def test_serializer_data(self):
        data = self.serializer.data
        self.assertEqual(data['mark'], 'Toyota')
        self.assertEqual(data['model'], 'Camry')
        self.assertEqual(data['year'], 2020)

    def test_create_serializer(self):
        new_car_data = {
            'number': 'B456CD',
            'mark': 'Honda',
            'model': 'Accord',
            'vin': '9876543210ABCDEFG',
            'year': 2021
        }
        serializer = CarSerializer(data=new_car_data)
        self.assertTrue(serializer.is_valid())
        car = serializer.save()
        self.assertEqual(car.mark, 'Honda')

    def test_update_serializer(self):
        update_data = {'mark': 'Updated Toyota'}
        serializer = CarSerializer(instance=self.car,
                                   data=update_data,
                                   partial=True)
        self.assertTrue(serializer.is_valid())
        car = serializer.save()
        self.assertEqual(car.mark, 'Updated Toyota')
