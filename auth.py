from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from flask_login import login_user, logout_user, login_required
from models import db

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        user = User.query.filter_by(email=email).first()
        try:
            user_role = user.role
        except:
            flash('Please Signup first')

        if not user:
            flash('Please sign up first!')
            return redirect(url_for('auth.signup'))
        elif check_password_hash(user.password, password):
            login_user(user, remember=remember)
            if user_role == 'patient':
                return redirect(url_for('main.patient'))
            elif user_role == 'doctor':
                return redirect(url_for('main.doctor'))
            else:
                flash('Please check your login details and try again.')
                return redirect(url_for('auth.login'))
        else:
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        role = request.form.get('role')
        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exists')
            return redirect(url_for('auth.signup'))
        new_user = User(email=email, name=name, password=generate_password_hash(password, method='SHA256'), role=role)

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
