import re
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.urls import reverse

# Create your views here.
def index(request):                                   
    if not request.user.is_authenticated:                       #la pagina principal de la app "users" lo primero que hace es validar si hay un usario logado, y eso se puede hacer directamente desde el "request", que tiene un atributo "user" y este a su vez un atributo "is_authenticated"
        return HttpResponseRedirect(reverse("users:login"))     #y si no hay usuario logado, nos lleva a la pagina de login.html
    
    return render(request, "users/user.html")                   #si el usuario está logado, renderizamos una pagina de usuario que muestre su nombre y mail. No es necesario
                                                                #pasarle ningún contexto porque el html tiene acceso a "request", el cual tiene el atributo "user", que es lo que se informa cuando hacemos "login"
                                                                #fíjate que este user.html no tiene definido un path en urls.py, ya que desde esta página no vamos a ejecutar ningún método.
                                                                #y sin embargo, index, que sí tiene un path en urls.py, en este caso no tiene un index.html asociado, no lo necesita, porque o te manda a login.html o a user.html
def login_view(request): 
    if request.method == "POST":
        username = request.POST["username"]  
        password = request.POST["password"]  
        user = authenticate(request, username = username, password = password)  #valida si el name y pass son correctos (si está dado de alta en la aplicación) y si lo son me devuelve el usuario. Para que sea válido, como administradores antes hemos tenido que dar de alta al usuario en la apliación.

        if user is not None:                                        #si user está informado con un usuario, es que las credenciales eran válidas
            login(request, user)                                    #entonces lo logamos (imagino que informa el atributo "user" de "request" con nuestro "user" devuelto por el "authenticate" )
            return HttpResponseRedirect(reverse("users:index"))     #y lo llevamos a la página principal
        else:                                                       #si no,
            return render(request, "users/login.html", {            #devolvemos la própia página con un contexto adicional para mostrar un mensaje de error.
                "message": "Credenciales no válidas."               #por lo tanto modificaré "login.html" para validar que si nos llega "message" informado, se muestre dicho mensaje en la página
            }) 

    return render(request, "users/login.html") 
    
def logout_view(request):    
    logout(request)                                                 #hace logout, quitando al user del request
    return render(request, "users/login.html", {                    #y renderizamos la página de login.html, pero enviando por contexto un mensaje diferente al que se enviaba cuando  "Credenciales no válidas."
        "message": "Usuario deslogado."                              #No necesitamos crear un logout.html, podemos aprovechar la de login para decir que el anterior usuario se ha salido y al mismo tiempo permitir hacer login de nuevo
    }) 
