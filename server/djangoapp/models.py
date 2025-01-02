# Uncomment the following imports before adding the Model code

from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator

class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.name

class CarModel(models.Model):
    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        ('SPORT', 'Sport'),
        ('COUPE', 'Coupe'),
        ('MINIVAN', 'Mini Van'),
    ]

    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    car_type = models.CharField(max_length=10, choices=CAR_TYPES)
    year = models.IntegerField(
        validators=[
            MinValueValidator(2015),
            MaxValueValidator(2023)
        ]
    )
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.car_make.name} {self.name} ({self.year})"
        
class Dealer(models.Model):
    id = models.IntegerField(primary_key=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    st = models.CharField(max_length=2)  # State abbreviation
    address = models.CharField(max_length=100)
    zip = models.CharField(max_length=10)
    lat = models.FloatField(default=0.0)
    long = models.FloatField(default=0.0)
    short_name = models.CharField(max_length=100, default='')
    full_name = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name

class Review(models.Model):
    id = models.AutoField(primary_key=True)
    dealership = models.ForeignKey(Dealer, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    review = models.TextField()
    purchase = models.BooleanField(default=False)
    purchase_date = models.DateField(null=True, blank=True)
    car_make = models.CharField(max_length=100)
    car_model = models.CharField(max_length=100)
    car_year = models.IntegerField()

class CarDealer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name

# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many
# Car Models, using ForeignKey field)
# - Name
# - Type (CharField with a choices argument to provide limited choices
# such as Sedan, SUV, WAGON, etc.)
# - Year (IntegerField) with min value 2015 and max value 2023
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
