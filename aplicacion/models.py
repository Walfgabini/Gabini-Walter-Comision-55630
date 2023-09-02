from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Empleado(models.Model):
    nombreApellido = models.CharField(max_length=100)
    cargo = models.CharField(max_length=50)
    fecha_contratacion = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.nombreApellido} - ({self.cargo}) - ({self.fecha_contratacion})"


class Cliente(models.Model):
    nombreApellido = models.CharField(max_length=100)
    telefono_contacto = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return f"{self.nombreApellido} - ({self.telefono_contacto}) - ({self.email})"
    
    
class Bulto(models.Model):
    descripcion = models.TextField()
    cantidad = models.IntegerField()

    def __str__(self):
        return f"{self.descripcion} - ({self.cantidad})"
    

class Envio(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    destino = models.CharField(max_length=100)
    bultos = models.ManyToManyField(Bulto)
    

    def __str__(self):
        return f"{self.cliente} - ({self.destino})"
    
    
class Avatar(models.Model):
    imagen = models.ImageField(upload_to="avatares")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} {self.imagen}"
    

