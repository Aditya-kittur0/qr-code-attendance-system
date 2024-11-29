from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    roll_number = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    mac_address=models.CharField(max_length=17,blank=True,null=True)


    def __str__(self):
        return self.name
    
class Session(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)  
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)  
    batch_id = models.CharField(max_length=50, blank=True, null=True) 
    duration_seconds = models.IntegerField(null=True, blank=True)  # Store duration in seconds
    order = models.IntegerField(null=True, blank=True)


    def __str__(self):
        return f"{self.title} - {self.date}"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    device_id = models.CharField(max_length=255, null=True, blank=True)  # Store device ID


    def __str__(self):
        return f"{self.student.name} - {self.session.title}"
