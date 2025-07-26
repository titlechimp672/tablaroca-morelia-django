import os

def listar_contenido(ruta, prefijo=""):
    try:
        elementos = os.listdir(ruta)
    except PermissionError:
        print(f"{prefijo}[Acceso denegado]: {ruta}")
        return

    for i, elemento in enumerate(elementos):
        path_completo = os.path.join(ruta, elemento)
        es_ultimo = i == len(elementos) - 1
        conector = "└── " if es_ultimo else "├── "
        print(prefijo + conector + elemento)

        if os.path.isdir(path_completo):
            nuevo_prefijo = prefijo + ("    " if es_ultimo else "│   ")
            listar_contenido(path_completo, nuevo_prefijo)

# Ruta raíz a explorar
ruta_raiz = r"G:\Mi unidad\Trabajo\Servicios WEB\proyecto_blogs"  # Cámbiala por la que desees
listar_contenido(ruta_raiz)
