import logging
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import joblib
from textblob import TextBlob
from config import Config

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__, static_folder="static")
app.config.from_object(Config)

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    journal_entries = db.relationship('JournalEntry', backref='author', lazy=True)

# Journal Entry model
class JournalEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    mood = db.Column(db.String(100), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sentiment_score = db.Column(db.Float, nullable=True)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

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

# Load the trained model
loaded_model = joblib.load('gratitude_model.joblib')

def get_gratitude_suggestions(prompt):
    try:
        suggestions = loaded_model.predict([prompt])
        return suggestions
    except Exception as e:
        print(f"Error generating suggestions: {e}")
        return ["Unable to generate suggestions at this time."]

def analyze_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

# Route definitions
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
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/add_entry', methods=['GET', 'POST'])
@login_required
def add_entry():
    if request.method == 'POST':
        content = request.form.get('content')
        mood = request.form.get('mood')
        sentiment_score = analyze_sentiment(content)
        new_entry = JournalEntry(content=content, mood=mood, user_id=current_user.id, sentiment_score=sentiment_score)
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('index'))
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
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user)
    return jsonify({"success": True, "message": "Registered successfully"})

@app.route('/api/add_entry', methods=['POST'])
@login_required
def api_add_entry():
    data = request.form
    content = data.get('content')
    mood = data.get('mood')
    sentiment_score = analyze_sentiment(content)
    new_entry = JournalEntry(content=content, mood=mood, user_id=current_user.id, sentiment_score=sentiment_score)
    db.session.add(new_entry)
    db.session.commit()
    return jsonify({"success": True, "message": "Entry added successfully"})

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