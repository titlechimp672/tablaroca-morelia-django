from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse


def vista_cliente_publica(request, username, seccion):
    cliente = get_object_or_404(User, username=username)
    
    # Ejemplo: filtrar blogs por título o descripción
#    blogs = Blog.objects.filter(propietario=cliente, publicar=True).order_by('-fecha_creacion')
    blogs = Blog.objects.filter(propietario=cliente,
                                publicar=True,
                                seccion=seccion).order_by('-fecha_creacion')


    # Construimos el nombre de plantilla: ej. "juanpintor_carpinteria.html"
    template_name = f"{username}_{seccion}.html"
    
    return render(request, template_name, {'blogs': blogs, 'cliente': cliente})

def alternar_publicar(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id, propietario=request.user)

    blog.publicar = not blog.publicar
    blog.save()

    return HttpResponseRedirect(reverse('lista_blogs'))  # Ajusta al nombre de tu vista

@login_required
def alternar_publicar_por_seccion(request, blog_id, seccion):
    blog = get_object_or_404(Blog, id=blog_id, propietario=request.user)
    if blog.seccion != seccion:
        blog.seccion = seccion
        blog.publicar = True
    else:
        blog.publicar = not blog.publicar
    blog.save()
    return redirect('lista_blogs')

#=====================================================================
#=====================================================================
#=====================================================================

@login_required
def lista_blogs(request):
    seccion_activa = request.GET.get('seccion', '')  # lee ?seccion=blog1 si existe

    blogs = Blog.objects.filter(propietario=request.user)
    if seccion_activa:
        blogs = blogs.filter(seccion=seccion_activa)

    blogs = blogs.order_by('-fecha_creacion')
    secciones = ['blog1', 'blog2']  # puedes extender esta lista luego

    return render(request, 'blogs/lista_blogs.html', {
        'blogs': blogs,
        'secciones': secciones,
        'seccion_activa': seccion_activa
    })

from .forms import BlogForm

@login_required
def crear_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            nuevo_blog = form.save(commit=False)
            nuevo_blog.propietario = request.user
            nuevo_blog.save()
            return redirect('lista_blogs')
    else:
        form = BlogForm()
    
    return render(request, 'blogs/crear_blog.html', {'form': form})

from .forms import ImagenForm

@login_required
def subir_imagen(request, blog_id):
    blog = Blog.objects.get(id=blog_id, propietario=request.user)

    # Si ya hay una imagen, no se permite subir más
    if blog.imagenes.count() >= 1:
        return render(request, 'blogs/subir_imagen.html', {
            'blog': blog,
            'form': None,
            'mensaje': 'Este blog ya tiene una imagen. No se pueden subir más.'
        })

    if request.method == 'POST':
        form = ImagenForm(request.POST, request.FILES)
        if form.is_valid():
            nueva_imagen = form.save(commit=False)
            nueva_imagen.blog = blog
            nueva_imagen.save()
            return redirect('lista_blogs')
    else:
        form = ImagenForm()

    return render(request, 'blogs/subir_imagen.html', {'form': form, 'blog': blog})



@login_required
def editar_blog(request, blog_id):
    blog = Blog.objects.get(id=blog_id, propietario=request.user)

    if request.method == 'POST':
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('lista_blogs')
    else:
        form = BlogForm(instance=blog)

    return render(request, 'blogs/editar_blog.html', {'form': form, 'blog': blog})

@login_required
def eliminar_blog(request, blog_id):
    blog = Blog.objects.get(id=blog_id, propietario=request.user)

    if request.method == 'POST':
        blog.delete()
        return redirect('lista_blogs')

    return render(request, 'blogs/eliminar_blog.html', {'blog': blog})

from .models import Imagen

@login_required
def eliminar_imagen(request, imagen_id):
    imagen = Imagen.objects.get(id=imagen_id, blog__propietario=request.user)

    if request.method == 'POST':
        imagen.delete()
        return redirect('lista_blogs')

    return render(request, 'blogs/eliminar_imagen.html', {'imagen': imagen})


