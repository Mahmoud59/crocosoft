from app import db


class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    category = db.Column(db.Enum('small', 'family', 'van'), nullable=False)
    category_rate = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=False)
