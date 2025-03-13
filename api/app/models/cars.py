from .orders import Orders
from ..extentions import db


class Cars(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(50))
    model = db.Column(db.String(50))
    vin = db.Column(db.String(50))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))

    orders_car = db.relationship(Orders, backref='cars')
