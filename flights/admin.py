from django.contrib import admin

from .models import *
# Register your models here.

class FlightAdmin(admin.ModelAdmin):
    list_display = ("id", "origin", "destination", "duration")  #la forma de configurar estos atributos es con tuplas

class PassengerAdmin(admin.ModelAdmin):
    filter_horizontal = ("flights",)                            #la forma de configurar estos atributos es con tuplas

admin.site.register(Airport)
admin.site.register(Flight, FlightAdmin)  #de esta forma le decimos a admin que cuando entremos a la tabla Flight, nos pinte los datos como hemos especificado en FlightAdmin, sustiyendo a "def __str__(self):"" en la clase "Flight" de "models.py"
admin.site.register(Passenger, PassengerAdmin) #con filter_horizontal podemos manejar campos ManyToManyField. De esta manera, al entrar a un pasajero, vamos a ver dos recuadros, uno con los vuelos disponibles y otro con los vuelos que tiene el pasajero, y podemos facilmente mover vuelos de un cuadro a otro