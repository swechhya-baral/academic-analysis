from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from academics.models import Teacher, Student, Course, Enrollment, Grade, Attendance
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Seeds the database with sample academic data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # --- Create Teachers ---
        teacher_names = [
            ('teacher1', 'Alice', 'Sharma', 'Computer Science'),
            ('teacher2', 'Ramesh', 'Karki', 'Mathematics'),
        ]
        teachers = []
        for username, first, last, dept in teacher_names:
            user, _ = User.objects.get_or_create(
                username=username,
                defaults={'first_name': first, 'last_name': last, 'email': f'{username}@example.com'}
            )
            user.set_password('password123')
            user.save()
            teacher, _ = Teacher.objects.get_or_create(user=user, defaults={'department': dept})
            teachers.append(teacher)
        self.stdout.write(self.style.SUCCESS(f'Created {len(teachers)} teachers'))

        # --- Create Students ---
        first_names = ['Sita', 'Bikash', 'Anjali', 'Suresh', 'Priya', 'Kiran', 'Nabin', 'Sushma', 'Rajan', 'Mina',
                        'Ashok', 'Dipika', 'Prakash', 'Sunita', 'Bishnu', 'Kamala', 'Ganesh', 'Sabina', 'Hari', 'Radha']
        last_names = ['Gurung', 'Thapa', 'Rai', 'Magar', 'Shrestha', 'Karki', 'Adhikari', 'Bhandari', 'Poudel', 'Basnet']

        students = []
        for i in range(1, 31):  # 30 students
            username = f'student{i}'
            first = random.choice(first_names)
            last = random.choice(last_names)
            user, _ = User.objects.get_or_create(
                username=username,
                defaults={'first_name': first, 'last_name': last, 'email': f'{username}@example.com'}
            )
            user.set_password('password123')
            user.save()
            student, _ = Student.objects.get_or_create(
                user=user,
                defaults={
                    'roll_number': f'2023-CS-{i:02d}',
                    'date_of_birth': date(2003, random.randint(1, 12), random.randint(1, 28))
                }
            )
            students.append(student)
        self.stdout.write(self.style.SUCCESS(f'Created {len(students)} students'))

        # --- Create Courses ---
        course_data = [
            ('CS101', 'Intro to Programming', 3, teachers[0]),
            ('CS201', 'Data Structures', 4, teachers[0]),
            ('MATH101', 'Calculus I', 3, teachers[1]),
        ]
        courses = []
        for code, name, credits, teacher in course_data:
            course, _ = Course.objects.get_or_create(
                code=code,
                defaults={'name': name, 'credit_hours': credits, 'teacher': teacher}
            )
            courses.append(course)
        self.stdout.write(self.style.SUCCESS(f'Created {len(courses)} courses'))

        # --- Create Enrollments (each student enrolls in 2 random courses) ---
        enrollments = []
        for student in students:
            enrolled_courses = random.sample(courses, k=2)
            for course in enrolled_courses:
                enrollment, _ = Enrollment.objects.get_or_create(
                    student=student, course=course, semester='Fall 2026'
                )
                enrollments.append(enrollment)
        self.stdout.write(self.style.SUCCESS(f'Created {len(enrollments)} enrollments'))

        # --- Create Grades for each enrollment ---
        assessment_types = ['Assignment 1', 'Midterm', 'Final']
        grade_count = 0
        for enrollment in enrollments:
            performance_level = random.uniform(35, 95)  # student's general performance baseline
            for assessment in assessment_types:
                score = round(max(0, min(100, random.gauss(performance_level, 8))), 2)
                Grade.objects.get_or_create(
                    enrollment=enrollment,
                    assessment_type=assessment,
                    defaults={'score': score, 'max_score': 100}
                )
                grade_count += 1
        self.stdout.write(self.style.SUCCESS(f'Created {grade_count} grade entries'))
        
        # --- Create Attendance for each enrollment ---
        attendance_count = 0
        start_date = date(2026, 8, 1)
        for enrollment in enrollments:
            attendance_rate = random.uniform(0.5, 1.0)  # varies per enrollment: 50%-100%
            for day_offset in range(15):
                session_date = start_date + timedelta(days=day_offset * 3)
                present = random.random() < attendance_rate
                Attendance.objects.get_or_create(
                    enrollment=enrollment,
                    date=session_date,
                    defaults={'present': present}
                )
                attendance_count += 1
        self.stdout.write(self.style.SUCCESS(f'Created {attendance_count} attendance records'))

        self.stdout.write(self.style.SUCCESS('Done seeding data!'))