from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .machine import Machine
from .log import Log
