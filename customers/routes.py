from flask import request, jsonify
from . import customer_bp
from .models import db, Customer


@customer_bp.route('/', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    result = []
    for customer in customers:
        customer_data = {
            'id': customer.id,
            'name': customer.name,
            'email': customer.email,
            'phone': customer.phone
        }
        result.append(customer_data)
    return jsonify(result)


@customer_bp.route('/', methods=['POST'])
def create_customer():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    address = data.get('address')
    customer = Customer(name=name, email=email, phone=phone, address=address)
    db.session.add(customer)
    db.session.commit()
    return jsonify({'id': customer.id}), 201


@customer_bp.route('/<int:id>')
def get_customer(id):
    customer = Customer.query.get_or_404(id)
    return jsonify({
        'id': customer.id,
        'name': customer.name,
        'email': customer.email,
        'phone': customer.phone,
        'address': customer.address
    })


@customer_bp.route('/<int:id>', methods=['PUT'])
def update_customer(id):
    customer = Customer.query.get(id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404

    # Update customer information from request body
    data = request.get_json()
    customer.name = data.get('name', customer.name)
    customer.email = data.get('email', customer.email)
    customer.phone = data.get('phone', customer.phone)

    # Save changes to database
    db.session.commit()

    return jsonify({'message': 'Customer updated successfully', 'customer': customer.to_dict()})


@customer_bp.route('/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = Customer.query.get(id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404

    # Delete customer from database
    db.session.delete(customer)
    db.session.commit()

    return jsonify({'message': 'Customer deleted successfully'})
