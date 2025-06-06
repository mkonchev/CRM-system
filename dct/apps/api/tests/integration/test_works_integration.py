from django.test import TestCase
from rest_framework import status
from apps.work.models.WorkModel import Work
from apps.api.tests.factories import WorkFactory, WorkstatusFactory


class WorkIntegrationTest(TestCase):

    def setUp(self):
        self.workstatus = WorkstatusFactory()
        self.work_data = {
            'name': 'Oil Change',
            'description': 'Full synthetic oil change service',
            'price': '49.99',
            'duration': 60,  # minutes
            'status': self.workstatus.id
        }

    def test_full_work_lifecycle(self):
        # Create a new work
        create_url = '/api/work/create'
        response = self.client.post(create_url, self.work_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        work_id = response.data['id']

        # Verify work was created in database
        self.assertEqual(Work.objects.count(), 1)
        work = Work.objects.get(pk=work_id)
        self.assertEqual(work.name, self.work_data['name'])
        self.assertEqual(work.description, self.work_data['description'])
        self.assertEqual(str(work.price), self.work_data['price'])
        self.assertEqual(work.duration, self.work_data['duration'])
        self.assertEqual(work.status.id, self.work_data['status'])

        # Get list of works
        list_url = '/api/work/'
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], work_id)

        # Get work details
        detail_url = f'/api/work/{work_id}'
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], work_id)

        # Update work
        update_url = f'/api/work/{work_id}/update'
        update_data = {
            'price': '59.99',
            'duration': 75
        }
        response = self.client.post(update_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        work.refresh_from_db()
        self.assertEqual(str(work.price), update_data['price'])
        self.assertEqual(work.duration, update_data['duration'])

        # Delete work
        delete_url = f'/api/work/{work_id}/delete'
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(Work.objects.count(), 0)

    def test_create_invalid_work(self):
        create_url = '/api/work/create'
        invalid_data = {
            'name': 'Oil Change',
            # missing required fields
        }
        response = self.client.post(create_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Work.objects.count(), 0)

    def test_update_nonexistent_work(self):
        update_url = '/api/work/99999/update'
        update_data = {
            'price': '59.99'
        }
        response = self.client.post(update_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_nonexistent_work(self):
        delete_url = '/api/work/99999/delete'
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_work_with_invalid_status(self):
        create_url = '/api/work/create'
        invalid_data = self.work_data.copy()
        invalid_data['status'] = 99999  # non-existent status
        response = self.client.post(create_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Work.objects.count(), 0) 