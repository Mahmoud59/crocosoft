from flask import request, jsonify

from app import db
from vehicles.models import Vehicle
from . import vehicle_bp


@vehicle_bp.route('/vehicles', methods=['POST'])
def create_vehicle():
    data = request.get_json()
    make = data.get('make')
    model = data.get('model')
    category = data.get('category')
    description = data.get('description')
    vehicle = Vehicle(make=make, model=model, category=category, description=description)
    db.session.add(vehicle)
    db.session.commit()
    return jsonify({'id': vehicle.id}), 201


@vehicle_bp.route('/vehicles/<int:id>')
def get_vehicle(id):
    vehicle = Vehicle.query.get_or_404(id)
    return jsonify({
        'id': vehicle.id,
        'make': vehicle.make,
        'model': vehicle.model,
        'category': vehicle.category,
        'description': vehicle.description
    })
