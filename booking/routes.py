from flask import request, jsonify
from datetime import datetime, timedelta

from app import db
from booking.models import Booking
from customers.models import Customer
from vehicles.models import Vehicle
from . import booking_bp


@booking_bp.route('/booking', methods=['POST'])
def create_booking():
    data = request.get_json()
    customer_id = data.get('customer_id')
    vehicle_id = data.get('vehicle_id')
    hire_date_str = data.get('hire_date')
    return_date_str = data.get('return_date')

    customer = Customer.query.get_or_404(customer_id)
    vehicle = Vehicle.query.get_or_404(vehicle_id)

    hire_date = datetime.strptime(hire_date_str, '%Y-%m-%d').date()
    return_date = datetime.strptime(return_date_str, '%Y-%m-%d').date()

    # Check if the booking duration is not more than a week
    if (return_date - hire_date).days > 7:
        return jsonify({'error': 'The booking duration cannot be more than a week.'}), 400

    # Check if the vehicles is available for the booking period
    bookings = Booking.query.filter_by(vehicle_id=vehicle_id).all()
    for booking in bookings:
        if hire_date <= booking.return_date and return_date >= booking.hire_date:
            return jsonify({'error': 'The vehicles is not available for the selected booking period.'}), 400

    booking = Booking(customer=customer, vehicle=vehicle, hire_date=hire_date, return_date=return_date)
    db.session.add(booking)
    db.session.commit()

    # Create invoice
    amount = (return_date - hire_date).days * vehicle.category_rate
    invoice = {
        'customer_name': customer.name,
        'customer_email': customer.email,
        'vehicle_make': vehicle.make,
        'vehicle_model': vehicle.model,
        'hire_date': hire_date_str,
        'return_date': return_date_str,
        'amount': amount
    }

    # Send confirmation letter if the booking is made in advance
    if hire_date > datetime.now().date():
        # TODO: Send confirmation letter
        pass

    return jsonify({'id': booking.id, 'invoice': invoice}), 201


@booking_bp.route('/booking/<int:id>')
def get_booking(id):
    booking = Booking.query.get_or_404(id)
    return jsonify({
        'id': booking.id,
        'customer_id': booking.customer_id,
        'vehicle_id': booking.vehicle_id,
        'hire_date': booking.hire_date.isoformat(),
        'return_date': booking.return_date.isoformat()
    })


@booking_bp.route('/booking/day/<date>')
def get_bookings_for_day(date):
    bookings = Booking.query.filter_by(hire_date=datetime.strptime(date, '%Y-%m-%d').date()).all()
    result = []
    for booking in bookings:
        result.append({
            'id': booking.id,
            'customer_name': booking.customer.name,
            'vehicle_make': booking.vehicle.make,
            'vehicle_model': booking.vehicle.model
        })
    return jsonify(result)
