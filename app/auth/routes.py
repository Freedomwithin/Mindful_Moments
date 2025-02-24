from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.exc import SQLAlchemyError
from ..models import User
from ..extensions import db
from .forms import LoginForm, RegistrationForm
from werkzeug.security import check_password_hash, generate_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    current_app.logger.info(f"Login attempt: Method={request.method}")

    if form.validate_on_submit():
        try:
            user = User.query.filter_by(username=form.username.data).first()
            current_app.logger.info(f"User found: {user is not None}")
            
            if user and check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                current_app.logger.info(f"User {user.username} logged in successfully")
                current_app.logger.info(f"Is authenticated: {current_user.is_authenticated}")
                next_page = request.args.get('next')
                current_app.logger.info(f"Redirecting to: {next_page or url_for('main.index')}")
                return redirect(next_page or url_for('main.index'))
            else:
                flash('Invalid username or password', 'danger')
                current_app.logger.warning(f"Failed login attempt for username: {form.username.data}")
        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error during login: {str(e)}")
            flash('An error occurred. Please try again.', 'danger')
    else:
        current_app.logger.info("Form validation failed or GET request")
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {getattr(form, field).label.text}: {error}", 'danger')
                current_app.logger.info(f"Form error: {field} - {error}")

    return render_template('login.html', form=form)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    current_app.logger.info(f"Signup attempt: Method={request.method}")

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('That username is already taken. Please choose a different one.', 'danger')
            current_app.logger.info(f"Signup attempt with existing username: {username}")
            return redirect(url_for('auth.signup'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password_hash=hashed_password)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Your account has been created! Please log in.', 'success')
            current_app.logger.info(f"New user created: {username}")
            return redirect(url_for('auth.login'))
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error(f"Signup error: {str(e)}")
            flash('An error occurred during signup. Please try again.', 'danger')
    else:
        current_app.logger.info("Form validation failed or GET request")
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {getattr(form, field).label.text}: {error}", 'danger')
                current_app.logger.info(f"Form error: {field} - {error}")

    return render_template('signup.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    username = current_user.username
    logout_user()
    flash('You have been logged out.', 'info')
    current_app.logger.info(f"User {username} logged out")
    return redirect(url_for('main.index'))