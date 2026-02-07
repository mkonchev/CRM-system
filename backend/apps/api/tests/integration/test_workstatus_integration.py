from django.test import TestCase
from rest_framework import status
from apps.workstatus.models.WorkstatusModel import Workstatus


class WorkStatusIntegrationTest(TestCase):

    def setUp(self):
        self.workstatus_data = {
            'name': 'In Progress',
            'description': 'Work is currently being performed'
        }

    def test_create_invalid_workstatus(self):
        create_url = '/api/workstatus/create'
        invalid_data = {
            # missing required fields
        }
        response = self.client.post(create_url, **invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Workstatus.objects.count(), 0)

    def test_update_nonexistent_workstatus(self):
        update_url = '/api/workstatus/99999/update'
        update_data = {
            'name': 'Updated Status'
        }
        response = self.client.post(update_url, **update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_nonexistent_workstatus(self):
        delete_url = '/api/workstatus/99999/delete'
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_duplicate_workstatus(self):
        # Create first work status
        create_url = '/api/workstatus/create'
        response = self.client.post(create_url, **self.workstatus_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Try to create work status with same name
        response = self.client.post(create_url, **self.workstatus_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
