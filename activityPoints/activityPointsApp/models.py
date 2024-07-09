from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone


# Create your models here.
class Student(models.Model):
    usn = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    sem = models.IntegerField()
    sec = models.CharField(max_length=1)
    phone_no = models.CharField(max_length=10)
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    
class Teacher(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20)
    department = models.CharField(max_length=3)

    def __str__(self):
        return self.name
    
class ActivityCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Activity(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='activities')
    category = models.ForeignKey(ActivityCategory, on_delete=models.CASCADE)
    description = models.TextField()
    date_started = models.DateField()
    date_completed = models.DateField()
    cert_file = models.FileField(upload_to='activity_certificates/', blank=True, null=True)
    upload_time = models.DateTimeField(default=timezone.now)
    points = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.category.name} - {self.student.name}"
    
class Announcement(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    posted_by = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    activity_link = models.URLField(blank=True, null=True)  # Link related to an activity

    def __str__(self):
        return self.title
