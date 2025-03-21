import unittest

from flask import json

from openapi_server.models.car import Car  # noqa: E501
from openapi_server.test import BaseTestCase


class TestCarsController(BaseTestCase):
    """CarsController integration test stubs"""

    def test_create_car(self):
        """Test case for create_car

        Car creating method
        """
        car = {"number":"E251MB11","owner_id":2,"model":"Toyota Corolla","vin":"JTNKM28E900090600"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/cars',
            method='POST',
            headers=headers,
            data=json.dumps(car),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_cars_by_owner_id(self):
        """Test case for get_cars_by_owner_id

        Cars getting method by its owner_id
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/cars/{owner_id}'.format(owner_id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_car(self):
        """Test case for update_car

        Car update method
        """
        car = {"number":"E251MB11","owner_id":2,"model":"Toyota Corolla","vin":"JTNKM28E900090600"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/cars/{car_id}'.format(car_id=56),
            method='PUT',
            headers=headers,
            data=json.dumps(car),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
