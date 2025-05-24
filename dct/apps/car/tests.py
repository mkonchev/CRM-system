from django.test import TestCase
from django.core.exceptions import ValidationError
from apps.car.models.CarModel import Car
from apps.core.models.UserModel import User


class CarModelTestCase(TestCase):

    def setUp(self):
        self.owner = User.objects.create(
            email='owner@example.com',
            first_name='Иван',
            last_name='Иванов'
        )
        
        self.car_data = {
            'number': 'А123БВ77',
            'mark': 'Toyota',
            'model': 'Camry',
            'vin': 'XTA21099734455321',
            'year': 2020,
            'owner': self.owner
        }

    def test_car_create(self):
        car = Car.objects.create(**self.car_data)
        
        self.assertEqual(car.number, 'А123БВ77')
        self.assertEqual(car.mark, 'Toyota')
        self.assertEqual(car.model, 'Camry')
        self.assertEqual(car.vin, 'XTA21099734455321')
        self.assertEqual(car.year, 2020)
        self.assertEqual(car.owner, self.owner)

    def test_verbose_names(self):
        """Проверка verbose_name"""
        self.assertEqual(Car._meta.verbose_name, 'Машина')
        self.assertEqual(Car._meta.verbose_name_plural, 'Машины')

    def test_owner_relation(self):
        """Тест связи с владельцем"""
        car = Car.objects.create(**self.car_data)
        self.assertEqual(car.owner, self.owner)
        self.assertIn(car, self.owner.car_owner.all())

    def test_field_max_lengths(self):
        """Тест максимальных длин полей"""
        with self.assertRaises(ValidationError):
            car = Car(
                number='A'*11,  # Превышает max_length=10
                mark='B'*51,    # Превышает max_length=50
                model='C'*51,   # Превышает max_length=50
                vin='D'*101      # Превышает max_length=100
            )
            car.full_clean()
