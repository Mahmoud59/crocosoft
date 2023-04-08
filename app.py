from flask import Flask
from flask_sqlalchemy import SQLAlchemy


SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1234@localhost/car_hire'

# Initialize the Flask app
app = Flask(__name__)

# Load the configuration from config.py
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/car_hire'

# Initialize the database
db = SQLAlchemy(app)

# Import the routes (you will need to create these)
from customers.routes import customer_bp
from vehicles.routes import vehicle_bp
from booking.routes import booking_bp

# Register the blueprints
app.register_blueprint(customer_bp, url_prefix='/customers')
app.register_blueprint(vehicle_bp, url_prefix='/vehicles')
app.register_blueprint(booking_bp, url_prefix='/booking')

# Start the development server if running directly
if __name__ == '__main__':
    app.run()
