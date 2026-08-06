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

## Limitations
Risk labels are rule-based (no real historical dropout data available) — noted as future work.