from django.test import TestCase
from apps.car.models import Car
from apps.work.models.WorkModel import Work
from apps.core.models.UserModel import User
from apps.api.serializers.WorkSerializer import WorkSerializer


class WorkSerializerTest(TestCase):

    def setUp(self):
        self.owner = User.objects.create(
            email='owner@example.com',
            first_name='Иван',
            last_name='Иванов'
        )
        self.car = Car.objects.create(
            mark='Toyota',
            model='Camry',
            year=2020,
            vin='XTA21099734455321',
            owner=self.owner
        )

        self.work_data = {
            'name': 'Замена масла',
            'description': 'Полная замена моторного масла и фильтра',
            'car': self.car,
            'price': 5000
        }
        self.work = Work.objects.create(**self.work_data)
        self.serializer = WorkSerializer(instance=self.work)

    def test_work_serialization(self):
        self.assertEqual(self.serializer.data['name'],
                         self.work_data['name'])
        self.assertEqual(self.serializer.data['description'],
                         self.work_data['description'])
        self.assertEqual(self.serializer.data['car'],
                         self.work_data['car'].pk)
        self.assertEqual(self.serializer.data['price'],
                         self.work_data['price'])

    def test_work_serializer_data(self):
        data = self.serializer.data
        self.assertEqual(data['name'], 'Замена масла')
        self.assertEqual(data['description'],
                         'Полная замена моторного масла и фильтра')
        self.assertEqual(data['car'], self.car.pk)
        self.assertEqual(data['price'], 5000)

    def test_create_serializer(self):
        new_work_data = {
            'name': 'Ремонт колеса',
            'description': 'Снять колесо, отрехтовать и отбалансировать',
            'car': self.car.pk,
            'price': 1000
        }
        serializer = WorkSerializer(data=new_work_data)
        self.assertTrue(serializer.is_valid())
        work = serializer.save()
        self.assertEqual(work.name, 'Ремонт колеса')

    def test_update_serializer(self):
        update_data = {'price': 5000}
        serializer = WorkSerializer(instance=self.work,
                                    data=update_data,
                                    partial=True)
        self.assertTrue(serializer.is_valid())
        work = serializer.save()
        self.assertEqual(work.price, 5000)
