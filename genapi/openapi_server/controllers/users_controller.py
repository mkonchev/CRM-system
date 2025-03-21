import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from genapi.openapi_server.models.user import User  # noqa: E501
from genapi.openapi_server import util

from api.app.models.users import Users
from api.app.extentions import db


def create_user(body):  # noqa: E501
    """User creating Method

    role: admin, worker # noqa: E501

    :param user: 
    :type user: dict | bytes

    :rtype: Union[User, Tuple[User, int], Tuple[User, int, Dict[str, str]]
    """
    user = body
    if connexion.request.is_json:
        user_dto = connexion.request.get_json()  # noqa: E501
        user_db = Users(
            first_name=user_dto.get('first_name'),
            second_name=user_dto.get('second_name'),
            phone_number=user_dto.get('phone_number'),
            email=user_dto.get('email'),
            tg_login=user_dto.get('tg_login'),
            role=user_dto.get('role')
        )
        db.session.add(user_db)
        db.session.commit()
        return user_db
    return 400


def get_users(first_name=None, second_name=None):  # noqa: E501
    """Users getting method with filtering by first_name &amp; second_name

    role: admin, worker # noqa: E501

    :param first_name: filter by first_name
    :type first_name: str
    :param second_name: filter by second_name
    :type second_name: str

    :rtype: Union[List[User], Tuple[List[User], int], Tuple[List[User], int, Dict[str, str]]
    """
    return 'do some magic!'


def update_user(user_id, body=None):  # noqa: E501
    """User update method

    role: admin, worker # noqa: E501

    :param user_id: User identifier needs to be updated
    :type user_id: int
    :param user: 
    :type user: dict | bytes

    :rtype: Union[User, Tuple[User, int], Tuple[User, int, Dict[str, str]]
    """
    user = body
    if connexion.request.is_json:
        user = User.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
