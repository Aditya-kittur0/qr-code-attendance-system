from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.shortcuts import render,redirect,redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage 
from django.contrib.auth.decorators import login_required
from .models import Student,Session,Attendance
from django.templatetags.static import static
from .forms import StudentForm,SessionForm
from django.contrib import messages
from datetime import timedelta
from django.conf import settings
from django.urls import reverse
from io import BytesIO
import qrcode
import socket
import uuid
import os


def custom_login(request):
    if request.user.is_authenticated:
        return redirect('redirect_user')  
    return redirect('administration/login.html')

@login_required
def redirect_user(request):
    if request.user.groups.filter(name='admin').exists():   
        return redirect('admin_view')  
    return redirect('administration/login')

def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student=form.save()
            messages.success(request, f"Student {student.name} added successfully!")
            return redirect('manage_student')  
    else:
        form = StudentForm()
    return render(request,'administration/add_student.html',{'form':form})

def manage_student(req):
    student_count = Student.objects.count()
    students = Student.objects.all()
    return render(req,'administration/manage_student.html',{'student_count': student_count,
        'students': students,})


def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id) 
    student.delete() 
    return redirect('manage_student')

@login_required
def admin_dashboard(request):
    student_count = Student.objects.count()
    students = Student.objects.all()
    sessions_titles = Session.objects.values_list('title', flat=True)
    print(sessions_titles)
    return render(request, 'administration/admin_view.html', {
        'student_count': student_count,
        'students': students,
        'sessions_titles':sessions_titles
    })

def view_attendance(request):
    sessions = Session.objects.all()
    session_data=[]
    for session in sessions:
        attendance_records=Attendance.objects.filter(session=session)     
        session_data.append({
            'session':session,
            'attendance_records':attendance_records
        })
    return render(request, 'administration/view_attendance.html', {'session_data': session_data})

def student_list(request):
    students = Student.objects.all()
    return render(request, 'administration/student.html', {'students': students})



def create_session(request):
    if request.method == "POST":
        session_name = str(request.POST.get('session_name'))
        duration_seconds = int(request.POST.get('duration'))
        num_sessions = int(request.POST.get('num_sessions'))
        batch_id = uuid.uuid4()
        sessions = []
        for i in range(num_sessions):
            session = Session(
                title=f"{session_name} {i+1}",
                duration_seconds=duration_seconds,
                batch_id=batch_id
            )
            session.save()
            sessions.append(session)
        return redirect('session_created', batch_id=batch_id)
    else:
        form = SessionForm()
    return render(request, 'administration/session.html', {'form': form})

def attendance_view(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    attendance_records = Attendance.objects.filter(session=session)  
    return render(request, 'administration/attendance_view.html', {
        'session': session,
        'attendance_records': attendance_records,
    })



def session_created(request, batch_id):
    sessions = list(Session.objects.filter(batch_id=batch_id).order_by('start_time'))
    displayed_sessions = request.session.get('displayed_sessions', [])
    current_session = None
    for session in sessions:
        if session.id not in displayed_sessions:
            current_session = session
            break

    if not current_session:
        request.session['displayed_sessions'] = []
        no_more_sessions = True
        return render(request, 'administration/session_created.html', {'batch_id': batch_id, 'no_more_sessions': no_more_sessions})
    
    mark_attendance_url = reverse('attendance', args=[current_session.id])
    hostname = socket.gethostbyname(socket.gethostname())
    full_url = f"http://{hostname}:8000{mark_attendance_url}?session_id={current_session.id}"
    print(f"Generated URL for QR Code: {full_url}")
    
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(full_url)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    
    qr_codes_folder = os.path.join(settings.BASE_DIR, 'administration', 'static', 'qr_codes')
    if not os.path.exists(qr_codes_folder):
        os.makedirs(qr_codes_folder)
    
    buffer = BytesIO()
    img.save(buffer)
    buffer.seek(0)
    
    file_name = f'qr_code_session_{current_session.id}.png'
    file_path = os.path.join(qr_codes_folder, file_name)
    img.save(file_path)
    
    qr_code_url = static(f'qr_codes/{file_name}')

    displayed_sessions.append(current_session.id)
    request.session['displayed_sessions'] = displayed_sessions
    request.session.modified = True

    remaining_time = timedelta(seconds=current_session.duration_seconds)
    remaining_time_seconds = int(remaining_time.total_seconds())

    last_session = len(displayed_sessions) == len(sessions)

    context = {
        'batch_id': batch_id,               
        'session': current_session,          
        'qr_code_url': qr_code_url,          
        'remaining_time_seconds': remaining_time_seconds,  
        'last_session': last_session    
    }

    return render(request, 'administration/session_created.html', context)





