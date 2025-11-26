from django.db import models

# Create your models here.
# class Flight(models.Model):                                 #creamos una clase que hereda de models.Model para representar una tabla. Le añadimod atributos para definir sus campos.
#     origin = models.CharField(max_length=64)                #ojo que no hace falta añadir la clave primaria "id", eso lo va a hacer automaticamente cuando ejecutemos el makemigrations (ver 0001_initial.py)
#     destination = models.CharField(max_length=64)
#     duration = models.IntegerField()

#     def __str__(self):
#         return f"{self.id} : Desde {self.origin} a {self.destination}"   #ojo, que tengo acceso al atributo "id" aunque no esté declarado en la clase
    

#comentamos lo anterior porque ahora queremos tener las ciudades de origen y destino almacenados en una tabla aparte, donde también estará el código del aeropuerto
#importante definir primero la clase Airport y después la clase Flight, ya que al revés la clase ForeignKey daría error de "Airport is not defined"
class Airport(models.Model):
    code = models.CharField(max_length=3) 
    city = models.CharField(max_length=64) 

    def __str__(self):
        return f"{self.city} ({self.code})"


#en la clase Flight, ahora "origin" y "destination" dejan de ser "models.CharField" para ser "models.ForeignKey" y así referenciar a la tabla/clase Airport
#la forma de relacionar ambas tablas es a través de id's internos. Sabemos que Django crea en cada clase de tipo model un campo "id", autoincremental, clave primaria,
#pero además, cuando usamos ForeignKey con origin y destination, también crea un id para cada uno, un origin.id y destination.id que apuntan al id de Airport, de forma 
#que cuando yo añado un registro en Flight, informando origin y destination con instancias de Airport, o sea, con OBJETOS, por detrás Django está insertando en la tabla
#los id que representan a esos aeropuertos dentro de Airport (no solo estoy guardando la city, sino su code, y si hubera más campos, esos también)
class Flight(models.Model):                                 
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures")     #related_name es la forma que vamos a tener de buscar este campo desde la otra tabla, o sea, desde un aeropuerto podemos buscar todos los vuelos que salen de él (departures)
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals")
    duration = models.IntegerField()

    def __str__(self):
        return f"{self.id} : Desde {self.origin} a {self.destination}"   #ojo, que tengo acceso al atributo "id" aunque no esté declarado en la clase

    #Lecture_7_Testing_CI_CD
    def is_valid_flight(self):                                          #creamos esta función que validaremos en Lecture_7_Testing_CI_CD haciendo uso de la herramienta de test de Django
        return self.origin != self.destination and self.duration > 0   #consideramos un vuelo válido aquél que tenga origen distinto del destino y cuya duración sea > 0. Para hacer que falle, simplemente cambiar "and" por "or"

#luego, despues de python manage.py makemigrations y  python manage.py migrate , empezaré a insertar registros en la tabla Airports creando objetos de tipo Airport
# nyc = Airport(code = 'NYC', city= "New York") 
# nyc.save()
# lon = Airport(code = 'LON', city= "London")     
# lon.save()
# tok = Airport(code = 'TOK', city= "Tokyo")    
# tok.save()
# par = Airport(code = 'PAR', city= "Paris")
# par.save()

#y luego crearé objetos de tipo Flight que llevarán como parámetros objetos de tipo Airport
# f1 = Flight(origin = nyc, destination = lon, duration = 415)
# f1.save()
# f2 = Flight(origin = nyc, destination = par, duration = 435)
# f2.save()

#ojo con esto, podemos consultar todos los vuelos que tienen como origen el aeropuerto de nueva york (nyc)
# nyc.departures.all()
# <QuerySet [<Flight: 1 : Desde New York (NYC) a London (LON)>, <Flight: 2 : Desde New York (NYC) a Paris (PAR)>]>

# o todos los vuelos que tienen como llegada el aeropuerto de londres (lon)
# lon.arrivals.all()
# <QuerySet [<Flight: 1 : Desde New York (NYC) a London (LON)>]>


class Passenger(models.Model):                                 
    first = models.CharField(max_length=64)
    last = models.CharField(max_length=64)
    flights = models.ManyToManyField(Flight, blank=True, related_name="passengers")     #ForeignKey se usa cuando la relación es 1:N. ManyToManyField se usa cuando es N:N
                                                                                        #podría no haber puesto aqui el campo "flights" y en la clase Flight haber puesto un campo "passengers" que referenciará con ManyToManyField a esta clase Passenger, por tanto, un vuelo tendría una lista de pasajeros
                                                                                        #de hacerlo así, la clase Passenger tendría que estar por encima de Flight, de lo contrario daría error de "not defined"
    def __str__(self):                                                                  
        return f"{self.first} {self.last}"  
