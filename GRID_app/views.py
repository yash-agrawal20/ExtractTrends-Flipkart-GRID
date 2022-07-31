from django.shortcuts import render
from django.http import HttpResponse
from .models import Employees

# Create your views here.
def index(request):
    employees = Employees.objects.all()
    context = {
        'employees' : employees
    }
    return render(request, "GRID_app/index.html", context)