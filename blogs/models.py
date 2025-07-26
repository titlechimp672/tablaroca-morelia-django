from django.db import models
from django.contrib.auth.models import User
import os

def renombrar_imagen(instance, filename):
    blog_id = instance.blog.id or 'temp'

    # Contar cuántas imágenes ya existen del blog
    total = Imagen.objects.filter(blog=instance.blog).count() + 1
    extension = filename.split('.')[-1]
    nuevo_nombre = f"blog{blog_id}_{total:03d}.{extension}"

    return os.path.join('imagenes_blogs', nuevo_nombre)

class Blog(models.Model):
    propietario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    publicar = models.BooleanField(default=False)
    seccion = models.CharField(max_length=100, default='blog1')
    
    def __str__(self):
        return self.titulo

class Imagen(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to=renombrar_imagen)

    def __str__(self):
        return f"Imagen de {self.blog.titulo}"
