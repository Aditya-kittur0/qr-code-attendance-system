from django.urls import path
from .import views

urlpatterns = [
   
    path('attendance/<int:session_id>/',views.attendance,name='attendance'),
]
