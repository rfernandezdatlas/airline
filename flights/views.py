from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Flight, Passenger

# Create your views here.                     

def index(request):                                     #la página principal mostrará una lista con todos los vuelos
    return render(request, "flights/index.html", {
        "flights": Flight.objects.all()
    }) 

def flight(request, flight_id):                          #cada página http://127.0.0.1:8000/flight/1 , 2 , 3, ... muestra los datos del vuelo 1 , 2, 3....
    #flight = Flight.objects.get(id=flight_id)            #recuperamos de la tabla/clase Flight el vuelo buscándolo por su id. En vez de get(id=flightID) podría haber usado get(pk=flightID), donde "pk" significa "primary key"
    flight = get_object_or_404(Flight, id=flight_id)     #Lecture_7_Testing_CI_CD - ésta es una forma rápida, de hecho se le llama "shortcut", de hacer lo mismo que la línea anterior o devolver un 404 al navegador en caso de no encontrar resultado
    passengers = flight.passengers.all()                 #recupera la lista de pasajeros del vuelo, usando el "related_name" "passengers". Ojo, podría haber usado "Passengers.objects.filter(flights=flight).all()" y funcionaría igual.
    
    return render(request, "flights/flight.html", {                      
        "flight": flight,                                   
        "passengers": passengers,
        "non_passengers": Passenger.objects.exclude(flights=flight).all()  #necesito la lista de personas que NO son pasajeros de este vuelo para poder mostrarlos en un combo desplegable para añadir nuevos pasajeros al vuelo
    })


def book(request, flight_id):
    if request.method == "POST":            
        flight = Flight.objects.get(pk=flight_id)   
        passenger = Passenger.objects.get(pk=int(request.POST["passenger_id"]))  #recuperamos del POST el dato informado en el campo llamado "passenger_id" de "flight.html"
        
        passenger.flights.add(flight)             #el atributo "flights" de la clase "Passenger" a la que pertenece "passenger" es una lista de vuelos (o quizá mejor dicho un set de vuelos) y por eso me permite ejecutar la función add para añadir un nuevo vuelo
                                                  #ojo, también podría haber hecho flight.passengers.add(passenger), ya que la clase Passenger tiene el campo flights de tipo ManyToManyField relacionado con la clase Flights con related_name = "passengers", 
                                                  # lo que significa que desde "flight" puedo acceder a "passengers"

        return HttpResponseRedirect(reverse("flights:flight", args=(flight_id,)))  #en este caso, además de identificar la url con app:nombre del path (en urls.py), necesitamos pasarle el dato "flight_id" (así está definido en urls.py: path("<int:flight_id>", views.flight, name="flight")). Ese dato se pasa como argumento (args) que por definición debe ser una tupla, en este caso de un solo elemento
        
    #return HttpResponseRedirect(reverse("flights:flight", args=(flight_id,))) --- no es necesario definir qué pasa si el method no es POST, ya que "book" no nos lleva a ninguna pagina, en todo momento estamos en la pagina de flight.html