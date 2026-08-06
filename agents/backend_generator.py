import os


class BackendGenerator:
    def generate_backend(self, website_type: str, website_name: str, sections: list):
        backend_code = self._generate_main_app(website_type, website_name, sections)
        models_code = self._generate_models(website_type, sections)
        admin_code = self._generate_admin_dashboard(website_type, website_name)
        requirements_code = self._generate_requirements()
        env_template = self._generate_env_template()

        return {
            "main_app": backend_code,
            "models": models_code,
            "admin_dashboard": admin_code,
            "requirements": requirements_code,
            "env_template": env_template,
            "website_type": website_type,
            "website_name": website_name
        }

    def _generate_main_app(self, website_type, website_name, sections):
        return f'''from fastapi import FastAPI, Depends, HTTPException, status, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import jwt
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional, List

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./website.db")
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")

engine = create_engine(DATABASE_URL, connect_args={{"check_same_thread": False}} if "sqlite" in DATABASE_URL else {{}})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from models import Base, User, FormSubmission, PageContent

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="{website_name} API",
    description="Backend API for {website_name}",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({{"exp": expire}})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt

def verify_token(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    try:
        scheme, credentials = authorization.split(" ", 1)
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid authorization scheme")
        payload = jwt.decode(credentials, SECRET_KEY, algorithms=["HS256"])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return email
    except (jwt.InvalidTokenError, ValueError, IndexError):
        raise HTTPException(status_code=401, detail="Invalid token")

# Schemas
class UserRegister(BaseModel):
    email: str
    password: str
    name: str

class UserLogin(BaseModel):
    email: str
    password: str

class FormSubmissionSchema(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    message: str
    form_type: str = "contact"

class PageContentSchema(BaseModel):
    page: str
    title: str
    content: str

class PageContentResponse(BaseModel):
    id: int
    page: str
    title: str
    content: str
    updated_at: datetime

    class Config:
        from_attributes = True

# Auth Endpoints
@app.post("/api/auth/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(email=user.email, name=user.name)
    new_user.set_password(user.password)
    db.add(new_user)
    db.commit()

    access_token = create_access_token(data={{"sub": user.email}})
    return {{"access_token": access_token, "token_type": "bearer"}}

@app.post("/api/auth/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not db_user.verify_password(user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={{"sub": user.email}})
    return {{"access_token": access_token, "token_type": "bearer", "user": {{"name": db_user.name, "email": db_user.email}}}}

# Form Submission Endpoints
@app.post("/api/forms/submit")
def submit_form(submission: FormSubmissionSchema, db: Session = Depends(get_db)):
    new_submission = FormSubmission(
        name=submission.name,
        email=submission.email,
        phone=submission.phone,
        message=submission.message,
        form_type=submission.form_type
    )
    db.add(new_submission)
    db.commit()
    return {{"success": True, "message": "Form submitted successfully", "id": new_submission.id}}

@app.get("/api/forms/submissions")
def get_submissions(email: str = Depends(verify_token), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")

    submissions = db.query(FormSubmission).all()
    return submissions

# Content Management Endpoints
@app.get("/api/content/{{page}}")
def get_page_content(page: str, db: Session = Depends(get_db)):
    content = db.query(PageContent).filter(PageContent.page == page).first()
    if not content:
        return {{"page": page, "title": "", "content": ""}}
    return content

@app.get("/api/content")
def get_all_content(db: Session = Depends(get_db)):
    return db.query(PageContent).all()

@app.post("/api/content")
def create_content(content: PageContentSchema, email: str = Depends(verify_token), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")

    page_content = db.query(PageContent).filter(PageContent.page == content.page).first()
    if page_content:
        page_content.title = content.title
        page_content.content = content.content
        page_content.updated_at = datetime.utcnow()
    else:
        page_content = PageContent(page=content.page, title=content.title, content=content.content)
        db.add(page_content)

    db.commit()
    return {{"success": True, "message": "Content updated"}}

# Health check
@app.get("/api/health")
def health_check():
    return {{"status": "ok", "service": "{website_name} API"}}

@app.get("/")
def root():
    return {{"message": "{website_name} API is running", "docs": "/docs"}}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''

    def _generate_models(self, website_type, sections):
        return '''from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from passlib.context import CryptContext

Base = declarative_base()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    hashed_password = Column(String)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def set_password(self, password: str):
        self.hashed_password = pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.hashed_password)

class FormSubmission(Base):
    __tablename__ = "form_submissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, index=True)
    phone = Column(String, nullable=True)
    message = Column(Text)
    form_type = Column(String, default="contact")
    submitted_at = Column(DateTime, default=datetime.utcnow)
    is_read = Column(Boolean, default=False)

class PageContent(Base):
    __tablename__ = "page_content"

    id = Column(Integer, primary_key=True, index=True)
    page = Column(String, unique=True, index=True)
    title = Column(String)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AdminSetting(Base):
    __tablename__ = "admin_settings"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True)
    value = Column(Text)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
