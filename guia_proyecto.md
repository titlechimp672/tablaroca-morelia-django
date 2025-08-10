# GUÍA COMPLETA - PROYECTO TABLAROCA MORELIA DJANGO

## INFORMACIÓN DEL PROYECTO

**Nombre:** Soluciones Tablaroca Morelia  
**Tecnología:** Django + Bootstrap + Google Maps  
**Servidor:** Ubuntu con nginx + gunicorn  
**Repositorio:** https://github.com/titlechimp672/tablaroca-morelia-django.git  
**Dominio:** solucionestablarocamorelia.com  

---

## FLUJO DE TRABAJO (REGLA DE ORO)

### SIEMPRE TRABAJAR LOCAL → GITHUB → SERVIDOR

```
Local → Github → Servidor
```

**NUNCA editar directamente en el servidor**

---

## COMANDOS LOCALES (Tu máquina)

### Verificar estado del proyecto:
```bash
git status
```

### Subir cambios a GitHub:
```bash
# Paso a paso
git add .
git commit -m "Descripción de los cambios"
git push origin main

# Comando rápido
git add . && git commit -m "Cambios realizados" && git push
```

### Ver historial:
```bash
git log --oneline
```

---

## COMANDOS DEL SERVIDOR

### Conectarse al servidor:
```bash
ssh root@emellado-server
```

### Actualizar proyecto desde GitHub:
```bash
cd /home/tablaroca-morelia-django
git pull origin main
sudo systemctl restart tablaroca.service
```

### Comando rápido para actualizar:
```bash
git pull && sudo systemctl restart tablaroca.service
```

### Verificar estado del servicio:
```bash
sudo systemctl status tablaroca.service
```

### Ver logs en tiempo real:
```bash
sudo journalctl -u tablaroca.service -f
```

### Trabajar con entorno virtual (si necesario):
```bash
cd /home/tablaroca-morelia-django
source venv/bin/activate
python manage.py check
deactivate  # para salir
```

---

## ESTRUCTURA DEL PROYECTO

```
/home/tablaroca-morelia-django/
├── proyecto_blogs/          # Configuración principal Django
│   ├── settings.py         # Configuraciones
│   ├── urls.py            # URLs principales
│   └── wsgi.py            # WSGI para producción
├── aplicaciones/
│   └── alejandro_blog1/   # App principal del sitio
├── templates/
│   └── alejandro_blog1.html # Template principal
├── static/                # Archivos estáticos (CSS, JS, imágenes)
├── media/                 # Archivos subidos por usuarios
├── .env                   # Variables de configuración
├── manage.py              # Comandos Django
└── README.md              # Este archivo
```

---
### Variables de entorno (.env):
```
ALLOWED_HOSTS=192.241.129.202,solucionestablarocamorelia.com,www.solucionestablarocamorelia.com
SECRET_KEY=tu_clave_secreta
DEBUG=False
```

### Servicios del servidor:
- **nginx:** Servidor web (puerto 80/443)
- **gunicorn:** Servidor Django (puerto 8001)
- **tablaroca.service:** Servicio systemd

### Puertos:
---

## SOLUCIÓN DE PROBLEMAS COMUNES

### Error 400 - Bad Request:
1. Verificar ALLOWED_HOSTS en .env
2. Agregar dominio a ALLOWED_HOSTS
3. Reiniciar servicio

### Error 500 - Internal Server Error:
```bash
# Ver logs detallados
sudo journalctl -u tablaroca.service -f --lines=50
```

### Sitio no carga:
```bash
# Verificar servicios
sudo systemctl status nginx
sudo systemctl status tablaroca.service

# Verificar Django localmente
curl http://127.0.0.1:8001/
```

### Archivos estáticos no cargan:
```bash
cd /home/tablaroca-morelia-django
source venv/bin/activate
python manage.py collectstatic --noinput
sudo systemctl restart tablaroca.service
```

### Conflictos de Git:
```bash
# En el servidor, si hay conflictos
git reset --hard HEAD
git pull origin main
```

---

## COMANDOS ÚTILES

### Ver archivos de configuración:
```bash
# Ver configuración nginx
sudo nano /etc/nginx/sites-available/default

# Ver servicio systemd
sudo nano /etc/systemd/system/tablaroca.service

# Ver variables de entorno
cat /home/tablaroca-morelia-django/.env
```

### Logs importantes:
```bash
# Logs de Django
sudo journalctl -u tablaroca.service -f

# Logs de nginx
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

### Reiniciar servicios:
```bash
sudo systemctl restart tablaroca.service
sudo systemctl restart nginx
sudo systemctl reload nginx  # Solo recargar configuración
```

---

## CARACTERÍSTICAS DEL SITIO

### Funcionalidades:
- Sitio web una página (landing page)
- Secciones: Inicio, Acerca, Servicios, Trabajos, Contacto
- Blog dinámico con imágenes
- Testimonios en carousel
- Mapa interactivo de Google Maps
- Integración con WhatsApp
- Diseño responsivo (móvil/tablet/desktop)

### Tecnologías:
- **Backend:** Django 4.x
- **Frontend:** Bootstrap 3, jQuery, Owl Carousel
- **Servidor:** nginx + gunicorn
- **Base de datos:** SQLite (por defecto)

---

## CONTACTO Y DATOS

### Información del negocio:
- **Teléfono:** +52 443 486 1244
- **Ubicación:** Morelia, Michoacán
- **WhatsApp:** https://wa.me/524434861244
- **Google Maps:** https://maps.app.goo.gl/4JgKtiCNwq63nmGj8

### Datos técnicos:
- **IP Servidor:** 192.241.129.202
- **Usuario SSH:** root
- **Directorio proyecto:** /home/tablaroca-morelia-django/

---

## EN CASO DE EMERGENCIA

### Si el sitio está caído:
1. **Verificar servicios:**
   ```bash
   sudo systemctl status tablaroca.service
   sudo systemctl status nginx
   ```

2. **Reiniciar todo:**
   ```bash
   sudo systemctl restart tablaroca.service
   sudo systemctl restart nginx
   ```

3. **Ver qué falló:**
   ```bash
   sudo journalctl -u tablaroca.service --lines=50
   ```

### Si hay cambios perdidos:
1. **Ver historial en GitHub**
2. **Hacer rollback si necesario:**
   ```bash
   git reset --hard commit_anterior
   sudo systemctl restart tablaroca.service
   ```

---

## NOTAS ADICIONALES

### Buenas prácticas:
- Siempre hacer backup antes de cambios grandes
- Probar cambios en local antes de subir
- Usar mensajes descriptivos en commits
- Documentar cambios importantes
- No editar archivos directamente en el servidor

### Mensajes de commit recomendados:
```
"Actualizar diseño de la sección servicios"
"Corregir error en el formulario de contacto"
"Agregar nuevas imágenes al portfolio"
"Optimizar velocidad de carga"
```

---

**Última actualización:** Agosto 2025  
**Creado por:** Claude AI (Anthropic)  
**Mantenido por:** Equipo de desarrollo  

---

## COMANDOS RÁPIDOS DE REFERENCIA

```bash
# LOCAL: Subir cambios
git add . && git commit -m "mensaje" && git push

# SERVIDOR: Actualizar
git pull && sudo systemctl restart tablaroca.service

# VER LOGS
sudo journalctl -u tablaroca.service -f

# ESTADO DE SERVICIOS
sudo systemctl status tablaroca.service nginx
```- **80/443:** nginx (público)
- **8001:** gunicorn (interno)


## CONFIGURACIONES IMPORTANTES


