# Academic Performance Analytics System

A role-based web platform for tracking student performance and attendance, with a machine learning model that flags at-risk students automatically. Built as a final year Bachelor's project.

## Features
- Role-based dashboards (Admin, Teacher, Student)
- Teacher: per-course student roster with grades/attendance/risk status; forms to record grades and attendance
- Student: personal grade breakdown and comparison to class average
- Admin: system-wide analytics with charts and at-risk student table
- ML model (scikit-learn) predicts at-risk students from average score + attendance

## Tech Stack
Django, PostgreSQL, scikit-learn/pandas, Bootstrap 5, Chart.js

## Setup
git clone <repo-url>
cd academic-analytics
py -3.12 -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt

Create a PostgreSQL database `academic_analytics`, copy `.env.example` to `.env` and fill in credentials, then:
python manage.py migrate
python manage.py seed_data
python manage.py createsuperuser
python manage.py runserver

Login at `/login/` (seeded: `student1`, `teacher1`, password `password123`) or `/admin/` with your superuser.

## Tests
python manage.py test

## Limitations
Risk labels are rule-based (no real historical dropout data available) — noted as future work.