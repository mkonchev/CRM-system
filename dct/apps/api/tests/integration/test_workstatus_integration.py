from django.test import TestCase
from rest_framework import status
from apps.workstatus.models.WorkstatusModel import Workstatus
from apps.api.tests.factories import WorkstatusFactory


class WorkStatusIntegrationTest(TestCase):

    def setUp(self):
        self.workstatus_data = {
            'name': 'In Progress',
            'description': 'Work is currently being performed'
        }

    def test_full_workstatus_lifecycle(self):
        # Create a new work status
        create_url = '/api/workstatus/create'
        response = self.client.post(create_url, self.workstatus_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        workstatus_id = response.data['id']

        # Verify work status was created in database
        self.assertEqual(Workstatus.objects.count(), 1)
        workstatus = Workstatus.objects.get(pk=workstatus_id)
        self.assertEqual(workstatus.name, self.workstatus_data['name'])
        self.assertEqual(workstatus.description, self.workstatus_data['description'])

        # Get list of work statuses
        list_url = '/api/workstatus/'
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], workstatus_id)

        # Get work status details
        detail_url = f'/api/workstatus/{workstatus_id}'
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], workstatus_id)

        # Update work status
        update_url = f'/api/workstatus/{workstatus_id}/update'
        update_data = {
            'name': 'Completed',
            'description': 'Work has been completed'
        }
        response = self.client.post(update_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        workstatus.refresh_from_db()
        self.assertEqual(workstatus.name, update_data['name'])
        self.assertEqual(workstatus.description, update_data['description'])

        # Delete work status
        delete_url = f'/api/workstatus/{workstatus_id}/delete'
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(Workstatus.objects.count(), 0)

    def test_create_invalid_workstatus(self):
        create_url = '/api/workstatus/create'
        invalid_data = {
            # missing required fields
        }
        response = self.client.post(create_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Workstatus.objects.count(), 0)

    def test_update_nonexistent_workstatus(self):
        update_url = '/api/workstatus/99999/update'
        update_data = {
            'name': 'Updated Status'
        }
        response = self.client.post(update_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_nonexistent_workstatus(self):
        delete_url = '/api/workstatus/99999/delete'
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_duplicate_workstatus(self):
        # Create first work status
        create_url = '/api/workstatus/create'
        response = self.client.post(create_url, self.workstatus_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Try to create work status with same name
        response = self.client.post(create_url, self.workstatus_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 