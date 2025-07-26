from django.urls import path
from . import views

urlpatterns = [
    # URLs de administración
    path('', views.lista_blogs, name='lista_blogs'),
    path('crear/', views.crear_blog, name='crear_blog'),
    path('editar/<int:blog_id>/', views.editar_blog, name='editar_blog'),
    path('eliminar/<int:blog_id>/', views.eliminar_blog, name='eliminar_blog'),
    path('subir-imagen/<int:blog_id>/', views.subir_imagen, name='subir_imagen'),
    path('eliminar-imagen/<int:imagen_id>/', views.eliminar_imagen, name='eliminar_imagen'),
    path('publicar/<int:blog_id>/', views.alternar_publicar, name='alternar_publicar'),
    path('publicar/<int:blog_id>/<str:seccion>/', views.alternar_publicar_por_seccion, name='alternar_publicar_por_seccion'),
    
    # URL genérica (va AL FINAL)
    path('<str:username>/<str:seccion>/', views.vista_cliente_publica, name='vista_publica_cliente'),
]

