# Full-Stack Website Generator - Testing Guide

## Step-by-Step Testing Instructions

### Step 1: Navigate to Your Project
```bash
cd C:\Users\HP\OneDrive\Desktop\multiagent_system
```

### Step 2: Pull Latest Changes
```bash
git pull origin main
```

### Step 3: Generate Website with Backend
```bash
python main_with_backend.py
```

When prompted:
- **Describe your website:** Type any of these:
  ```
  Create a restaurant website with menu, reservations, and contact form
  ```
  OR
  ```
  Build a portfolio website for a web developer with projects and skills
  ```
  OR
  ```
  Make a business website with services, pricing, and contact form
  ```

- **Generate backend?** Type: `yes`

### Step 4: Wait for Generation
- The system will generate HTML, CSS, and backend
- A browser preview will open automatically
- Close it when ready

### Step 5: Setup the Backend

#### Terminal 1 - Setup Backend Files:
```bash
cd output/backend
dir
```

You should see:
- `main.py` (FastAPI application)
- `models.py` (Database models)
- `admin.html` (Admin dashboard)
- `requirements.txt` (Dependencies)
- `.env.example` (Configuration template)

#### Copy .env template:
```bash
copy .env.example .env
```

#### Install dependencies:
```bash
pip install -r requirements.txt
```

This will install:
- FastAPI
- SQLAlchemy
- PyJWT
- bcrypt
- uvicorn
- And 7 more packages

### Step 6: Run the Backend Server

#### Start the server:
```bash
python main.py
```

OR (if above doesn't work):
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 7: Test the API (Open New Terminal)

#### Terminal 2 - Test API Endpoints:

**Register a new user:**
```bash
curl -X POST "http://localhost:8000/api/auth/register" ^
  -H "Content-Type: application/json" ^
  -d "{\"email\": \"user@example.com\", \"password\": \"password123\", \"name\": \"John Doe\"}"
```

**Login:**
```bash
curl -X POST "http://localhost:8000/api/auth/login" ^
  -H "Content-Type: application/json" ^
  -d "{\"email\": \"user@example.com\", \"password\": \"password123\"}"
```

**Submit a form (contact/reservation):**
```bash
curl -X POST "http://localhost:8000/api/forms/submit" ^
  -H "Content-Type: application/json" ^
  -d "{\"name\": \"John Doe\", \"email\": \"john@example.com\", \"phone\": \"1234567890\", \"message\": \"I would like to book a table\", \"form_type\": \"reservation\"}"
```

**Check API health:**
```bash
curl http://localhost:8000/api/health
```

### Step 8: Access Admin Dashboard

#### Open in Browser:
```
http://localhost:8000/admin.html
```

You should see:
- Login form
- Admin dashboard
- Form submissions table
- Content management
- User management
- Settings

### Step 9: Access API Documentation

#### Open in Browser:
```
http://localhost:8000/docs
```

You will see:
- Interactive API documentation
- Try out all endpoints
- See request/response formats
- Authorization options

### Step 10: View Generated Files

#### Check what was created:
```bash
dir output\backend\
dir output\
```

Files created:
- `output/index.html` - Generated website
- `output/styles.css` - Generated CSS
- `output/preview.html` - Preview page
- `output/backend/main.py` - FastAPI app
- `output/backend/models.py` - Database models
- `output/backend/admin.html` - Admin dashboard
- `output/backend/requirements.txt` - Dependencies
- `output/backend/.env` - Configuration

### Step 11: Test Website Responsiveness

#### Open Preview in Browser:
```
file:///C:/Users/HP/OneDrive/Desktop/multiagent_system/output/preview.html
```

Or:
```
http://localhost:8000 (if backend running)
```

Test on:
- Desktop (full screen)
- Tablet (resize window to 768px)
- Mobile (resize window to 480px)

Click buttons and verify they respond!

### Step 12: Check Database

#### View SQLite database:
```bash
cd output/backend
sqlite3 website.db
```

Then run SQL:
```sql
SELECT * FROM users;
SELECT * FROM form_submissions;
SELECT * FROM page_content;
.exit
```

---

## Complete Quick-Test Script

Save as `quick_test.bat` and run:

```batch
@echo off
echo ===== WEBSITE GENERATOR QUICK TEST =====

echo Step 1: Navigate to project
cd C:\Users\HP\OneDrive\Desktop\multiagent_system

echo Step 2: Generate website with backend
python main_with_backend.py

echo Step 3: Setup backend
cd output\backend
copy .env.example .env
pip install -r requirements.txt

echo Step 4: Start backend server
echo Backend will start on http://localhost:8000
python main.py
```

---

## Full Test Checklist

- [ ] Generate website with backend
- [ ] Backend server starts without errors
- [ ] API health check returns OK
- [ ] User registration endpoint works
- [ ] User login endpoint works
- [ ] Form submission endpoint works
- [ ] Admin dashboard loads at /admin.html
- [ ] API docs load at /docs
- [ ] Database file created (website.db)
- [ ] Website preview is responsive
- [ ] Buttons are clickable and styled
- [ ] Admin can view form submissions

---

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'fastapi'`
**Solution:** Install dependencies again:
```bash
pip install -r requirements.txt
```

### Issue: `Port 8000 already in use`
**Solution:** Kill the process or use different port:
```bash
uvicorn main:app --reload --port 8001
```

### Issue: `.env file not found`
**Solution:** Create it:
```bash
copy .env.example .env
```

### Issue: `Cannot find database`
**Solution:** It will be created automatically when you run `python main.py`

### Issue: Website won't load
**Solution:** Make sure backend is running on port 8000:
```bash
python main.py
```

---

## What Should Happen

1. **Generation** → Generates HTML, CSS, and FastAPI backend
2. **Database** → Creates SQLite database with 4 tables
3. **Server** → Starts FastAPI server on port 8000
4. **API** → All endpoints working and returning data
5. **Dashboard** → Admin panel accessible and functional
6. **Website** → Responsive on all screen sizes
7. **Data Storage** → User details and forms saved in database

---

## Next Steps After Testing

- Customize the generated files
- Deploy to a server (Heroku, Railway, AWS, etc.)
- Connect frontend to backend API
- Add email notifications
- Setup payment processing
- Deploy to production

**Everything is ready to use!** 🚀
