# Flask Bootstrap I2C Regwizard App

This project is a Flask web application that allows users to input I2C messages, process them using a custom Python script, and download the processed files. The application uses Bootstrap for the frontend and supports user authentication and environment-based configuration.
## Features

- User authentication with credentials stored in environment variables.
- Input I2C messages through a web form with validation for proper I2C command format.
- Validation ensures only one of ADDR_H/DATA_H or ADDR_L/DATA_L pairs are provided per message.
- Select specific messages to process using a custom script (ces_i2c_regwizard.py).
- Download processed files in .vhd format or other supported formats.
- Environment-based configuration using .env files.

## Prerequisites

Before running this project locally, ensure you have the following installed:

- Python 3.7+
- `pip` (Python package installer)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/lpvera22/tcl_to_python.git
cd tcl_to_python
```
### 2. Create and Activate a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Set Up Environment Variables
```bash
touch .env
```
Add the following environment variables to the .env file:
```bash
# Flask configuration
FLASK_ENV=development
FLASK_APP=app.py
SECRET_KEY=supersecretkey

# Database configuration
SQLALCHEMY_DATABASE_URI=sqlite:///flask_bootstrap_app.db

# Example user credentials
ADMIN_USERNAME=admin
ADMIN_PASSWORD=password123
```
### 5. Initialize the Database
```bash
flask shell
```
In the Flask shell, run:
```bash
from app import db
db.create_all()
exit()
```
### 5.1 Apply Migrations
After initializing the database, apply any existing migrations:
```bash
flask db upgrade
```
### 6. Run the Application
```bash
flask run
```
### 7. Usage
- Login: Use the credentials specified in your .env file to log in.
- Input I2C Messages: Add I2C messages through the provided web form. Ensure that you only use one combination of ADDR_H/DATA_H or ADDR_L/DATA_L. The command must be either W (write) or R (read).
- Select Messages for Processing: Before processing, select the specific messages you want to include in the output file.
- Process Messages: Click the "Generate and Process File" button to process the selected I2C messages.
- Download Processed Files: After processing, a download link will be provided for the generated .vhd or other file formats.

### 8. Usage
The project includes test cases to validate functionality, such as ensuring proper message handling and file generation:

- Add Message with Validation: Tests ensure that only valid commands (W or R) and address/data pairs (ADDR_H/DATA_H or ADDR_L/DATA_L) are accepted.
- Select and Process Messages: Tests ensure that only selected messages are processed and included in the generated file.

### 9. Troubleshooting
If you encounter any issues:

- Check the logs for detailed error messages.
- Ensure that all environment variables are correctly set in the .env file.
- Verify that the database is properly initialized and accessible.