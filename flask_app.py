import os
import logging
from flask import Flask, request, render_template, redirect, url_for, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from textblob import TextBlob
import joblib
from config import Config
from extensions import db, migrate, login_manager
from models import User, JournalEntry

# Configure logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Database configuration
database_url = os.environ.get('DATABASE_URL')
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///instance/journal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Load the rest of the configuration
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)
login_manager.login_view = 'login'

# Load the trained model
loaded_model = joblib.load('gratitude_model.joblib')

# Log database URL and debug mode
logging.info(f"Database URL: {app.config['SQLALCHEMY_DATABASE_URI']}")
logging.info(f"Debug mode: {app.config['DEBUG']}")

# Helper functions
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def mood_to_value(mood):
    mood_values = {
        'Sad': 1,
        'Neutral': 3,
        'Calm': 3,
        'Grateful': 4,
        'Happy': 5,
        'Excited': 5
    }
    return mood_values.get(mood, 3)  # Default to Neutral if mood not found

def get_gratitude_suggestions(prompt):
    try:
        suggestions = loaded_model.predict([prompt])
        return suggestions
    except Exception as e:
        logging.error(f"Error generating suggestions: {e}")
        return ["Unable to generate suggestions at this time."]

def analyze_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        entries = JournalEntry.query.filter_by(user_id=current_user.id).order_by(JournalEntry.date.desc()).all()
        return render_template('index.html', entries=entries)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists')
        else:
            new_user = User(username=username, password=generate_password_hash(password))
            try:
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                return redirect(url_for('index'))
            except SQLAlchemyError as e:
                db.session.rollback()
                flash('An error occurred. Please try again.')
                logging.error(f"Database error: {str(e)}")
    return render_template('register.html')

@app.route('/add_entry', methods=['GET', 'POST'])
@login_required
def add_entry():
    if request.method == 'POST':
        content = request.form.get('content')
        mood = request.form.get('mood')
        date = request.form.get('date')
        sentiment_score = analyze_sentiment(content)
        suggestions = get_gratitude_suggestions(content)
        
        new_entry = JournalEntry(
            content=content, 
            mood=mood, 
            date=datetime.strptime(date, '%Y-%m-%d'),
            user_id=current_user.id, 
            sentiment_score=sentiment_score
        )
        
        try:
            db.session.add(new_entry)
            db.session.commit()
            return render_template('entry_added.html', sentiment_score=sentiment_score, suggestions=suggestions)
        except SQLAlchemyError as e:
            db.session.rollback()
            flash('An error occurred. Please try again.')
            logging.error(f"Database error: {str(e)}")
    
    return render_template('add_entry.html')

@app.route('/mood_chart')
@login_required
def mood_chart():
    entries = JournalEntry.query.filter_by(user_id=current_user.id).order_by(JournalEntry.date).all()
    dates = [entry.date.strftime('%Y-%m-%d') for entry in entries]
    mood_values = [mood_to_value(entry.mood) for entry in entries]
    return render_template('chart.html', dates=dates, mood_values=mood_values)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# API routes
@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.form
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        login_user(user)
        return jsonify({"success": True, "message": "Logged in successfully"})
    return jsonify({"success": False, "message": "Invalid username or password"}), 401

@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.form
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({"success": False, "message": "Username already exists"}), 400
    new_user = User(username=username, password=generate_password_hash(password))
    try:
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return jsonify({"success": True, "message": "Registered successfully"})
    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error(f"Database error: {str(e)}")
        return jsonify({"success": False, "message": "An error occurred. Please try again."}), 500

@app.route('/api/add_entry', methods=['POST'])
@login_required
def api_add_entry():
    data = request.form
    content = data.get('content')
    mood = data.get('mood')
    sentiment_score = analyze_sentiment(content)
    new_entry = JournalEntry(content=content, mood=mood, user_id=current_user.id, sentiment_score=sentiment_score)
    try:
        db.session.add(new_entry)
        db.session.commit()
        return jsonify({"success": True, "message": "Entry added successfully"})
    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error(f"Database error: {str(e)}")
        return jsonify({"success": False, "message": "An error occurred. Please try again."}), 500

@app.route('/api/entries')
@login_required
def api_entries():
    entries = JournalEntry.query.filter_by(user_id=current_user.id).order_by(JournalEntry.date.desc()).all()
    return jsonify({
        "entries": [
            {
                "id": entry.id,
                "content": entry.content,
                "mood": entry.mood,
                "date": entry.date.isoformat(),
                "sentiment_score": entry.sentiment_score
            } for entry in entries
        ]
    })

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"}), 200

# Initialize Flask-Migrate
with app.app_context():
    if db.engine.url.drivername == 'sqlite':
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    try:
        app.run(host='0.0.0.0', port=port)
    except Exception as e:
        print(f"An error occurred: {e}")
        logging.exception("An error occurred while running the app")