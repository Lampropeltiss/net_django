from django.views.generic import ListView
from django.shortcuts import render

from .models import Student, Teacher


def students_list(request):
    ordering = 'group'
    template = 'school/students_list.html'
    students = Student.objects.all().prefetch_related('teachers')
    context = {
        'students_list': students.order_by(ordering)
    }
    return render(request, template, context)

def teachers_list(request):
    ordering = 'name'
    template = 'school/teachers_list.html'
    teachers = Teacher.objects.all().prefetch_related('students')
    context = {
        'teachers_list': teachers.order_by(ordering)
    }
    return render(request, template, context)
