from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy

from .models import Empleado, Cliente, Bulto, Envio, Avatar
from .forms import *

from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required



def home(request):
    return render(request, "aplicacion/home.html")

@login_required
def empleados(request):
    empleados = Empleado.objects.all()
    contexto = {'empleados': empleados, 'titulo': 'Listado de Empleados'}
    return render(request, 'aplicacion/empleados.html', contexto)

@login_required
def cliente(request):
    cliente = Cliente.objects.all()
    contexto = {'cliente': cliente}
    return render(request, "aplicacion/cliente.html", contexto)

@login_required
def bultos(request):
    bultos = Bulto.objects.all()
    contexto = {'bultos': bultos}
    return render(request, "aplicacion/bultos.html", contexto)

@login_required
def envio(request):
    envio =Envio.objects.all()
    contexto = {'envios': envio}
    return render(request, "aplicacion/envio.html", contexto)


## Agregar Empleados

@login_required
def empleadosForm(request):
    if request.method == "POST":
        nombre = request.POST['nombre']
        cargo = request.POST['cargo']
    if 'fecha_contratacion' in request.POST:
        fecha_contratacion = request.POST['fecha_contratacion']
        empleado = Empleado(nombreApellido=nombre, cargo=cargo, fecha_contratacion=fecha_contratacion)
        empleado.save()
        return HttpResponse("Se agregó el nuevo empleado")
    
    return render(request, "aplicacion/empleadoForm.html")
                         
## Agregar Cliente

