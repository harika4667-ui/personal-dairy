# 📔 Personal Diary Web App

A beautiful, modern personal diary web application built with Python Flask, SQLite, and Jinja2 templates. Write, edit, and reflect on your daily thoughts with a stunning pastel gradient interface.

## Features

✨ **Key Features:**
- 🔐 **User Authentication** - Secure login/signup with Flask sessions
- ✍️ **Create, Edit, Delete Entries** - Full CRUD functionality with date tracking
- 📅 **Month-based Organization** - Entries grouped and displayed by month
- 🔥 **Streak System** - Tracks daily writing streaks with longest streak records
- 📊 **Dashboard Stats** - Display current streak, longest streak, and total entries
- 📱 **Responsive Design** - Mobile-friendly layout that works on all devices
- 🎨 **Beautiful UI** - Soft pastel gradients and smooth animations
- 💾 **Persistent Storage** - All data stored in SQLite database
- 📝 **Preview Cards** - First 100 characters shown in card previews
- 🔍 **Full Entry View** - Click cards to see complete entries

## Tech Stack

- **Backend:** Python Flask
- **Database:** SQLite with SQLAlchemy ORM
- **Frontend:** Jinja2 templates + CSS (no JavaScript frameworks)
- **Styling:** Custom CSS with responsive design

## Project Structure

```
personal diary/
├── app.py                 # Main Flask application with routes
├── models.py             # SQLAlchemy models (User, DiaryEntry, Streak)
├── config.py             # Flask configuration settings
├── requirements.txt      # Python dependencies
├── templates/            # Jinja2 HTML templates
│   ├── base.html         # Base template with navbar
│   ├── login.html        # Login page
│   ├── signup.html       # Sign up page
│   ├── dashboard.html    # Main dashboard with entries
│   ├── add_entry.html    # Form to create new entry
│   ├── edit_entry.html   # Form to edit entry
│   ├── view_entry.html   # Full entry view
│   ├── settings.html     # User settings & account info
│   ├── 404.html          # 404 error page
│   └── 500.html          # 500 error page
├── static/
│   └── css/
│       └── style.css     # All styling (mobile-responsive)
└── README.md             # This file
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone or Download the Project**
   ```bash
   cd "personal diary"
   ```

2. **Create a Virtual Environment** (recommended)
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   python app.py
   ```

5. **Access the App**
   Open your browser and navigate to: `http://localhost:5000`

## Usage

### Getting Started

1. **Sign Up** - Create a new account with username, email, and password
2. **Login** - Sign in to your account
3. **Add Entry** - Click the "+" button to create a new entry
4. **View & Edit** - Click on any entry card to view full content or edit it
5. **Track Progress** - Check your streak and total entries on the dashboard

### Diary Features

- **Write Entries**: Click "+ Add Note" button to create a new entry
- **Optional Titles**: Add a title to your entry or leave it untitled
- **Auto-save Draft**: Your draft is automatically saved locally while you type
- **View Full Entry**: Click on entry cards to see the complete content
- **Edit Anytime**: Update any entry from the full view page
- **Delete Entry**: Remove entries you no longer want (with confirmation)

### Streak System

- **Daily Streak**: Automatically increments when you write at least one entry per day
- **Longest Streak**: Tracks your best consecutive days of writing
- **Reset Protection**: Streak resets only when you miss a day
- **Dashboard Display**: View all your stats on the main dashboard

### Account Management

- **Profile**: View your username and email in settings
- **Change Password**: Update your password securely
- **Session Management**: Logout from settings page

## Database Schema

### Users Table
```
- id: Integer (Primary Key)
- username: String (Unique)
- email: String (Unique)
- password_hash: String
- created_at: DateTime
```

### DiaryEntry Table
```
- id: Integer (Primary Key)
- user_id: Integer (Foreign Key)
- title: String (Optional)
- content: Text
- created_at: DateTime
- updated_at: DateTime
```

### Streak Table
```
- id: Integer (Primary Key)
- user_id: Integer (Foreign Key, Unique)
- current_streak: Integer
- longest_streak: Integer
- last_entry_date: Date
- updated_at: DateTime
```

## Security Features

✅ **Implemented Security:**
- Password hashing with Werkzeug (bcrypt-based)
- Session-based authentication
- CSRF protection via Flask sessions
- HttpOnly cookies
- User isolation (users see only their own entries)
- Form validation
- Error handling

## Customization

### Change Secret Key
Edit `config.py`:
```python
SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-unique-secret-key'
```

### Change Database Location
Edit `config.py`:
```python
SQLALCHEMY_DATABASE_URI = 'sqlite:///your_custom_path.db'
```

### Modify Colors & Styling
Edit `static/css/style.css` to customize:
- Primary gradient colors
- Text colors
- Shadows and effects
- Responsive breakpoints

## Performance Tips

- First-time page load initializes the SQLite database
- Database queries are optimized with indexes on frequently searched fields
- Static CSS is cached by browsers
- No JavaScript required (lightweight frontend)

## Troubleshooting

### Port Already in Use
If port 5000 is already in use:
```python
# In app.py, change the last line:
app.run(debug=True, host='0.0.0.0', port=5001)  # Use different port
```

### Database Issues
To reset the database:
1. Delete `diary.db` file if it exists
2. Restart the application
3. New database will be created automatically

### Session Issues
Clear your browser cookies or:
```python
# In app.py, modify config:
SESSION_COOKIE_HTTPONLY = False  # For development only
```

## Browser Compatibility

✅ Works on:
- Chrome/Chromium (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers

## Responsive Breakpoints

- Desktop: 1024px and above
- Tablet: 768px - 1023px
- Mobile: Below 768px

## Future Enhancements

Potential features to add:
- 📎 Image attachments to entries
- 🏷️ Tags and categories
- 🔎 Full-text search
- 📊 Analytics dashboard
- 🎨 Custom themes
- ☁️ Cloud backup
- 🔐 Two-factor authentication
- 📤 Export entries as PDF

## Deployment

For production deployment:

1. **Update config.py**:
   ```python
   app = create_app('production')
   SESSION_COOKIE_SECURE = True  # Requires HTTPS
   ```

2. **Use a production WSGI server** (Gunicorn, uWSGI):
   ```bash
   pip install gunicorn
   gunicorn -w 4 app:create_app()
   ```

3. **Set environment variables**:
   ```bash
   export SECRET_KEY='your-secure-random-key'
   export FLASK_ENV='production'
   ```

## License

This project is open source and available for personal use.

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Verify all dependencies are installed
3. Ensure Python version is 3.8+

---

**Happy Writing! 📝✨**

Start capturing your thoughts and building your writing streak today!
