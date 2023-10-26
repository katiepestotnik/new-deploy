from django.shortcuts import render, redirect
from .models import Cat, Toy, Photo
from .forms import FeedingForm
# from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

## imports for photo aws
import uuid
import boto3
## to access .env keys
import os

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
    toys = Toy
    #grab the toys the cat doesnt have 
    # BUT FIRST lets get a list of toys the cat does own
    id_list = cat.toys.all().values_list('id')
    # EXCLUDE all the toy ID's that the cat owns so we can see a list of toys it DOESNT have
    ## .exclude(column__in = query options)
    toys_cat_doesnt_have = Toy.objects.exclude(id__in=id_list)

    feeding_form = FeedingForm()
    return render(request, 'cats/detail.html', 
        {
            'cat': cat,
            'feeding_form': feeding_form,
            'toys': toys_cat_doesnt_have
        })

def add_feeding(request, pk):
    form = FeedingForm(request.POST)
    # check if the form is 'clean' with proper data and confirm all data returns to the server
    if form.is_valid():
        # it saves the data from the FeedingForm, BUT doesnt save it to the database when we use commit=False
        new_feeding = form.save(commit=False)
        # this is our Feeding model, so we can still access cat_id column with our form
        new_feeding.cat_id = pk
        new_feeding.save() # puts the date, meal, and cat_id into our db
    return redirect('detail', cat_id=pk)

def assoc_toy(request, pk, toy_pk):
    Cat.objects.get(id=pk).toys.add(toy_pk)
    return redirect('detail', cat_id=pk)
#delete toy for specific cat
def assoc_delete(request, pk, toy_pk):
    Cat.objects.get(id=pk).toys.remove(toy_pk)
    return redirect('detail', cat_id=pk)

## add photo view
def add_photo(request, cat_id):
    photo_file = request.FILES.get('photo_file', None)
    print(photo_file)
    if photo_file:
        ## make variable to use sdk to talk with aws
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        print(f'this is the key {key}')
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            url = f'{os.environ["S3_BASE_URL"]}{bucket}/{key}'
            Photo.objects.create(url=url, cat_id=cat_id)
        except Exception as e:
            print('An error occured uploading file to S3')
            print(e)
    return redirect('detail', cat_id=cat_id)


# class based views
class CatCreate(CreateView):
    model = Cat
    fields = ['name', 'breed', 'description', 'age']
    # optional 1 way
    #success_url = '/cats/{cat_id}'

class CatUpdate(UpdateView):
    model = Cat
    fields = ['breed', 'description', 'age']

class CatDelete(DeleteView):
    model = Cat
    success_url = '/cats'

## TOY CBVs ##
class ToyList(ListView):
    model = Toy

class ToyDetail(DetailView):
    model = Toy

class ToyCreate(CreateView):
    model = Toy
    fields = '__all__'

class ToyUpdate(UpdateView):
    model = Toy
    fields = ['name', 'color']

class ToyDelete(DeleteView):
    model = Toy
    success_url = '/toys'