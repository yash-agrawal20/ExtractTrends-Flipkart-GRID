from django.shortcuts import render
from django.http import HttpResponse
from .models import Instadata



# Create your views here.
def index(request):
    posts = Instadata.objects.all()
    context = {
        'posts' : posts
    }
    return render(request, "GRID_app/index.html", context)

def search(request):
    form= UserForm(request.POST)
    if form.is_valid():
        q = form.cleaned_data['srch-item']
    
    sql = f"SELECT CAT,SUB_CAT FROM INSTADATA WHERE KWORDS LIKE %{q}%"

    posts = Instadata.objects.raw(sql)[:2]

    cont = {
        'posts' : posts
    }
    return render(request, "GRID_app/index.html", cont)