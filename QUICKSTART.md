# 🚀 Quick Start Guide

## Installation & Setup (2 Minutes)

### Windows Users
Simply double-click `run.bat`:
- ✅ Virtual environment created automatically
- ✅ Dependencies installed
- ✅ App starts on http://localhost:5000

### macOS/Linux Users
Run in terminal:
```bash
chmod +x run.sh
./run.sh
```

### Manual Setup
1. Create virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate it:
   - **Windows**: `venv\Scripts\activate`
   - **Mac/Linux**: `source venv/bin/activate`

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the app:
   ```bash
   python app.py
   ```

5. Open browser: **http://localhost:8080**

## First Steps

1. **Create Account** → Click "Sign up here"
2. **Create Entry** → Click "+" button or "Write Your First Entry"
3. **View Dashboard** → See your stats and entries

## Project Contents

```
✅ Backend (Python)
  - app.py           → Flask routes & logic
  - models.py        → Database models
  - config.py        → Settings

✅ Database
  - SQLite (auto-created as diary.db)
  - 3 tables: users, diary_entries, streaks

✅ Frontend
  - 10 HTML templates (Jinja2)
  - 1 CSS file (responsive design)
  - No JavaScript frameworks

✅ Scripts
  - run.bat          → Windows launcher
  - run.sh           → Unix launcher
  - requirements.txt → Dependencies
```

## Features at a Glance

| Feature | Status |
|---------|--------|
| User authentication | ✅ Complete |
| Create/Edit/Delete entries | ✅ Complete |
| Daily streak tracking | ✅ Complete |
| Monthly grouping | ✅ Complete |
| Responsive mobile UI | ✅ Complete |
| Persistent storage | ✅ Complete |
| Pastel gradient design | ✅ Complete |
| Auto-save drafts | ✅ Complete |
| Settings & account page | ✅ Complete |

## Key Technologies

- **Flask 3.0** - Web framework
- **SQLAlchemy** - ORM
- **SQLite** - Database
- **Jinja2** - Templates
- **CSS Grid/Flexbox** - Responsive layout

## File Structure

```
personal diary/
├── app.py                  ← Main application
├── models.py              ← Database models
├── config.py              ← Configuration
├── requirements.txt       ← Dependencies
├── run.bat               ← Windows launcher
├── run.sh                ← Unix launcher
├── README.md             ← Full documentation
├── QUICKSTART.md         ← This file
├── .gitignore            ← Git ignore
├── templates/
│   ├── base.html         ← Main layout
│   ├── login.html        ← Login page
│   ├── signup.html       ← Signup page
│   ├── dashboard.html    ← Main view
│   ├── add_entry.html    ← New entry form
│   ├── edit_entry.html   ← Edit form
│   ├── view_entry.html   ← Full entry view
│   ├── settings.html     ← Settings page
│   ├── 404.html          ← Error pages
│   └── 500.html          ← Error pages
└── static/
    └── css/
        └── style.css     ← All styling

Total Files: 20+
```

## Testing the App

1. **Sign up** with test credentials
2. **Create entries** with different titles
3. **Write multiple entries** to see grouping by month
4. **Check streak** counter after creating entries
5. **Edit/Delete** entries to test CRUD
6. **Change password** in settings
7. **Test on mobile** - use browser dev tools (F12)

## Troubleshooting

**Port 5000 in use?**
Edit app.py last line:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

**Database errors?**
Delete `diary.db` and restart - it recreates automatically

**Virtual env not activating?**
Try: `python -m venv --clear venv`

## Next Steps

- Read [README.md](README.md) for full documentation
- Customize colors in [style.css](static/css/style.css)
- Modify settings in [config.py](config.py)
- Deploy to production when ready!

## Browser Support

Works on all modern browsers:
- Chrome ✅
- Firefox ✅
- Safari ✅
- Edge ✅
- Mobile browsers ✅

## Tips & Tricks

💡 **Auto-save drafts** - Your entry text is saved locally as you type
🔥 **Streak tracking** - Write every day to build your streak
📱 **Mobile friendly** - Use on phone, tablet, or desktop
🎨 **Pastel colors** - Beautiful gradient backgrounds
⚡ **Fast & lightweight** - No heavy frameworks

---

**Happy writing! Start your diary journey today! 📝✨**
