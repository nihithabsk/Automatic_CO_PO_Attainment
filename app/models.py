import json
from sqlalchemy.types import TypeDecorator, VARCHAR
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class JSONEncodedDict(TypeDecorator):
    impl = VARCHAR(1024)

    def process_bind_param(self, value, dialect):
        if value is None:
            return '{}'
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        return json.loads(value)

class CalculationResult(db.Model):
    __tablename__ = 'calculation_result'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('results', lazy=True))
    sheet_name = db.Column(db.String(255), nullable=False)
    average = db.Column(db.Float, nullable=False)
    level = db.Column(db.String(20), nullable=False)
    avg_cos = db.Column(JSONEncodedDict(1024), nullable=False)
    avg_co_levels = db.Column(JSONEncodedDict(1024), nullable=False)


class COAttainment(db.Model):
    __tablename__ = 'co_attainment'
    id = db.Column(db.Integer, primary_key=True)
    co_name = db.Column(db.String(100), nullable=False)
    questions = db.Column(db.String(100), nullable=False)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False) 

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)