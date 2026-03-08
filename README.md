# AI-Driven Project Management Platform

This is a **Django-based project lifecycle management platform** designed to manage projects between **clients, managers, and associates**.

The system demonstrates **role-based access control, workflow automation, AI-assisted prioritization, and team collaboration tools** in a SaaS-style architecture.

---

# Features

## Role-Based Access Control (RBAC)

The platform supports four user roles:

### Admin

* Manage users
* Assign managers to projects
* Monitor platform activity

### Manager

* View assigned projects
* Assign associates to projects
* Monitor project progress

### Associate

* Work on assigned projects
* Update project status
* Participate in project discussions

### Client

* Submit project requirements
* Track project progress
* Communicate with the team

---

# Core Functionalities

### Project Lifecycle Management

Projects move through the following stages:

New → Assigned → In Progress → Review → Completed → Closed

---

### Team Assignment Workflow

Project assignment process:

1. Client creates project
2. Admin assigns a Manager
3. Manager assigns Associates
4. Associates execute project tasks

---

### AI-Based Priority Scoring

Projects are automatically prioritized using the formula:

Priority Score = (Price × 0.5) + (Complexity × 0.3) + (Urgency × 0.2)

This helps identify high-value and urgent projects.

---

### Project Communication System

Each project includes a communication space where:

* Clients
* Managers
* Associates

can collaborate and exchange messages.

---

# Technology Stack

Backend:

* Python
* Django Framework

Database:

* SQLite

AI / ML:

* scikit-learn
* HuggingFace Transformers
* LanguageTool

Frontend:

* Django Templates
* Custom CSS

Other Tools:

* Git
* GitHub
* Virtual Environment

---

# Project Structure

```id="projstruct01"
project-management-platform/
│
├── accounts/              # User management and roles
├── projects/              # Project models and business logic
├── dashboard/             # Role-based dashboards
├── templates/             # HTML templates
├── static/                # CSS and static assets
├── manage.py
├── requirements.txt
└── README.md
```

---

# Installation Guide

Follow these steps to run the project locally.

## 1. Clone the Repository

```id="clone01"
git clone https://github.com/your-username/project-management-platform.git
cd project-management-platform
```

---

## 2. Create Virtual Environment

```id="venv01"
python -m venv venv
```

Activate environment:

Windows

```id="venv02"
venv\Scripts\activate
```

Mac/Linux

```id="venv03"
source venv/bin/activate
```

---

## 3. Install Dependencies

```id="install01"
pip install -r requirements.txt
```

---

## 4. Run Database Migrations

```id="migrate01"
python manage.py migrate
```

---

## 5. Create Admin User

```id="superuser01"
python manage.py createsuperuser
```

---

## 6. Start Development Server

```id="run01"
python manage.py runserver
```

Open the application:

```id="url01"
http://127.0.0.1:8000
```

Admin panel:

```id="url02"
http://127.0.0.1:8000/admin
```

---

# System Workflow

1. Client registers and creates project
2. Admin assigns manager
3. Manager assigns associates
4. Associates work on project tasks
5. Team communicates through project chat
6. Project moves through workflow stages

---

# Possible Future Enhancements

* Real-time chat using WebSockets
* AI-based workload balancing
* Kanban board for project tracking
* Notification system
* Analytics dashboard
* Cloud deployment

---

# Author

Developed by **Pradeep Nishad**

GitHub:
https://github.com/pradeepnishad