@login_required
def clienteForm(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            nombreApellido = form.cleaned_data.get('nombreApellido')
            telefono_contacto = form.cleaned_data.get('telefono_contacto')
            email = form.cleaned_data.get('email')
            cliente = Cliente(nombreApellido=nombreApellido, telefono_contacto=telefono_contacto, email=email)
            cliente.save()
            return render(request, "aplicacion/base.html")  
    else:
        form = ClienteForm()
    
    return render(request, "aplicacion/clienteForm.html", {"form": form})

##Agregar Bulto

@login_required
def bultoForm(request):
    if request.method == 'POST':
        form = BultoForm(request.POST)
        if form.is_valid():
            descripcion = form.cleaned_data.get('descripcion')
            cantidad = form.cleaned_data.get('cantidad')
            bulto = Bulto(descripcion=descripcion, cantidad=cantidad)
            bulto.save()
            return render(request, "aplicacion/base.html")  
    else:
        form = BultoForm()
    return render(request, 'aplicacion/bultoForm.html', {'form': form})

##Buscar Envios

@login_required
def buscarEnvio(request):
    return render(request, "aplicacion/buscarEnvio.html")

def buscar2(request):
    if request.GET['buscar']:
        patron = request.GET['buscar']
        envio = Envio.objects.filter(cliente__nombreApellido__icontains=patron)
        contexto = {'envios': envio} 
        return render(request, "aplicacion/envio.html", contexto)
    return HttpResponse("No se ingreso nada a buscar")



##Crear, modificar y eliminar Empleados
    
class EmpleadoCreate(LoginRequiredMixin, CreateView):
    model = Empleado
    fields = ['nombreApellido', 'cargo', 'fecha_contratacion']
    success_url = reverse_lazy('empleados')    

class EmpleadoUpdate(LoginRequiredMixin, UpdateView):
    model = Empleado
    fields = ['nombreApellido', 'cargo', 'fecha_contratacion']
    success_url = reverse_lazy('empleados')

class EmpleadoDelete(LoginRequiredMixin, DeleteView):
    model = Empleado
    success_url = reverse_lazy('empleados')
        
     
##Crear, modificar y eliminar Clientes


class ClienteCreate(LoginRequiredMixin, CreateView):
    model = Cliente
    fields = ['nombreApellido', 'telefono_contacto', 'email']
    success_url = reverse_lazy('cliente')    

class ClienteUpdate(LoginRequiredMixin, UpdateView):
    model = Cliente
    fields = ['nombreApellido', 'telefono_contacto', 'email']
    success_url = reverse_lazy('cliente')

class ClienteDelete(LoginRequiredMixin, DeleteView):
    model = Cliente
    success_url = reverse_lazy('cliente')
    
    
##Crear, modificar y eliminar Bultos

class BultoCreate(LoginRequiredMixin, CreateView):
    model = Bulto
    fields = ['descripcion', 'cantidad']
    success_url = reverse_lazy('bultos')    

class BultoUpdate(LoginRequiredMixin, UpdateView):
    model = Bulto
    fields = ['descripcion', 'cantidad']
    success_url = reverse_lazy('bultos')

class BultoDelete(LoginRequiredMixin, DeleteView):
    model = Bulto
    success_url = reverse_lazy('bultos')
    
    
##Crear, modificar y eliminar Envios

class EnvioList(LoginRequiredMixin, ListView):
    model = Envio

class EnvioCreate(LoginRequiredMixin, CreateView):
    model = Envio
    fields = ['cliente', 'destino', 'bultos']
    success_url = reverse_lazy('envio')    

class EnvioUpdate(LoginRequiredMixin, UpdateView):
    model = Envio
    fields = ['cliente', 'destino', 'bultos']
    success_url = reverse_lazy('envio')

class EnvioDelete(LoginRequiredMixin, DeleteView):
    model = Envio
    success_url = reverse_lazy('envio')
    
    
##Login/logout

def login_request(request):
    if request.method == "POST":
        miForm = AuthenticationForm(request, data=request.POST)
        if miForm.is_valid():
            usuario = miForm.cleaned_data.get('username')
            password = miForm.cleaned_data.get('password')
            user = authenticate(username=usuario, password=password)
            if user is not None:
                login(request, user)
                try:
                    avatar = Avatar.objects.get(user=request.user.id).imagen.url
                except:
                    avatar = "media/avatares/default.png"
                finally:
                    request.session["avatar"] = avatar
                return render(request, "aplicacion/base.html", {'mensaje': f'Bienvenido a nuestro sitio {usuario}'})
            else:
                return render(request, "aplicacion/login.html", {'form': miForm, 'mensaje': f'Los datos son inválidos'})
        else:
            return render(request, "aplicacion/login.html", {'form': miForm, 'mensaje': f'Los datos son inválidos'})

    miForm =   AuthenticationForm()      

    return render(request, "aplicacion/login.html", {"form":miForm})    


#Registro de usuario

def register(request):
    if request.method == "POST":
        miForm = RegistroUsuariosForm(request.POST)
        if miForm.is_valid():
            usuario = miForm.cleaned_data.get('username')
            miForm.save()
            return render(request, "aplicacion/base.html")
    else:
        miForm =   RegistroUsuariosForm()      
    return render(request, "aplicacion/registro.html", {"form":miForm}) 


#Editar perfil

@login_required
def editarPerfil(request):
    usuario = request.user
    if request.method == "POST":
        form = UserEditForm(request.POST)
        if form.is_valid():
            usuario.email = form.cleaned_data.get('email')
            usuario.password1 = form.cleaned_data.get('password1')
            usuario.password2 = form.cleaned_data.get('password2')
            usuario.first_name = form.cleaned_data.get('first_name')
            usuario.last_name = form.cleaned_data.get('last_name')
            usuario.save()
            return render(request,"aplicacion/base.html")
        else:
            return render(request,"aplicacion/editarPerfil.html", {'form': form, 'usuario': usuario.username})
    else:
        form = UserEditForm(instance=usuario)
    return render(request, "aplicacion/editarPerfil.html", {'form': form, 'usuario': usuario.username})


#Agregar Avatar

@login_required
def agregarAvatar(request):
    if request.method == "POST":
        form = AvatarFormulario(request.POST, request.FILES)
        if form.is_valid():
            u = User.objects.get(username=request.user)
            avatarViejo = Avatar.objects.filter(user=u)
            if len(avatarViejo) > 0:
                for i in range(len(avatarViejo)):
                    avatarViejo[i].delete()
            avatar = Avatar(user=u, imagen=form.cleaned_data['imagen'])
            avatar.save()
            imagen = Avatar.objects.get(user=request.user.id).imagen.url
            request.session["avatar"] = imagen
            return render(request,"aplicacion/base.html")
    else:
        form = AvatarFormulario()
    return render(request, "aplicacion/agregarAvatar.html", {'form': form })


##Acerca de mi

def acercaDeMi(request):
    return render(request, 'aplicacion/acercaDeMi.html', {})

    
    
    

    