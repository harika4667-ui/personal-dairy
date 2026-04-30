from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from datetime import datetime, date
import os
from config import config
from models import db, User, DiaryEntry, Streak

def create_app(config_name='development'):
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Login required decorator
    def login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please log in first.', 'warning')
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function
    
    # Get current user
    def get_current_user():
        if 'user_id' in session:
            return User.query.get(session['user_id'])
        return None
    
    # Inject current user to all templates
    @app.context_processor
    def inject_user():
        user = get_current_user()
        return {'current_user': user}
    
    # Home page
    @app.route('/')
    def index():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return redirect(url_for('dashboard'))
    
    # Dashboard
    @app.route('/dashboard')
    @login_required
    def dashboard():
        user = get_current_user()
        
        # Get user's streak info
        streak = Streak.query.filter_by(user_id=user.id).first()
        if not streak:
            streak = Streak(user_id=user.id)
            db.session.add(streak)
            db.session.commit()
        
        # Update streak
        current_streak = streak.check_and_update_streak()
        
        # Get all entries for the user, ordered by date
        entries = DiaryEntry.query.filter_by(user_id=user.id).order_by(
            DiaryEntry.created_at.desc()
        ).all()
        
        # Group entries by month
        entries_by_month = {}
        for entry in entries:
            month_key = entry.created_at.strftime('%Y-%m')
            month_label = entry.created_at.strftime('%B %Y')
            if month_key not in entries_by_month:
                entries_by_month[month_key] = {'label': month_label, 'entries': []}
            entries_by_month[month_key]['entries'].append(entry)
        
        # Sort months in reverse chronological order
        sorted_months = sorted(entries_by_month.items(), reverse=True)
        
        total_entries = len(entries)
        
        return render_template('dashboard.html',
                             current_streak=current_streak,
                             longest_streak=streak.longest_streak,
                             total_entries=total_entries,
                             entries_by_month=sorted_months)
    
    # View single entry
    @app.route('/entry/<int:entry_id>')
    @login_required
    def view_entry(entry_id):
        entry = DiaryEntry.query.get_or_404(entry_id)
        
        # Check if user owns this entry
        if entry.user_id != session['user_id']:
            flash('Access denied.', 'danger')
            return redirect(url_for('dashboard'))
        
        return render_template('view_entry.html', entry=entry)
    
    # Add entry page
    @app.route('/add-entry', methods=['GET', 'POST'])
    @login_required
    def add_entry():
        if request.method == 'POST':
            title = request.form.get('title', '').strip() or None
            content = request.form.get('content', '').strip()
            
            if not content:
                flash('Content cannot be empty.', 'danger')
                return redirect(url_for('add_entry'))
            
            entry = DiaryEntry(
                user_id=session['user_id'],
                title=title,
                content=content
            )
            
            db.session.add(entry)
            db.session.commit()
            
            # Update streak
            user = get_current_user()
            streak = Streak.query.filter_by(user_id=user.id).first()
            if not streak:
                streak = Streak(user_id=user.id)
                db.session.add(streak)
                db.session.commit()
            streak.check_and_update_streak()
            
            flash('Entry created successfully!', 'success')
            return redirect(url_for('view_entry', entry_id=entry.id))
        
        return render_template('add_entry.html')
    
    # Edit entry
    @app.route('/edit-entry/<int:entry_id>', methods=['GET', 'POST'])
    @login_required
    def edit_entry(entry_id):
        entry = DiaryEntry.query.get_or_404(entry_id)
        
        # Check if user owns this entry
        if entry.user_id != session['user_id']:
            flash('Access denied.', 'danger')
            return redirect(url_for('dashboard'))
        
        if request.method == 'POST':
            entry.title = request.form.get('title', '').strip() or None
            content = request.form.get('content', '').strip()
            
            if not content:
                flash('Content cannot be empty.', 'danger')
                return redirect(url_for('edit_entry', entry_id=entry.id))
            
            entry.content = content
            entry.updated_at = datetime.utcnow()
            
            db.session.commit()
            flash('Entry updated successfully!', 'success')
            return redirect(url_for('view_entry', entry_id=entry.id))
        
        return render_template('edit_entry.html', entry=entry)
    
    # Delete entry
    @app.route('/delete-entry/<int:entry_id>', methods=['POST'])
    @login_required
    def delete_entry(entry_id):
        entry = DiaryEntry.query.get_or_404(entry_id)
        
        # Check if user owns this entry
        if entry.user_id != session['user_id']:
            flash('Access denied.', 'danger')
            return redirect(url_for('dashboard'))
        
        db.session.delete(entry)
        db.session.commit()
        flash('Entry deleted successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    # Sign up
    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '')
            password_confirm = request.form.get('password_confirm', '')
            
            # Validation
            if not username or not email or not password:
                flash('All fields are required.', 'danger')
                return redirect(url_for('signup'))
            
            if len(username) < 3:
                flash('Username must be at least 3 characters long.', 'danger')
                return redirect(url_for('signup'))
            
            if len(password) < 6:
                flash('Password must be at least 6 characters long.', 'danger')
                return redirect(url_for('signup'))
            
            if password != password_confirm:
                flash('Passwords do not match.', 'danger')
                return redirect(url_for('signup'))
            
            # Check if user exists
            if User.query.filter_by(username=username).first():
                flash('Username already exists.', 'danger')
                return redirect(url_for('signup'))
            
            if User.query.filter_by(email=email).first():
                flash('Email already registered.', 'danger')
                return redirect(url_for('signup'))
            
            # Create user
            user = User(username=username, email=email)
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            
            # Create streak record
            streak = Streak(user_id=user.id)
            db.session.add(streak)
            db.session.commit()
            
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))
        
        return render_template('signup.html')
    
    # Login
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '')
            
            if not username or not password:
                flash('Username and password are required.', 'danger')
                return redirect(url_for('login'))
            
            user = User.query.filter_by(username=username).first()
            
            if not user or not user.check_password(password):
                flash('Invalid username or password.', 'danger')
                return redirect(url_for('login'))
            
            # Set session
            session['user_id'] = user.id
            session.permanent = True
            
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('dashboard'))
        
        return render_template('login.html')
    
    # Logout
    @app.route('/logout')
    def logout():
        session.clear()
        flash('You have been logged out.', 'info')
        return redirect(url_for('login'))
    
    # Settings page
    @app.route('/settings')
    @login_required
    def settings():
        user = get_current_user()
        streak = Streak.query.filter_by(user_id=user.id).first()
        return render_template('settings.html', streak=streak)
    
    # Change password
    @app.route('/change-password', methods=['POST'])
    @login_required
    def change_password():
        user = get_current_user()
        old_password = request.form.get('old_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        if not old_password or not new_password or not confirm_password:
            flash('All fields are required.', 'danger')
            return redirect(url_for('settings'))
        
        if not user.check_password(old_password):
            flash('Current password is incorrect.', 'danger')
            return redirect(url_for('settings'))
        
        if len(new_password) < 6:
            flash('New password must be at least 6 characters long.', 'danger')
            return redirect(url_for('settings'))
        
        if new_password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('settings'))
        
        user.set_password(new_password)
        db.session.commit()
        
        flash('Password changed successfully!', 'success')
        return redirect(url_for('settings'))
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def server_error(error):
        db.session.rollback()
        return render_template('500.html'), 500
    
    return app

if __name__ == '__main__':
    app = create_app(os.environ.get('FLASK_ENV', 'development'))
    app.run(debug=True,host='0.0.0.0', port=5000)
