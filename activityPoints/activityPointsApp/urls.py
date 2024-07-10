from django.conf import settings
from django.urls import path
from .views import activity_detail, addActivity, dashboard, logout, register, login, studentActivities, loginTeacherView, teacherDashboard, assignPoints, manage_categories, create_announcement, manage_announcements, delete_announcement, home
from django.conf.urls.static import static


urlpatterns = [
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),  # Add the logout URL
    path('login/', login, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/<int:activity_id>/', dashboard, name='dashboard'),
    path('activities/<int:student_id>/', studentActivities, name='studentActivities'),
    path('teacher/login/', loginTeacherView, name='loginTeacher'),
    path('teacher/dashboard/', teacherDashboard, name='teacherDashboard'),
    path('assign_points/<int:activity_id>/', assignPoints, name='assignPoints'),
    path('manageCategories/', manage_categories, name='manageCategories'),
    path('create_announcement/', create_announcement, name='create_announcement'),
    path('manage_announcements/', manage_announcements, name='manage_announcements'),
    path('delete_announcement/<int:announcement_id>/', delete_announcement, name='delete_announcement'),
    path('announcement_info/<int:announcement_id>/', activity_detail, name='activity_detail'),
    path('addActivity/<int:announcement_id>/', addActivity, name='addActivity')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)