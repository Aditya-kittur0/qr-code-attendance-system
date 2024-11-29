from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='administration/login.html'), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('redirect/', views.redirect_user, name='redirect_user'),   
    path('manage_student/', views.manage_student, name='manage_student'),
    path('add_student/', views.add_student, name='add_student'),  
    path('admin_view/', views.admin_dashboard, name='admin_view'),
    path('view_attendance/', views.view_attendance, name='view_attendance'),
    path('session/', views.create_session, name='session'),
    path('attendance_view/<int:session_id>/', views.attendance_view, name='attendance_view'),
    path('student/',include('student.urls')),
    path('session_created/<uuid:batch_id>/', views.session_created, name='session_created'),
    path('delete-student/<int:student_id>/', views.delete_student, name='delete_student'),
    path('student/', views.student_list, name='student_list'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
