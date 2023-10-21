from django.db import models
from django.urls import reverse
# Create your models here.

MEALS = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner'),
)

class Cat(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()

    def __str__(self):
        return self.name
    
    # handle redirecting for update and create
    def get_absolute_url(self):
        return reverse('detail', kwargs={'cat_id': self.id})

class Feeding(models.Model):
    date = models.DateField('feeding Date')
    meal = models.CharField(
        max_length=1,
        # add the 'choices' field aka our MEALS tuple variable
        choices=MEALS,
        # set the default value for meal to be 'B'
        default=MEALS[0][0]
    )
    # syntax / column made for FK = (Model)_id
    # in the db the column is called cat_id
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)

    def __str__(self):
        # syntax for getting our meal visuals get_(Model)_display()
        return f"{self.get_meal_display()} on {self.date}"
    
    # reorder our dates so the newest date is first (DESC) the default is (ASC)
    class Meta:
        # the default for ASC is just 'date' but we put a '-' in front of the field to reverse the order (DESC)
        ordering = ['-date']


# feeding_first.cat.description

# feeding_first = {
#     date = '2023-10-06',
#     meal = 'B'
#     cat = {
#         name = rubber biscuit
#         desciption = laskdjfs;aldkjf
#         age = 5
#         breed = lkasdjf
#     }
# }    

