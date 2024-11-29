from django.contrib import admin
from .models import Student, Attendance,Session

class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'roll_number', 'created_at')
    search_fields = ('name', 'email', 'roll_number')

class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 0
    fields = ['student', 'session']
    readonly_fields = ['student']

class SessionAdmin(admin.ModelAdmin):
    list_display = ['title', 'date']
    inlines = [AttendanceInline]


admin.site.register(Student, StudentAdmin)
admin.site.register(Session, SessionAdmin)