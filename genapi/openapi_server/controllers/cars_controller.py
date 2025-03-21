import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from genapi.openapi_server.models.car import Car  # noqa: E501
from genapi.openapi_server import util

from api.app.models.cars import Cars
from api.app.extentions import db


def create_car(body) -> Car:  # noqa: E501
    """Car creating method

    role: admin, worker, user # noqa: E501

    :param car:
    :type car: dict | bytes

    :rtype: Union[Car, Tuple[Car, int], Tuple[Car, int, Dict[str, str]]
    """
    car = body
    if connexion.request.is_json:
        car_dto = connexion.request.get_json()  # noqa: E501
        car_db = Cars(
            number=car_dto.get('number'),
            model=car_dto.get('model'),
            vin=car_dto.get('vin'),
            owner_id=car_dto.get('owner_id')
        )
        db.session.add(car_db)
        db.session.commit()
        return car_db
    return 400


def get_cars_by_owner_id(owner_id):  # noqa: E501
    """Cars getting method by its owner_id

    role: admin, worker # noqa: E501

    :param owner_id: User identifier to find user cars
    :type owner_id: int

    :rtype: Union[List[Car], Tuple[List[Car], int], Tuple[List[Car], int, Dict[str, str]]
    """
    return 'do some magic!'


def update_car(car_id, body=None):  # noqa: E501
    """Car update method

    role: admin, worker # noqa: E501

    :param car_id: Car identifier needs to be updated
    :type car_id: int
    :param car: 
    :type car: dict | bytes

    :rtype: Union[Car, Tuple[Car, int], Tuple[Car, int, Dict[str, str]]
    """
    car = body
    if connexion.request.is_json:
        car = Car.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
