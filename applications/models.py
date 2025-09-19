from .database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    full_name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(255), nullable=True)
    pin_code = db.Column(db.Integer, nullable=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)

    reservation = db.relationship('Reservation', backref='user', lazy=True)

class ParkingLot(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lot_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    max_spots = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    pincode = db.Column(db.Integer, nullable=False)

    spots = db.relationship('ParkingSpot', backref='parking_lot', cascade='all, delete', lazy=True)

class ParkingSpot(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'),  nullable=False)
    status = db.Column(db.String(1), nullable=False)

    reservations = db.relationship('Reservation', backref='spot', lazy=True)

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.id'), nullable=False)
    vehicle_num = db.Column(db.String(20), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=True)
    price = db.Column(db.Float, nullable=False)    