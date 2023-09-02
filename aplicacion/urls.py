from django.urls import path, include
from .views import *

from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', home, name = "home" ),
    path('empleados/', empleados, name = "empleados" ),
    path('cliente/', cliente, name = "cliente" ),
    path('bultos/', bultos, name = "bultos" ),
    path('envio/', envio, name = "envio" ),
   
    
     path('empleado_form/', empleadosForm, name = "empleado_form" ),
     path('cliente_form/', clienteForm, name="cliente_form"),
     path('bulto_form/', bultoForm, name="bulto_form"),
     
     path('buscar_envio/', buscarEnvio, name="buscar_envio"),
     path('buscar2/', buscar2, name="buscar2"),
     
    
     path('create_empleado/', EmpleadoCreate.as_view(), name="create_empleado" ),    
     path('update_empleado/<int:pk>/', EmpleadoUpdate.as_view(), name="update_empleado"),
     path('delete_empleado/<int:pk>/', EmpleadoDelete.as_view(), name="delete_empleado"),
     
     path('create_cliente/', ClienteCreate.as_view(), name="create_cliente" ),    
     path('update_cliente/<int:pk>/', ClienteUpdate.as_view(), name="update_cliente"),
     path('delete_cliente/<int:pk>/', ClienteDelete.as_view(), name="delete_cliente"),
     
     #path('create_/', ClienteCreate.as_view(), name="create_cliente" ),    
     path('update_bulto/<int:pk>/', BultoUpdate.as_view(), name="update_bulto"),
     path('delete_bulto/<int:pk>/', BultoDelete.as_view(), name="delete_bulto"),
     
     path('envio/', EnvioList.as_view(), name="envio" ),
     path('create_envio/', EnvioCreate.as_view(), name="create_envio" ),    
     path('update_envio/<int:pk>/', EnvioUpdate.as_view(), name="update_envio" ),
     path('delete_envio/<int:pk>/', EnvioDelete.as_view(), name="delete_envio" ),
     
     path('login/', login_request, name="login" ),
     path('logout/', LogoutView.as_view(template_name="aplicacion/logout.html"), name="logout" ),
     path('registro/', register, name="registro" ),
     path('editar_perfil/', editarPerfil, name="editar_perfil" ),
     path('agregar_avatar/', agregarAvatar, name="agregar_avatar" ),
     
     path('acerca_de_mi/', acercaDeMi, name="acerca_de_mi" ),
]

