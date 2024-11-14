import json
import logging
import os
import stat
import shutil
import subprocess
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
from flask_migrate import Migrate
from flask import jsonify
from models import db, User, Machine, Log

# Load environment variables from .env file
load_dotenv()

# Set up basic logging configuration
logging.basicConfig(level=logging.DEBUG,  # Set to DEBUG to capture all messages
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler()])
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)
migrate = Migrate(app, db)
# Create the database and tables
with app.app_context():
    db.create_all()

# Add a test user using credentials from the .env file
admin_username = os.getenv('ADMIN_USERNAME')
admin_password = os.getenv('ADMIN_PASSWORD')

test_user = User(username=admin_username)

with app.app_context():
    if not User.query.filter_by(username=admin_username).first():
        db.session.add(test_user)
        db.session.commit()

@app.route('/')
def index():
    if "username" in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json  # Retrieve JSON data from the request body

    # Extract username and password from the JSON payload
    username = data.get('username')
    password = data.get('password')

    # Check if the user exists and verify the password
    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        return jsonify(success=True, user_id=user.id, role=user.role)
    else:
        return jsonify(success=False)  # Return false if login fails

@app.route('/api/print', methods=['POST'])
def print_transaction():
    data = request.json  # Retrieve JSON data from the request body

    # Extract fields from the JSON payload
    machine_id = data.get('machine_id')
    pda_id = data.get('pda_id')
    employee_id = data.get('employee_id')
    manager_id = data.get('manager_id')
    amount = data.get('amount')
    description = data.get('description')
    timestamp_str = data.get('timestamp')

    # Parse timestamp from string to datetime object if necessary
    try:
        timestamp = datetime.strptime(timestamp_str, '%m/%d/%Y')
    except ValueError:
        return jsonify(success=False, message="Invalid timestamp format"), 400

    # Create a new Transaction record
    new_transaction = Log(
        machine_id=machine_id,
        pda_id=pda_id,
        employee_id=int(employee_id),
        manager_id=int(manager_id),
        amount=float(amount),
        description=description,
        timestamp=timestamp
    )

    # Add and commit the new record to the database
    try:
        db.session.add(new_transaction)
        db.session.commit()
        return jsonify(success=True, message="Transaction saved successfully")
    except Exception as e:
        db.session.rollback()
        return jsonify(success=False, message="Database error", error=str(e)), 500

@app.route('/edit_register/<int:register_id>', methods=['GET', 'POST'])
def edit_register(register_id):
    if 'username' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('login'))

    register = Register.query.get_or_404(register_id)
    return render_template('edit_register.html', register=register)

if __name__ == "__main__":
    app.run(debug=True)
