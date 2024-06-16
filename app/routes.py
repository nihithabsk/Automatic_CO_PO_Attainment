from flask import render_template, request, redirect, url_for, flash
from app import app, db
from app.models import CalculationResult
import pandas as pd
from app.utils import cal
from app.avg_cal import average_calculator
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import RegistrationForm, LoginForm
from app.models import User
from app.po import po
@app.route('/history')
@login_required
def history():
    results = CalculationResult.query.filter_by(user_id=current_user.id).all()
    return render_template('history.html', results=results)
@app.route('/avgcal', methods=['POST'])
@login_required
def average():
    mid1 = float(request.form['mid1'])
    mid2 = float(request.form['mid2'])
    answer = average_calculator(mid1, mid2)
    return render_template('avg_result.html', avg=answer)

@app.route('/average')
@login_required
def av():
    return render_template('avg.html')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
@login_required
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
    if len(sheet_name) > 50:
        sheet_name = sheet_name[:50]
    file_path = "uploaded_file.xlsx"
    file.save(file_path)

    avg, ans, avg_cos, avg_co_levels,sheet_name = cal(file_path, sheet_name, class_strength,co_mappings)

    result = CalculationResult(user_id=current_user.id, average=avg, level=ans, avg_cos=avg_cos, avg_co_levels=avg_co_levels, sheet_name=sheet_name)
    db.session.add(result)
    db.session.commit()

    return render_template('result.html', average=avg, level=ans, avg_cos=avg_cos,avg_co_levels = avg_co_levels)
@app.route('/check_db')
def check_db():
    results = CalculationResult.query.all()
    data = [{"id": result.id, "average": result.average, "level": result.level, "avg_cos": result.avg_cos, "avg_co_levels": result.avg_co_levels,"sheet_name": result.sheet_name} for result in results]
    return {"results": data}
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, role=form.role.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
@app.route('/pocal', methods=['GET', 'POST'])
@login_required
def po_calculate():
    if request.method == 'POST':
        file = request.files['file']
        sheet_name = request.form['sheet_name']
        file_path = "uploaded_po_file.xlsx"
        file.save(file_path)

        avg_of_pos = po(file_path, sheet_name)

        result = CalculationResult(user_id=current_user.id, average=0, level='', avg_cos={}, avg_co_levels=avg_of_pos, sheet_name=sheet_name)
        db.session.add(result)
        db.session.commit()

        return render_template('po_result.html', avg_of_pos=avg_of_pos, sheet_name=sheet_name)
    return render_template('po_form.html')
