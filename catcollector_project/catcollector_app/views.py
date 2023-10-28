from django.shortcuts import render, redirect
from .models import Cat, Toy, Photo
from .forms import FeedingForm
# from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
# import login_required decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

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

@login_required
def cats_index(request):
    # filter the Cat objects to find the lOGGED IN (request.user) user's cats
    cats = Cat.objects.filter(user=request.user)
    return render(request, 'cats/index.html', {'cats': cats})

@login_required
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

@login_required
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

@login_required
def assoc_toy(request, pk, toy_pk):
    Cat.objects.get(id=pk).toys.add(toy_pk)
    return redirect('detail', cat_id=pk)

#delete toy for specific cat
@login_required
def assoc_delete(request, pk, toy_pk):
    Cat.objects.get(id=pk).toys.remove(toy_pk)
    return redirect('detail', cat_id=pk)

## add photo view
@login_required
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

def signup(request):
    error_message = ''
    if request.method == 'POST':
        # our user form object that includes user data from the browser's form
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # add the user to the database
            user = form.save()
            # login the user! they signed up lets log them in!
            login(request, user)
            return redirect('index')
        else: 
            error_message = 'Invalid sign up - try again'
    # a bad POST OR GET request, render signup.html with an empty form
    form = UserCreationForm()
    context = {
        'form': form, 
        'error_message': error_message,
    }
    return render(request, 'registration/signup.html', context)

# class based views
class CatCreate(LoginRequiredMixin, CreateView):
    model = Cat
    fields = ['name', 'breed', 'description', 'age']
    # optional 1 way
    #success_url = '/cats/{cat_id}'

    # inherited (built-in) method is called a valid cat form is being submitted
    def form_valid(self, form):
        # assign the logged in user (self.request.user)
        form.instance.user = self.request.user
        return super().form_valid(form)

class CatUpdate(LoginRequiredMixin, UpdateView):
    model = Cat
    fields = ['breed', 'description', 'age']

class CatDelete(LoginRequiredMixin, DeleteView):
    model = Cat
    success_url = '/cats'

## TOY CBVs ##
class ToyList(LoginRequiredMixin, ListView):
    model = Toy

class ToyDetail(LoginRequiredMixin, DetailView):
    model = Toy

class ToyCreate(LoginRequiredMixin, CreateView):
    model = Toy
    fields = '__all__'

class ToyUpdate(LoginRequiredMixin, UpdateView):
    model = Toy
    fields = ['name', 'color']

class ToyDelete(LoginRequiredMixin, DeleteView):
    model = Toy
    success_url = '/toys'