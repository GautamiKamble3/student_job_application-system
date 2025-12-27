# 🎓 Student Job Application Management System

A web-based application built using Python Flask that allows students to browse and apply for jobs while enabling administrators to manage job postings and student applications efficiently.

This project demonstrates full-stack development, role-based authentication, and database-driven workflows, making it suitable for freshers and entry-level Python developer roles.

## 🚀 Features

### 👩‍🎓 Student Module
- Student registration and login
- View available job listings
- Apply for jobs
- Track application status (Pending / Approved / Rejected)

### 🛠️ Admin Module
- Admin login with role-based access
- Create and manage job postings
- View all student applications
- Approve or reject applications

### 🔐 Authentication & Security
- Role-based authentication using Flask-Login
- Secure password hashing using Werkzeug
- Session management

## 🧰 Tech Stack

| Layer | Technology |
|------|------------|
| Backend | Python, Flask |
| Frontend | HTML5, CSS3 |
| Database | SQLite |
| ORM | SQLAlchemy |
| Authentication | Flask-Login |
| Version Control | Git, GitHub |

## 📂 Project Structure

```text
student_job_system/
│
├── app.py
├── models.py
├── extensions.py
├── requirements.txt
├── static/
│   ├── css/
│   └── images/
├── templates/
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── admin_dashboard.html
│   ├── admin_jobs.html
│   ├── admin_applications.html
│   ├── student_dashboard.html
│   ├── student_jobs.html
│   └── student_applications.html
├── screenshots/
│   ├── Home_page.png
│   ├── Login_page.png
│   ├── Admin_dashboard.png
│   ├── Student_dashboard.png
│   └── Student_jobs_available.png
└── .gitignore
