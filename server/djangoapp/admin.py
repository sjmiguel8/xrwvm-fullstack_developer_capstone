from django.contrib import admin

<<<<<<< HEAD
from django.contrib import admin
from .models import CarModel, CarMake

=======
from .models import CarMake, CarModel, Dealer, Review
>>>>>>> 5640e36cdccbbac143706c3b2726d6031e25c264

admin.site.register(CarMake)
admin.site.register(CarModel)
admin.site.register(Dealer)
admin.site.register(Review)
