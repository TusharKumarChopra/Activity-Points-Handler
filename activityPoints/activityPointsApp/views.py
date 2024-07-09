from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.utils.dateparse import parse_date
from .models import Activity, Student, ActivityCategory, Announcement, Teacher

def dashboard(request):
    if 'student_id' not in request.session:
        return redirect('login')

    student_id = request.session['student_id']
    student = Student.objects.get(id=student_id)
    categories = ActivityCategory.objects.all()

    if request.method == 'POST':
        category_id = request.POST.get('category')
        description = request.POST.get('description')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        cert_file = request.FILES.get('cert_file')

        category = get_object_or_404(ActivityCategory, id=category_id)

        activity = Activity(
            student=student,
            category=category,
            description=description,
            date_started=parse_date(start_date),
            date_completed=parse_date(end_date),
            cert_file=cert_file
        )
        activity.save()

        return redirect('dashboard')
    
    activities = student.activities.all()
    announcements = Announcement.objects.all()

    return render(request, 'dashboard.html', {'categories': categories, 'activities': activities, 'announcements': announcements})


def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        usn = request.POST.get('usn')
        email = request.POST.get('email')
        password = request.POST.get('password')
        sem = request.POST.get('sem')
        sec = request.POST.get('sec')
        phone = request.POST.get('phone')

        if Student.objects.filter(usn=usn).exists():
            return render(request, 'register.html', {'error': 'USN already exists'})

        hashed_password = make_password(password)
        student = Student(name=name, usn=usn, email=email, password=hashed_password, sem=sem, sec=sec, phone_no=phone)
        student.save()
        return redirect('login')

    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        usn = request.POST.get('usn')
        password = request.POST.get('password')

        try:
            student = Student.objects.get(usn=usn)
            if check_password(password, student.password):
                # Clear teacher session
                request.session.flush()
                # Set student session
                request.session['student_id'] = student.id
                request.session['usn'] = student.usn
                return redirect('dashboard')  # Redirect to a dashboard or home page
            else:
                return render(request, 'login.html', {'error': 'Invalid credentials'})
        except Student.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')

def logout(request):
    # Clear all session variables
    request.session.flush()
    return redirect('login')

def studentActivities(request, student_id):
    if 'student_id' not in request.session and 'teacher_email' not in request.session:
        return redirect('login')  # Redirect to login page if not logged in

    # Retrieve the student from the session
    # student_id = request.session['student_id']
    # student = Student.objects.get(id=student_id)

    # activities = student.activities.all()
    student = get_object_or_404(Student, id=student_id)
    activities = student.activities.all()

    return render(request, 'myActivities.html', {"student": student, "activities": activities})

# Hardcoded teacher credentials
HARD_CODED_TEACHERS = [
    {"name": "Teacher1", "email": "teacher1@example.com", "password": "password1", "department": "CSE"},
    {"name": "Teacher2", "email": "teacher2@example.com", "password": "password2", "department": "CSE"}
]

def loginTeacherView(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        for teacher in HARD_CODED_TEACHERS:
            if teacher['email'] == email and teacher['password'] == password:
                # Clear student session
                request.session.flush()
                # Set teacher session 
                request.session['teacher_email'] = email
                return redirect('teacherDashboard')
        
        return render(request, 'loginTeacher.html', {'error': 'Invalid credentials'})
    
    return render(request, 'loginTeacher.html')

def teacherDashboard(request):
    if 'teacher_email' not in request.session:
        return redirect('loginTeacher')

    if request.method == 'POST':
        usn = request.POST.get('usn')
        try:
            student = Student.objects.get(usn=usn)
            students = [student]
        except Student.DoesNotExist:
            return render(request, 'teacherDashboard.html', {'error': 'Student with this USN does not exist'})
    
    else:
        students = Student.objects.all().order_by('usn')

    return render(request, 'teacherDashboard.html', {'students': students})

def assignPoints(request, activity_id):
    if 'teacher_email' not in request.session:
        return redirect('loginTeacher')
    
    activity = get_object_or_404(Activity, id=activity_id)
    
    if request.method == 'POST':
        points = int(request.POST.get('points', 0))
        activity.points = points
        activity.save()

        # Update the total points for the student
        student = activity.student
        student.points = sum(a.points for a in student.activities.all())
        student.save()

        return redirect('teacherDashboard')
    
    return render(request, 'assignPoints.html', {'activity': activity})

def manage_categories(request):
    if 'teacher_email' not in request.session:
        return redirect('loginTeacher')

    categories = ActivityCategory.objects.all()

    if request.method == 'POST':
        if 'add_category' in request.POST:
            category_name = request.POST.get('category_name')
            if category_name:
                ActivityCategory.objects.create(name=category_name)
        elif 'delete_category' in request.POST:
            category_id = request.POST.get('category_id')
            category = get_object_or_404(ActivityCategory, id=category_id)
            category.delete()

        return redirect('manageCategories')

    return render(request, 'manageCategories.html', {'categories': categories})

def create_announcement(request):
    if 'teacher_email' not in request.session:
        return redirect('loginTeacher')

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        try:
            teacher = Teacher.objects.get(email=request.session['teacher_email'])
        except Teacher.DoesNotExist:
            return render(request, 'create_announcement.html', {'error': 'Teacher not found.'})

        announcement = Announcement(
            title=title,
            content=content,
            posted_by=teacher
        )
        announcement.save()

        return redirect('teacherDashboard')

    return render(request, 'create_announcement.html')


def manage_announcements(request):
    if 'teacher_email' not in request.session:
        return redirect('loginTeacher')

    teacher_email = request.session['teacher_email']
    announcements = Announcement.objects.filter(posted_by__email=teacher_email)

    if request.method == 'POST' and 'delete_announcement' in request.POST:
        announcement_id = request.POST.get('announcement_id')
        announcement = get_object_or_404(Announcement, id=announcement_id, posted_by__email=teacher_email)
        announcement.delete()
        return redirect('manage_announcements')

    return render(request, 'manage_announcements.html', {'announcements': announcements})

def delete_announcement(request, announcement_id):
    if 'teacher_email' not in request.session:
        return redirect('loginTeacher')

    teacher_email = request.session['teacher_email']
    announcement = get_object_or_404(Announcement, id=announcement_id, posted_by__email=teacher_email)
    
    if request.method == 'POST':
        announcement.delete()
        return redirect('manage_announcements')

    return render(request, 'confirm_delete.html', {'announcement': announcement})

