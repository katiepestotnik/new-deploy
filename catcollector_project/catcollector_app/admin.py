from django.contrib import admin
from .models import Cat, Feeding, Toy, Photo
# Register your models here.
admin.site.register(Cat)
# register the new Feeding model
admin.site.register(Feeding)
admin.site.register(Toy)
admin.site.register(Photo)