'''

    def _generate_admin_dashboard(self, website_type, website_name):
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Dashboard - {website_name}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: #f3f4f6;
            color: #111827;
        }}

        .container {{
            display: flex;
            min-height: 100vh;
        }}

        .sidebar {{
            width: 250px;
            background: #1f2937;
            color: white;
            padding: 2rem 0;
            position: fixed;
            height: 100vh;
            left: 0;
            top: 0;
        }}

        .sidebar h2 {{
            padding: 0 1.5rem;
            margin-bottom: 2rem;
            font-size: 1.25rem;
        }}

        .sidebar ul {{
            list-style: none;
        }}

        .sidebar li {{
            margin: 0;
        }}

        .sidebar a {{
            display: block;
            padding: 1rem 1.5rem;
            color: #d1d5db;
            text-decoration: none;
            transition: all 0.3s;
            border-left: 3px solid transparent;
        }}

        .sidebar a:hover {{
            background: #374151;
            color: white;
            border-left-color: #3b82f6;
        }}

        .sidebar a.active {{
            background: #374151;
            color: white;
            border-left-color: #3b82f6;
        }}

        .main {{
            margin-left: 250px;
            flex: 1;
            padding: 2rem;
        }}

        header {{
            background: white;
            padding: 1.5rem 2rem;
            border-radius: 0.5rem;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            margin-bottom: 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        h1 {{
            font-size: 2rem;
            margin-bottom: 1rem;
        }}

        .card {{
            background: white;
            border-radius: 0.5rem;
            padding: 2rem;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            margin-bottom: 2rem;
        }}

        .card h2 {{
            margin-bottom: 1.5rem;
            color: #1f2937;
            border-bottom: 2px solid #e5e7eb;
            padding-bottom: 1rem;
        }}

        .form-group {{
            margin-bottom: 1.5rem;
        }}

        label {{
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 500;
            color: #374151;
        }}

        input, textarea, select {{
            width: 100%;
            padding: 0.75rem;
            border: 1px solid #d1d5db;
            border-radius: 0.375rem;
            font-size: 1rem;
            font-family: inherit;
        }}

        input:focus, textarea:focus, select:focus {{
            outline: none;
            border-color: #3b82f6;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }}

        textarea {{
            resize: vertical;
            min-height: 150px;
        }}

        button {{
            background: #3b82f6;
            color: white;
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: 0.375rem;
            cursor: pointer;
            font-weight: 500;
            transition: all 0.3s;
        }}

        button:hover {{
            background: #2563eb;
        }}

        .btn-danger {{
            background: #dc2626;
        }}

        .btn-danger:hover {{
            background: #b91c1c;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
        }}

        th, td {{
            padding: 1rem;
            text-align: left;
            border-bottom: 1px solid #e5e7eb;
        }}

        th {{
            background: #f9fafb;
            font-weight: 600;
            color: #374151;
        }}

        tr:hover {{
            background: #f9fafb;
        }}

        .badge {{
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.875rem;
            font-weight: 500;
        }}

        .badge-success {{
            background: #d1fae5;
            color: #065f46;
        }}

        .badge-warning {{
            background: #fef3c7;
            color: #92400e;
        }}

        .logout {{
            background: #6b7280;
            color: white;
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: 0.375rem;
            cursor: pointer;
            transition: all 0.3s;
        }}

        .logout:hover {{
            background: #4b5563;
        }}

        .alert {{
            padding: 1rem;
            border-radius: 0.375rem;
            margin-bottom: 1rem;
        }}

        .alert-success {{
            background: #d1fae5;
            color: #065f46;
            border: 1px solid #6ee7b7;
        }}

        .alert-error {{
            background: #fee2e2;
            color: #991b1b;
            border: 1px solid #fca5a5;
        }}

        .hidden {{
            display: none;
        }}

        @media (max-width: 768px) {{
            .sidebar {{
                width: 100%;
                height: auto;
                position: relative;
            }}

            .main {{
                margin-left: 0;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="sidebar">
            <h2>{website_name}</h2>
            <ul>
                <li><a href="#dashboard" class="nav-link active" onclick="showSection('dashboard')">Dashboard</a></li>
                <li><a href="#submissions" class="nav-link" onclick="showSection('submissions')">Form Submissions</a></li>
                <li><a href="#content" class="nav-link" onclick="showSection('content')">Manage Content</a></li>
                <li><a href="#users" class="nav-link" onclick="showSection('users')">Users</a></li>
                <li><a href="#settings" class="nav-link" onclick="showSection('settings')">Settings</a></li>
            </ul>
        </div>

        <div class="main">
            <header>
                <h1>{website_name} Admin</h1>
                <button class="logout" onclick="logout()">Logout</button>
            </header>

            <div id="alert" class="alert hidden"></div>

            <!-- Dashboard Section -->
            <section id="dashboard" class="section">
                <div class="card">
                    <h2>Dashboard</h2>
                    <p>Welcome to your admin dashboard. Manage your website content, forms, and users from here.</p>
                </div>
            </section>

            <!-- Form Submissions Section -->
            <section id="submissions" class="section hidden">
                <div class="card">
                    <h2>Form Submissions</h2>
                    <table id="submissionsTable">
                        <thead>
                            <tr>
                                <th>Name</th>
                                <th>Email</th>
                                <th>Type</th>
                                <th>Message</th>
                                <th>Date</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            <!-- Will be populated by JavaScript -->
                        </tbody>
                    </table>
                </div>
            </section>

            <!-- Content Management Section -->
            <section id="content" class="section hidden">
                <div class="card">
                    <h2>Manage Page Content</h2>
                    <div class="form-group">
                        <label>Page:</label>
                        <select id="pageName">
                            <option>home</option>
                            <option>about</option>
                            <option>services</option>
                            <option>contact</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Title:</label>
                        <input type="text" id="pageTitle" placeholder="Page title">
                    </div>
                    <div class="form-group">
                        <label>Content:</label>
                        <textarea id="pageContent" placeholder="Page content"></textarea>
                    </div>
                    <button onclick="saveContent()">Save Content</button>
                </div>
            </section>

            <!-- Users Section -->
            <section id="users" class="section hidden">
                <div class="card">
                    <h2>Users</h2>
                    <table id="usersTable">
                        <thead>
                            <tr>
                                <th>Name</th>
                                <th>Email</th>
                                <th>Role</th>
                                <th>Joined</th>
                            </tr>
                        </thead>
                        <tbody>
                            <!-- Will be populated by JavaScript -->
                        </tbody>
                    </table>
                </div>
            </section>

            <!-- Settings Section -->
            <section id="settings" class="section hidden">
                <div class="card">
                    <h2>Settings</h2>
                    <div class="form-group">
                        <label>Website Name:</label>
                        <input type="text" id="siteName" value="{website_name}">
                    </div>
                    <div class="form-group">
                        <label>Website Email:</label>
                        <input type="email" id="siteEmail" placeholder="contact@example.com">
                    </div>
                    <button onclick="saveSettings()">Save Settings</button>
                </div>
            </section>
        </div>
    </div>

    <script>
        const API_URL = "http://localhost:8000/api";
        const token = localStorage.getItem("token");

        function showSection(sectionId) {{
            document.querySelectorAll(".section").forEach(s => s.classList.add("hidden"));
            document.getElementById(sectionId).classList.remove("hidden");

            document.querySelectorAll(".nav-link").forEach(l => l.classList.remove("active"));
            event.target.classList.add("active");
        }}

        function logout() {{
            localStorage.removeItem("token");
            window.location.href = "/";
        }}

        function showAlert(message, type = "success") {{
            const alert = document.getElementById("alert");
            alert.textContent = message;
            alert.className = `alert alert-${{type}}`;
            alert.classList.remove("hidden");
            setTimeout(() => alert.classList.add("hidden"), 3000);
        }}

        async function saveContent() {{
            const page = document.getElementById("pageName").value;
            const title = document.getElementById("pageTitle").value;
            const content = document.getElementById("pageContent").value;

            try {{
                const response = await fetch(`${{API_URL}}/content`, {{
                    method: "POST",
                    headers: {{
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${{token}}`
                    }},
                    body: JSON.stringify({{ page, title, content }})
                }});

                if (response.ok) {{
                    showAlert("Content saved successfully!");
                }} else {{
                    showAlert("Error saving content", "error");
                }}
            }} catch (error) {{
                showAlert("Error: " + error.message, "error");
            }}
        }}

        async function saveSettings() {{
            showAlert("Settings saved!");
        }}

        // Load form submissions on page load
        async function loadSubmissions() {{
            try {{
                const response = await fetch(`${{API_URL}}/forms/submissions`, {{
                    headers: {{ "Authorization": `Bearer ${{token}}` }}
                }});

                if (response.ok) {{
                    const submissions = await response.json();
                    const tbody = document.querySelector("#submissionsTable tbody");
                    tbody.innerHTML = submissions.map(s => `
                        <tr>
                            <td>${{s.name}}</td>
                            <td>${{s.email}}</td>
                            <td><span class="badge badge-success">${{s.form_type}}</span></td>
                            <td>${{s.message.substring(0, 50)}}...</td>
                            <td>${{new Date(s.submitted_at).toLocaleDateString()}}</td>
                            <td><span class="badge badge-warning">Unread</span></td>
                        </tr>
                    `).join("");
                }}
            }} catch (error) {{
                console.error("Error loading submissions:", error);
            }}
        }}

        // Initialize on page load
        if (!token) {{
            window.location.href = "/login.html";
        }}
    </script>
</body>
</html>
'''

    def _generate_requirements(self):
        return '''fastapi==0.115.12
uvicorn[standard]==0.34.3
sqlalchemy==2.0.23
alembic==1.13.1
pydantic==2.10.6
python-dotenv==1.1.1
pyjwt==2.8.1
passlib[bcrypt]==1.7.4
bcrypt==4.1.1
python-multipart==0.0.20
email-validator==2.1.0
requests==2.31.0
'''

    def _generate_env_template(self):
        return '''# Database Configuration
DATABASE_URL=sqlite:///./website.db
# For PostgreSQL: postgresql://user:password@localhost/dbname

# JWT Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production

# Email Configuration (optional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-email-password

# API Configuration
API_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000
'''
