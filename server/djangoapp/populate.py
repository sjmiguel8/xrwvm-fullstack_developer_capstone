from django.utils import timezone
from .models import CarMake, CarModel

def initiate():
    # Create car makes
    honda = CarMake.objects.create(
        name="Honda",
        description="Japanese automaker known for reliability"
    )
    
    toyota = CarMake.objects.create(
        name="Toyota",
        description="World's largest automaker"
    )
    
    ford = CarMake.objects.create(
        name="Ford",
        description="American automotive manufacturer"
    )
    
    chevrolet = CarMake.objects.create(
        name="Chevrolet",
        description="American automobile division of GM"
    )

    # Create car models
    # Honda models
    CarModel.objects.create(
        car_make=honda,
        name="Civic",
        car_type="SEDAN",
        year=2023
    )
    
    CarModel.objects.create(
        car_make=honda,
        name="Accord",
        car_type="SEDAN",
        year=2023
    )

    # Toyota models
    CarModel.objects.create(
        car_make=toyota,
        name="Camry",
        car_type="SEDAN",
        year=2023
    )
    
    CarModel.objects.create(
        car_make=toyota,
        name="Corolla",
        car_type="SEDAN",
        year=2023
    )

    # Ford models
    CarModel.objects.create(
        car_make=ford,
        name="F-150",
        car_type="SUV",
        year=2023
    )
    
    CarModel.objects.create(
        car_make=ford,
        name="Mustang",
        car_type="SPORT",
        year=2023
    )

    # Chevrolet models
    CarModel.objects.create(
        car_make=chevrolet,
        name="Silverado",
        car_type="SUV",
        year=2023
    )
    
    CarModel.objects.create(
        car_make=chevrolet,
        name="Camaro",
        car_type="SPORT",
        year=2023
    )

    print("Car makes and models have been populated!")
