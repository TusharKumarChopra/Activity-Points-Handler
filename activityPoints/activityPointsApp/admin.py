from django.contrib import admin
from .models import Announcement, Student, Teacher, Activity

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Activity)
admin.site.register(Announcement)
