from .cars import Cars
from .orders import Orders
from ..extentions import db, DefaultMeta


BaseModel: DefaultMeta = db.Model

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    second_name = db.Column(db.String(50))
    phone_number = db.Column(db.String(50))
    email = db.Column(db.String(50))
    tg_login = db.Column(db.String(50))
    role = db.Column(db.String(50))  # add enum and change

    orders_owner = db.relationship(Orders, backref='users')
    orders_worker = db.relationship(Orders, backref='users')
    cars_owner = db.relationship(Cars, backref='users')
