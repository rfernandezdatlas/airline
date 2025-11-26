from django.contrib import admin
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User

#generado con IA. Con esta clase puedo ver desde /admin la tabla Session, que contiene un session_key, session_data y expire_date. 
#session_data es un chorro de caracateres, que contiene información de 3 campos, el primero de los cuales es el id del usuario logado. Lo que hace la función user()
#es recuperar esa id, y con ella ir a la tabla User para recuperar el usuario
#readonly_fields añade campos a la vista de un registro particular de la tabla en modo no editable, y en este caso mostrará el valor devuelto por la función "session_data_pretty", que
#simplemente devuelve el chorro de "Session data" decodificado
class SessionAdmin(admin.ModelAdmin):
    list_display = ["session_key", "user", "expire_date"]
    readonly_fields = ["session_data_pretty"]

    def user(self, obj):
        """Devuelve el usuario asociado a esta sesión (si lo hay)."""
        data = obj.get_decoded()
        user_id = data.get("_auth_user_id")

        if user_id:
            try:
                return User.objects.get(id=user_id)
            except User.DoesNotExist:
                return "Usuario no encontrado"
        return "Anónimo"

    def session_data_pretty(self, obj):
        """Muestra el contenido decodificado de la sesión en el detalle."""
        return obj.get_decoded()

admin.site.register(Session, SessionAdmin)