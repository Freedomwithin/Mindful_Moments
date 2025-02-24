from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, abort, current_app
from flask_login import login_required, current_user
from ..extensions import db
from ..models import JournalEntry  # Assuming this is your model
from ..helpers import mood_to_value, analyze_sentiment, get_gratitude_suggestions, get_random_quote, generate_ai_insights
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
import logging
import traceback

main = Blueprint('main', __name__)
logger = logging.getLogger(__name__)

@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    try:
        quote = get_random_quote()

        page = request.args.get('page', 1, type=int)
        entries = JournalEntry.query.filter_by(user_id=current_user.id).order_by(JournalEntry.date.desc()).paginate(page=page, per_page=10)

        all_entries = JournalEntry.query.filter_by(user_id=current_user.id).order_by(JournalEntry.date.asc()).all()
        dates = [entry.date.strftime('%Y-%m-%d') for entry in all_entries]
        mood_values = [mood_to_value(entry.mood) for entry in all_entries]

        ai_suggestions = generate_ai_insights(all_entries) if all_entries else []

        return render_template('index.html',
                               entries=entries,
                               quote=quote,
                               dates=dates,
                               mood_values=mood_values,
                               ai_suggestions=ai_suggestions)

    except Exception as e:
        logger.error(f"Error in index route: {str(e)}")
        logger.error(traceback.format_exc())
        flash('An error occurred while loading the page. Please try again.', 'error')
        return redirect(url_for('main.index'))

@main.route('/add_entry', methods=['POST'])
@login_required
def add_entry():
    if request.method == 'POST':
        content = request.form.get('content')
        mood = request.form.get('mood')
        category = request.form.get('category')
        date_str = request.form.get('date')

        if not content:
            logger.warning(f"Add entry attempt with empty content by user {current_user.id}")
            return jsonify({'error': 'Content cannot be empty'}), 400

        if mood not in ['Sad', 'Neutral', 'Calm', 'Grateful', 'Happy', 'Excited']:
            logger.warning(f"Add entry attempt with invalid mood '{mood}' by user {current_user.id}")
            return jsonify({'error': 'Invalid mood'}), 400

        if category not in ['Personal', 'Work', 'Family', 'Health', 'Relationships', 'Other']:
            logger.warning(f"Add entry attempt with invalid category '{category}' by user {current_user.id}")
            return jsonify({'error': 'Invalid category'}), 400

        try:
            entry_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            new_entry = JournalEntry(
                content=content,
                mood=mood,
                date=entry_date,
                category=category,
                user_id=current_user.id
            )
            db.session.add(new_entry)
            db.session.commit()
            logger.info(f"New entry added successfully for user {current_user.id}")

            # Return the JSON response with message and redirect
            return jsonify({
                'message': 'Entry added successfully',
                'redirect': url_for('main.index') 
            }), 200 

        except ValueError as ve:
            logger.error(f"ValueError in add_entry: {str(ve)}, Date string: {date_str}")
            return jsonify({'error': 'Invalid date format. Please use YYYY-MM-DD.'}), 400
        except SQLAlchemyError as se:
            db.session.rollback()
            logger.error(f"SQLAlchemyError in add_entry: {str(se)}")
            return jsonify({'error': 'Database error occurred'}), 500
        except Exception as e:
            db.session.rollback()
            logger.error(f"Unexpected error in add_entry: {str(e)}")
            logger.error(traceback.format_exc())
            return jsonify({'error': 'An unexpected error occurred'}), 500

    return jsonify({'message': 'Invalid request method'}), 405  # Only allow POST

@main.route('/edit_entry/<int:entry_id>', methods=['GET', 'POST'])
@login_required
def edit_entry(entry_id):
    entry = JournalEntry.query.get_or_404(entry_id)
    if entry.user_id != current_user.id:
        abort(403)

    if request.method == 'POST':
        entry.content = request.form.get('content')
        entry.mood = request.form.get('mood')
        entry.date = request.form.get('date')
        entry.category = request.form.get('category')

        try:
            entry.date = datetime.strptime(entry.date, '%Y-%m-%d')
            db.session.commit()
            flash('Entry updated successfully!', 'success')
            return redirect(url_for('main.index'))
        except ValueError:
            flash('Invalid date format. Please use YYYY-MM-DD.', 'danger')
            return render_template('edit_entry.html', entry=entry)
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error during edit: {e}")
            flash('An error occurred while updating the entry.', 'danger')
            return render_template('edit_entry.html', entry=entry)

    else:
        return render_template('edit_entry.html', entry=entry)

@main.route('/delete_entry/<int:entry_id>', methods=['POST'])
@login_required
def delete_entry(entry_id):
    entry = JournalEntry.query.get_or_404(entry_id)
    if entry.user_id != current_user.id:
        abort(403)
    try:
        db.session.delete(entry)
        db.session.commit()
        flash('Your entry has been deleted.', 'success')
    except Exception as e:
        logger.error(f"Error in delete_entry route: {str(e)}")
        logger.error(traceback.format_exc())
        db.session.rollback()
        flash('An error occurred while deleting the entry. Please try again.', 'danger')
    return redirect(url_for('main.index'))

@main.route('/mood_chart')
@login_required
def mood_chart():
    entries = JournalEntry.query.filter_by(user_id=current_user.id).order_by(JournalEntry.date).all()
    dates = [entry.date.strftime('%Y-%m-%d') for entry in entries]
    mood_values = [mood_to_value(entry.mood) for entry in entries]
    
    return render_template('mood_chart.html', dates=dates, mood_values=mood_values)

@main.route('/get_mood_data', methods=['GET'])
@login_required
def get_mood_data():
    try:
        entries = JournalEntry.query.filter_by(user_id=current_user.id).order_by(JournalEntry.date).all()
        data = [{'date': entry.date.strftime('%Y-%m-%d'), 'mood': entry.mood} for entry in entries]
        return jsonify(data)
    except Exception as e:
        logger.error(f"Error in get_mood_data route: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': 'An error occurred while fetching mood data'}), 500

@main.route('/ai_insights')
@login_required
def ai_insights():
    all_entries = JournalEntry.query.filter_by(user_id=current_user.id).order_by(JournalEntry.date.asc()).all()
    ai_suggestions = generate_ai_insights(all_entries) if all_entries else []
    generation_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return render_template('ai_insights.html', 
                           ai_suggestions=ai_suggestions, 
                           generation_time=generation_time)

@main.app_errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@main.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500