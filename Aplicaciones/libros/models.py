from django.contrib.auth.models import User
from django.db import models

# Modelo PerfilUsuario
class PerfilUsuario(models.Model):
    # Relación uno a uno con el modelo User
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    
    # Campos adicionales
    telefono = models.CharField(max_length=10, blank=True, null=True)
    direccion = models.CharField(max_length=100, blank=True, null=True)
    
    # Campos para roles
    ROL_CHOICES = [
        ('Administrador', 'Administrador'),
        ('Vendedor', 'Vendedor'),
        ('Comprador', 'Comprador'),
    ]
    rol = models.CharField(max_length=50, choices=ROL_CHOICES, default='Comprador')
    def __str__(self):
        return self.user.username


# Modelo Categoría
class Categoria(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

# Modelo Libro


class Libro(models.Model):
    titulo = models.CharField(max_length=255)
    autor = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='libros/', null=True, blank=True) 
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='libros')
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='libros_en_venta')
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo

# Modelo Transacciones
ESTADO_TRANSACCION = [
    ('Pendiente', 'Pendiente'),
    ('Completada', 'Completada'),
]

class Transacciones(models.Model):
    comprador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='libros_comprados')
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=50, choices=ESTADO_TRANSACCION, default='Pendiente')

    def __str__(self):
        return f'{self.comprador.username} compró {self.libro.titulo}'
