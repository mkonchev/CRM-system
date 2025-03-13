from ..extentions import db


class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id', ondelete='CASCADE'))
    services = db.Column(db.String(50))
    checkpoints = db.Column(db.String(50))  # to json type?
    worker_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
