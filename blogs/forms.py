from django import forms
from .models import Blog, Imagen

class BlogForm(forms.ModelForm):
    # Definir el campo seccion explícitamente con choices
    seccion = forms.ChoiceField(
        choices=[
            ('blog1', 'Diseño Empresarial'),
            ('blog2', 'Diseño Personal'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Diseño',
        help_text='Selecciona el diseño visual que usará tu blog'
    )
    
    class Meta:
        model = Blog
        fields = ['titulo', 'descripcion', 'seccion', 'publicar']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingresa el título de tu blog',
                'maxlength': 255
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe el contenido de tu blog...',
                'rows': 8,
                'cols': 50
            }),

            'publicar': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'titulo': 'Título',
            'descripcion': 'Contenido',
            'publicar': 'Publicar inmediatamente'
        }
        help_texts = {
            'titulo': 'Máximo 255 caracteres',
            'descripcion': 'Contenido principal del blog',
            'publicar': 'Marca esta opción para hacer el blog visible al público'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ya no necesitamos definir choices aquí porque 
        # el campo seccion ya está definido arriba

    def clean_titulo(self):
        titulo = self.cleaned_data['titulo']
        if len(titulo.strip()) < 5:
            raise forms.ValidationError("El título debe tener al menos 5 caracteres.")
        return titulo.strip()

    def clean_descripcion(self):
        descripcion = self.cleaned_data['descripcion']
        if len(descripcion.strip()) < 10:
            raise forms.ValidationError("El contenido debe tener al menos 10 caracteres.")
        return descripcion.strip()


class ImagenForm(forms.ModelForm):
    class Meta:
        model = Imagen
        fields = ['imagen']
        widgets = {
            'imagen': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'id': 'imagen-upload'
            })
        }
        labels = {
            'imagen': 'Seleccionar imagen'
        }
        help_texts = {
            'imagen': 'Formatos soportados: JPG, PNG, GIF. Máximo 5MB'
        }

    def clean_imagen(self):
        imagen = self.cleaned_data['imagen']
        if imagen:
            # Validar tamaño (5MB máximo)
            if imagen.size > 5 * 1024 * 1024:
                raise forms.ValidationError("La imagen no puede ser mayor a 5MB.")
            
            # Validar formato
            if not imagen.name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                raise forms.ValidationError("Solo se permiten archivos JPG, PNG y GIF.")
        
        return imagen


class BusquedaBlogForm(forms.Form):
    """Formulario para buscar y filtrar blogs"""
    busqueda = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar blogs...',
            'id': 'busqueda-input'
        })
    )
    
    seccion = forms.ChoiceField(
        choices=[('', 'Todas las secciones')] + [
            ('blog1', 'Diseño Empresarial'),
            ('blog2', 'Diseño Personal')
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    publicado = forms.ChoiceField(
        choices=[
            ('', 'Todos'),
            ('1', 'Publicados'),
            ('0', 'Borradores')
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )