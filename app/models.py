from app import db

class COAttainment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    co_name = db.Column(db.String(100), nullable=False)
    questions = db.Column(db.String(100), nullable=False)
    print(id,co_name,questions)

class CalculationResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    average = db.Column(db.Float, nullable=False)
    level = db.Column(db.String(20), nullable=False)
