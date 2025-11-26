from urllib import response
from django.test import TestCase, Client
from django.db.models import Max

from .models import *

#-------------------------------Para ejecutar los tests, desde el terminal ejecutar:  python manage.py test 

# Create your tests here.
class FlightTestCase(TestCase):
    def setUp(self):
        #crear aeropuertos para las pruebas. Estos datos existirán solo para las pruebas, no se añadirán realmente a la bbdd
        a1 = Airport.objects.create(code='AAA', city='A')
        a2 = Airport.objects.create(code='BBB', city='B')
        
        #crear vuelos para las pruebas
        Flight.objects.create(origin=a1, destination=a2, duration=100)
        Flight.objects.create(origin=a1, destination=a1, duration=200)
        Flight.objects.create(origin=a1, destination=a2, duration=-100)

#pruebas sobre la bbdd
    def test_departures_count(self):
        a = Airport.objects.get(code='AAA')
        self.assertEqual(a.departures.count(), 3)       #valida que la cantidad de vuelos que salen de A es 3

    def test_arrivals_count(self):
        a = Airport.objects.get(code='AAA')
        self.assertEqual(a.arrivals.count(), 1)         #valida que la cantidad de vuelos que llegan a A es 1
    
    def test_valid_flight(self):
        a1 = Airport.objects.get(code='AAA')          
        a2 = Airport.objects.get(code='BBB')
        f =  Flight.objects.get(origin=a1, destination=a2, duration=100)
        self.assertTrue(f.is_valid_flight())            #valida que el vuelo con origen A y destino B y duración 100 es válido
    
    def test_invalid_flight_destination(self):
        a1 = Airport.objects.get(code='AAA')
        f =  Flight.objects.get(origin=a1, destination=a1)
        self.assertFalse(f.is_valid_flight())           #valida que el vuelo con origen y destino A NO es válido

    def test_invalid_flight_duration(self):
        f =  Flight.objects.get(duration=-100)
        self.assertFalse(f.is_valid_flight())           #valida que el vuelo con duración negativa NO es válido

#pruebas de navegación en el servidor
    def test_index(self):
        c = Client()
        response = c.get("/flights/")                               #accede a la página principal (index.html)
        self.assertEqual(response.status_code, 200)                 #verifica que el acceso es correcto
        self.assertEqual(response.context["flights"].count(), 3)    #verifica que se muestran 3 vuelos (OJO,los 3 vuelos dummys que se configuraron en setUp)

    def test_valid_flight_page(self):                               #Recupera el vuelo con origen y destino en el aeropuerto AAA y valida que se accede a la página del vuelo correctamente
        a1 = Airport.objects.get(code='AAA')
        f =  Flight.objects.get(origin=a1, destination=a1)

        c = Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)

    def test_invalid_flight_page(self):                                 #Recupera el último vuelo (el que tenga el id más alto) e intenta acceder a la página del siguiente vuelo, que logicamente no existe. Valida que recibimos un 404.
        max_id = Flight.objects.all().aggregate(Max("id"))["id__max"]   # aggregate() es un método que calcula funciones de agregación sobre un QuerySet.
                                                                        # Max("id") es la función de agregación que pide el valor máximo del campo id de todos los objetos Flight.
                                                                        # El resultado de aggregate() no es un QuerySet normal, sino un diccionario con la(s) clave(s) que representa(n) la agregación. En este caso, solo hay una clave (id__max), y accedo a su valor con ["id__max"]
        c = Client()
        response = c.get(f"/flights/{max_id + 1}")
        self.assertEqual(response.status_code, 404)

    def test_flight_page_passengers(self):                              #Valida que la página de un vuelo contiene la cantidad de pasajeros correcta
        f = Flight.objects.get(pk=1)                                    #recupera el vuelo con id = 1, o sea (origin=a1, destination=a2, duration=100)
        p= Passenger.objects.create(first="Alicia", last="Adams")       #crea un pasajero, solo existirá en esta prueba
        p.flights.add(f)                                                #Añadimos el vuelo al pasajero. No puedes hacer p= Passenger.objects.create(first="Alicia", last="Adams", flights=f) porque "flights" es un campo ManyToManyField. Es obligatorio usar add()

        c = Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["passengers"].count(), 1)

    def test_flight_page_non_passengers(self):                          #Valida que la página de un vuelo contiene la cantidad de no-pasajeros correcta
        f = Flight.objects.get(pk=1)
        Passenger.objects.create(first="Alicia", last="Adams")

        c = Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["non_passengers"].count(), 1)