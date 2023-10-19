from django.shortcuts import render
from .models import Cat
# from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Add this cats list below the imports
# cats = [
#   {'name': 'Lolo', 'breed': 'tabby', 'description': 'furry little demon', 'age': 3},
#   {'name': 'Sachi', 'breed': 'calico', 'description': 'gentle and loving', 'age': 0},
# ]


# Create your views here.
# view functions
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

# class based views
class CatCreate(CreateView):
    model = Cat
    fields = '__all__'
    # optional 1 way
    #success_url = '/cats/{cat_id}'

class CatUpdate(UpdateView):
    model = Cat
    fields = ['breed', 'description', 'age']

class CatDelete(DeleteView):
    model = Cat
    success_url = '/cats'