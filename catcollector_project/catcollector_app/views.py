from django.shortcuts import render
from .models import Cat
# from django.http import HttpResponse

# Add this cats list below the imports
# cats = [
#   {'name': 'Lolo', 'breed': 'tabby', 'description': 'furry little demon', 'age': 3},
#   {'name': 'Sachi', 'breed': 'calico', 'description': 'gentle and loving', 'age': 0},
# ]


# Create your views here.
def home(request):
    return render(request, 'cats/home.html') 
    # return res.render('home.ejs', context)

def about(request):
    return render(request, 'cats/about.html')

def cats_index(request):
    cats = Cat.objects.all()
    return render(request, 'cats/index.html', {'cats': cats})

def cats_detail(request, cat_id):
    cat = Cat.objects.get(id=cat_id)
    return render(request, 'cats/detail.html', {'cat': cat})