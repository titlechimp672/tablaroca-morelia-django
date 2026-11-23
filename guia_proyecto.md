# GUÍA COMPLETA - PROYECTO TABLAROCA MORELIA DJANGO

## INFORMACIÓN DEL PROYECTO

**Nombre:** Soluciones Tablaroca Morelia  
**Tecnología:** Django 5.2 + Bootstrap + Google Maps  
**Servidor:** DigitalOcean, Ubuntu 24.04 LTS, nginx + gunicorn + PostgreSQL 17  
**Repositorio:** https://github.com/titlechimp672/tablaroca-morelia-django (rama `main`)  
**Dominio:** https://solucionestablarocamorelia.com (DNS en Hostinger)  

---

## FLUJO DE TRABAJO (REGLA DE ORO)

### SIEMPRE TRABAJAR LOCAL → GITHUB → SERVIDOR

```
Local (WSL) → GitHub → Servidor
```

**NUNCA editar directamente en el servidor.** Si se edita ahí, el siguiente
`update_site.sh` se detiene porque `git pull` no puede sobrescribir el cambio.

---

## COMANDOS LOCALES (Tu máquina)

Copia de trabajo:
`OneDrive/Trabajo/Servicios WEB/alejandro_soluciones_tablaroca_morelia/tablaroca-morelia-django`

