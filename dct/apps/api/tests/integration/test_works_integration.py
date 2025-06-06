from django.test import TestCase
from rest_framework import status
from apps.work.models.WorkModel import Work
from apps.api.tests.factories import WorkFactory, WorkStatusFactory


class WorkIntegrationTest(TestCase):

    def setUp(self):
        self.workstatus = WorkStatusFactory()
        self.work_data = {
            'name': 'Oil Change',
            'description': 'Full synthetic oil change service',
            'price': '49.99',
            'duration': 60,  # minutes
            'status': self.workstatus.id
        }

    def test_create_invalid_work(self):
        create_url = '/api/work/create'
        invalid_data = {
            'name': 'Oil Change',
            # missing required fields
        }
        response = self.client.post(create_url, **invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Work.objects.count(), 1)

    def test_update_nonexistent_work(self):
        update_url = '/api/work/99999/update'
        update_data = {
            'price': '59.99'
        }
        response = self.client.post(update_url, **update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_nonexistent_work(self):
        delete_url = '/api/work/99999/delete'
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_work_with_invalid_status(self):
        create_url = '/api/work/create'
        invalid_data = self.work_data.copy()
        invalid_data['status'] = 99999  # non-existent status
        response = self.client.post(create_url, **invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Work.objects.count(), 1) 