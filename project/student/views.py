from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from administration.models import Student, Attendance,Session

def attendance(request,session_id):
     session = get_object_or_404(Session, id=session_id)
     messages=[]
     if request.method == 'POST':
        print("POST data:", request.POST)
        roll_number = request.POST.get('roll_number')
        session = get_object_or_404(Session, id=session_id)
        print(session_id)
        if not roll_number or not session_id:
            messages.append("roll number is required")
            return render(request, 'attendance.html',{'session_id': session.id,'messages':messages})  
        try:
            session = Session.objects.get(id=session_id)
        except Session.DoesNotExist:
            return JsonResponse({"error": "Invalid session ID"}, status=400)
        
        mac_address =  ip = request.META.get('REMOTE_ADDR')  # Retrieve the MAC address
        if not mac_address:
            return JsonResponse({"error": "Unable to retrieve MAC address."}, status=400)
        
        try:
            student = Student.objects.get(roll_number=roll_number)
        except Student.DoesNotExist:
            messages.append("Invalid roll number. No student found.")
            return render(request, 'attendance.html',{'session_id': session.id,'messages':messages})  
        
        if student.mac_address:
            if student.mac_address != mac_address:
                messages.append("IP address does not match the registered device.")
                return render(request, 'attendance.html',{'session_id': session.id,'messages':messages})  
        else:
           
            mac_assigned = Student.objects.filter(mac_address=mac_address).exists()
            if mac_assigned:
                messages.append("This IP address is already registered to another student.")
                return render(request, 'attendance.html',{'session_id': session.id,'messages':messages})  
            student.mac_address = mac_address
            student.save()
        
        attendance_exists = Attendance.objects.filter(session=session, student__roll_number=roll_number).exists()
        if attendance_exists:
            messages.append("Attendance already marked for this session.")
            return render(request, 'attendance.html',{'session_id': session.id,'messages':messages})  
        Attendance.objects.create(session=session,student=student)
        messages.append("Attendance marked successfully.")
        return render(request, 'attendance.html',{'session_id': session.id,'messages':messages})  
     
     return render(request, 'attendance.html',{'session_id': session.id,'messages':messages})  

