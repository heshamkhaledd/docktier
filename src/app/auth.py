from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user
from werkzeug.security import generate_password_hash, check_password_hash
import bcrypt
from .models import User
from . import db, login_manager
import json
from sqlalchemy import func

auth_bp = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            login_user(user)
            return redirect(url_for('main.products'))
        else:
            flash('Invalid email or password')
    return render_template('login.html')


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone = request.form['phone']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        address = {
            "street": request.form['street'],
            "city": request.form['city'],
            "zip": request.form['zip']
        }

        if password != confirm_password:
            flash("Passwords do not match.")
            return redirect(url_for('auth.signup'))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered.")
            return redirect(url_for('auth.signup'))

        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        new_id = (db.session.query(func.max(User.id)).scalar() or 0) + 1
        user = User(
            id = new_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            password=hashed_pw,
            address=address
        )
        db.session.add(user)
        db.session.commit()
        flash("Account created. Please log in.")
        return redirect(url_for('auth.login'))

    return render_template('signup.html')
