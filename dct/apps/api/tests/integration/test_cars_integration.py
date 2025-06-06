from django.test import TestCase
from rest_framework import status
from apps.car.models.CarModel import Car
from apps.api.tests.factories import CarFactory


class CarIntegrationTest(TestCase):

    def setUp(self):
        self.car_data = {
            'mark': 'Toyota',
            'model': 'Camry',
            'year': 2020,
            'vin': 'ABC123456789DEF12'
        }

    def test_full_car_lifecycle(self):
        # Create a new car
        create_url = '/api/car/create'
        response = self.client.post(create_url, **self.car_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        car_id = response.data['id']

        # Verify car was created in database
        self.assertEqual(Car.objects.count(), 1)
        car = Car.objects.get(pk=car_id)
        self.assertEqual('Toyota', self.car_data['mark'])
        self.assertEqual('Camry', self.car_data['model'])
        self.assertEqual(2020, self.car_data['year'])
        self.assertEqual('ABC123456789DEF12', self.car_data['vin'])

        # Get list of cars
        list_url = '/api/car/'
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], car_id)

        # Get car details
        detail_url = f'/api/car/{car_id}'
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], car_id)

        # Update car
        update_url = f'/api/car/{car_id}/update'
        update_data = {
            'year': 2021,
            'vin': 'XYZ987654321ABC45'
        }
        response = self.client.post(update_url, **update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        car.refresh_from_db()
        self.assertEqual(2021, update_data['year'])
        self.assertEqual('XYZ987654321ABC45', update_data['vin'])

        # Delete car
        delete_url = f'/api/car/{car_id}/delete'
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(Car.objects.count(), 0)

    def test_create_invalid_car(self):
        create_url = '/api/car/create'
        invalid_data = {
            'mark': 'Toyota',
            # missing required fields
        }
        response = self.client.post(create_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Car.objects.count(), 1)

    def test_update_nonexistent_car(self):
        update_url = '/api/car/99999/update'
        update_data = {
            'year': 2021
        }
        response = self.client.post(update_url, **update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_nonexistent_car(self):
        delete_url = '/api/car/99999/delete'
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 