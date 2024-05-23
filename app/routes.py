from flask import render_template, request, redirect, url_for
from app import app, db
from app.models import COAttainment, CalculationResult
import pandas as pd
from app.utils import cal

@app.route('/history')
def history():
    results = CalculationResult.query.all()
    return render_template('history.html', results=results)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    class_strength = int(request.form['class_strength'])
    co_mappings_input = request.form['co_mappings']
    co_mappings = {}

    for co_mapping in co_mappings_input.split(';'):
        parts = co_mapping.split(':')
        if len(parts) == 2:
            co, questions = parts
            co_mappings[co.strip()] = [q.strip() for q in questions.split(',')]
        else:
            return "Invalid CO mappings format", 400

    file = request.files['file']
    sheet_name = request.form['sheet_name'] 
    file_path = "uploaded_file.xlsx"
    file.save(file_path)

    avg, ans, avg_cos,avg_co_levels = cal(file_path, sheet_name, class_strength, co_mappings)

    return render_template('result.html', average=avg, level=ans, avg_cos=avg_cos,avg_co_levels = avg_co_levels)

    result = CalculationResult(average=avg, level=ans)
    db.session.add(result)
    db.session.commit()

    return render_template('result.html', average=avg, level=ans)
