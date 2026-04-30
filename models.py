from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date

db = SQLAlchemy()

class User(db.Model):
    """User model for authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    entries = db.relationship('DiaryEntry', backref='author', lazy='dynamic', cascade='all, delete-orphan')
    streak = db.relationship('Streak', backref='user', uselist=False, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class DiaryEntry(db.Model):
    """Diary entry model"""
    __tablename__ = 'diary_entries'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_preview(self, length=100):
        """Get preview of content (first N characters)"""
        if len(self.content) > length:
            return self.content[:length] + '...'
        return self.content
    
    def get_date_only(self):
        """Get just the date part"""
        return self.created_at.date()
    
    def __repr__(self):
        return f'<DiaryEntry {self.id}: {self.title}>'

class Streak(db.Model):
    """Streak tracking model"""
    __tablename__ = 'streaks'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    current_streak = db.Column(db.Integer, default=0)
    longest_streak = db.Column(db.Integer, default=0)
    last_entry_date = db.Column(db.Date)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def check_and_update_streak(self):
        """
        Check if user wrote today, and update streak accordingly.
        Returns the current streak count.
        """
        today = date.today()
        
        # Check if user has entry today
        has_entry_today = DiaryEntry.query.filter_by(user_id=self.user_id).filter(
            db.func.date(DiaryEntry.created_at) == today
        ).first() is not None
        
        if not has_entry_today:
            return self.current_streak
        
        # If last entry was today, streak is already counted
        if self.last_entry_date == today:
            return self.current_streak
        
        # If no previous entry date or last entry was yesterday
        if self.last_entry_date is None or self.last_entry_date == date.today():
            # New streak or continuing
            self.current_streak = 1
        elif (today - self.last_entry_date).days == 1:
            # Streak continues (entry yesterday, today, etc.)
            self.current_streak += 1
        else:
            # Gap in streak - reset
            self.current_streak = 1
        
        # Update longest streak if current exceeds it
        if self.current_streak > self.longest_streak:
            self.longest_streak = self.current_streak
        
        self.last_entry_date = today
        db.session.commit()
        
        return self.current_streak
    
    def __repr__(self):
        return f'<Streak user_id={self.user_id}: {self.current_streak}>'