Usar la terminal de **WSL**: ahí está la llave SSH registrada en GitHub
(usuario `titlechimp672`), así que `git push` no pide contraseña.

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
ssh root@142.93.113.94
# o, desde WSL, con el alias configurado en ~/.ssh/config:
ssh nuevo
```

### Actualizar el sitio desde GitHub:
```bash
bash /home/update_site.sh
# o sin entrar al servidor:
ssh nuevo 'bash /home/update_site.sh'
```

El script hace, en orden: `git pull --ff-only`, instala paquetes si cambió
`requirements.txt`, aplica migraciones, `collectstatic`, reinicia el sitio y
comprueba que responda. Si algo falla, se detiene y muestra el error.

### Verificar estado del servicio:
```bash
systemctl status tablaroca.service
```

### Ver logs en tiempo real:
```bash
journalctl -u tablaroca.service -f
```

### Comandos de Django en el servidor:
El sitio corre con el usuario `tablaroca` (no root). Ejecutar `manage.py`
siempre como ese usuario, para no dejar archivos con dueño equivocado:
```bash
cd /home/tablaroca-morelia-django
sudo -u tablaroca venv/bin/python manage.py check
sudo -u tablaroca venv/bin/python manage.py createsuperuser
sudo -u tablaroca venv/bin/python manage.py shell
```

---

## ESTRUCTURA DEL PROYECTO

```
/home/tablaroca-morelia-django/
├── proyecto_blogs/          # Configuración principal Django
│   ├── settings.py          # Configuraciones (lee .env)
│   ├── urls.py              # URLs principales: admin/, usuarios/, blogs/
│   └── wsgi.py              # WSGI para gunicorn
├── blogs/                   # App de blogs: modelos Blog e Imagen, panel de edición
├── usuarios/                # Login / logout
├── templates/
│   ├── base.html
│   ├── alejandro_blog1.html # Página principal pública
│   └── alejandro_blog2.html
├── static/                  # CSS, JS, imágenes del diseño (en git)
├── collected_static/        # Generado por collectstatic (no en git)
├── media/                   # Imágenes subidas desde el panel (no en git)
├── requirements.txt         # Versiones exactas de paquetes
├── .env                     # Secretos (no en git)
├── venv/                    # Entorno virtual (no en git)
└── manage.py
```

### URLs principales:
- `/` → redirige (en nginx) a `/blogs/alejandro/blog1/`
- `/blogs/<usuario>/<seccion>/` → vista pública
- `/blogs/` → panel para crear, editar y publicar blogs (requiere login)
- `/usuarios/login/` → inicio de sesión
- `/admin/` → administrador de Django

---

## CONFIGURACIONES IMPORTANTES

### Variables de entorno (.env, sólo en el servidor):
```
SECRET_KEY=...            # 64 caracteres aleatorios; NO subir a git
DEBUG=False
ALLOWED_HOSTS=solucionestablarocamorelia.com,www.solucionestablarocamorelia.com
DB_NAME=tablaroca_db
DB_USER=...
DB_PASSWORD=...
DB_HOST=localhost
DB_PORT=5432
# Opcional: duración de HSTS en segundos (por omisión 3600)
# SECURE_HSTS_SECONDS=31536000
```

Con `DEBUG=False` se usa PostgreSQL y se activan: redirección a HTTPS,
cookies sólo por HTTPS, `CSRF_TRUSTED_ORIGINS` y HSTS (ver final de
`settings.py`). Con `DEBUG=True` (desarrollo local) se usa SQLite.

### Servicios del servidor:
- **nginx:** servidor web, puertos 80/443 (públicos)
- **gunicorn:** Django en 127.0.0.1:8001 (interno), 2 workers
- **tablaroca.service:** servicio systemd, corre como usuario `tablaroca`
- **postgresql:** base `tablaroca_db`
- **certbot.timer:** renueva solo el certificado HTTPS (Let's Encrypt)
- **unattended-upgrades:** instala solo los parches de seguridad

### Firewall (ufw):
Sólo abiertos: 22 (SSH), 80 (HTTP) y 443 (HTTPS).

### Archivos de configuración:
```bash
/etc/nginx/sites-available/solucionestablarocamorelia   # nginx del sitio
/etc/systemd/system/tablaroca.service                   # servicio gunicorn
/home/update_site.sh                                    # script de actualización
/home/tablaroca-morelia-django/.env                     # secretos
```

---

## SOLUCIÓN DE PROBLEMAS COMUNES

### Error 400 - Bad Request:
1. Verificar ALLOWED_HOSTS en .env
2. Agregar el dominio a ALLOWED_HOSTS
3. `systemctl restart tablaroca.service`

### Error 403 al enviar un formulario (CSRF):
Revisar que el dominio esté en ALLOWED_HOSTS (de ahí se arma
CSRF_TRUSTED_ORIGINS) y que se entre por https.

### Error 500 - Internal Server Error:
```bash
journalctl -u tablaroca.service --lines=50
```

### Error 502 - Bad Gateway (gunicorn no arranca):
```bash
systemctl status tablaroca.service
journalctl -u tablaroca.service --lines=50
# Probar Django directo:
curl -H "Host: solucionestablarocamorelia.com" http://127.0.0.1:8001/blogs/alejandro/blog1/
```

### Archivos estáticos no cargan:
```bash
cd /home/tablaroca-morelia-django
sudo -u tablaroca venv/bin/python manage.py collectstatic --noinput
systemctl restart tablaroca.service
```

### update_site.sh dice que git pull no puede continuar:
Alguien editó un archivo directamente en el servidor. Ver qué cambió:
```bash
cd /home/tablaroca-morelia-django
sudo -u tablaroca git status
sudo -u tablaroca git diff
```
Si el cambio sirve, pasarlo a la copia local y subirlo a GitHub. Luego, en
el servidor, descartarlo y volver a actualizar:
```bash
sudo -u tablaroca git checkout -- <archivo>
bash /home/update_site.sh
```

---

## COMANDOS ÚTILES

### Logs importantes:
```bash
journalctl -u tablaroca.service -f        # Django / gunicorn
tail -f /var/log/nginx/error.log          # nginx: errores
tail -f /var/log/nginx/access.log         # nginx: visitas
```

### Reiniciar servicios:
```bash
systemctl restart tablaroca.service
systemctl reload nginx        # tras cambiar su configuración (probar antes con: nginx -t)
```

### Certificado HTTPS:
```bash
certbot certificates          # ver vencimiento
certbot renew --dry-run       # simular renovación
```

---

## RESPALDOS

No hay respaldos automáticos. Respaldo manual más reciente:
`OneDrive/Trabajo/Servicios WEB/alejandro_soluciones_tablaroca_morelia/respaldo_2026-11-23`
(su `LEEME.md` explica cómo restaurar en un servidor nuevo).

Respaldo rápido de la base de datos:
```bash
sudo -u postgres pg_dump -Fc tablaroca_db > /root/tablaroca_db_$(date +%F).dump
```

---

## CARACTERÍSTICAS DEL SITIO

### Funcionalidades:
- Sitio web de una página (landing page)
- Secciones: Inicio, Acerca, Servicios, Trabajos, Contacto
- Blog dinámico con imágenes, editable desde /blogs/
- Testimonios en carrusel
- Mapa interactivo de Google Maps
- Integración con WhatsApp
- Diseño responsivo (móvil/tablet/desktop)

### Tecnologías:
- **Backend:** Django 5.2, Python 3.12
- **Frontend:** Bootstrap 3, jQuery, Owl Carousel
- **Servidor:** nginx + gunicorn
- **Base de datos:** PostgreSQL 17 (producción), SQLite (desarrollo con DEBUG=True)

---

## CONTACTO Y DATOS

### Información del negocio:
- **Teléfono:** +52 443 486 1244
- **Ubicación:** Morelia, Michoacán
- **WhatsApp:** https://wa.me/524434861244
- **Google Maps:** https://maps.app.goo.gl/4JgKtiCNwq63nmGj8

### Datos técnicos:
- **Droplet:** `tablaroca-alejandro` (DigitalOcean)
- **IP Servidor:** 142.93.113.94
- **Usuario SSH:** root (sólo con llave SSH, sin contraseña)
- **Usuario del sitio:** tablaroca
- **Directorio proyecto:** /home/tablaroca-morelia-django/
- **DNS:** Hostinger. Registro `A @` → 142.93.113.94; `www` es CNAME a `@`

---

## EN CASO DE EMERGENCIA

### Si el sitio está caído:
1. **Verificar servicios:**
   ```bash
   systemctl status tablaroca.service nginx postgresql
   ```

2. **Reiniciar todo:**
   ```bash
   systemctl restart tablaroca.service
   systemctl restart nginx
   ```

3. **Ver qué falló:**
   ```bash
   journalctl -u tablaroca.service --lines=50
   ```

### Si un cambio subido rompió el sitio:
Revertirlo en la copia local y volver a subirlo (así GitHub y el servidor
quedan iguales):
```bash
# LOCAL
git revert <commit_con_el_error>
git push
# SERVIDOR
bash /home/update_site.sh
```

---

## NOTAS ADICIONALES

### Buenas prácticas:
- Siempre hacer respaldo antes de cambios grandes
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

## COMANDOS RÁPIDOS DE REFERENCIA

```bash
# LOCAL (WSL): subir cambios
git add . && git commit -m "mensaje" && git push

# Actualizar el servidor
ssh nuevo 'bash /home/update_site.sh'

# Ver logs
ssh nuevo 'journalctl -u tablaroca.service -f'

# Estado de servicios
ssh nuevo 'systemctl status tablaroca.service nginx'
```

---

**Última actualización:** 23 de noviembre de 2026 (mudanza a Ubuntu 24.04, droplet 142.93.113.94)  
**Creado por:** Claude AI (Anthropic)  
