# Deploy en Render

Esta guía describe cómo ejecutar el proyecto en un entorno Linux y desplegarlo en Render.

---

# ¿Por qué Linux?

El proyecto utiliza **Gunicorn** como servidor WSGI para producción.

Gunicorn depende del módulo:

```python
fcntl
```

Este módulo únicamente está disponible en sistemas Linux/Unix.

Por este motivo el siguiente comando **NO funciona en Windows**:

```powershell
gunicorn app:app
```

Error:

```text
ModuleNotFoundError: No module named 'fcntl'
```

Esto es un comportamiento esperado y no un problema del proyecto.

---

# Desarrollo local

## Windows

Crear el entorno virtual

```powershell
python -m venv .venv
```

Activar

```powershell
.\.venv\Scripts\Activate.ps1
```

Instalar dependencias

```powershell
pip install -r requirements.txt
```

Ejecutar

```powershell
python app.py
```

La aplicación estará disponible en

```
http://127.0.0.1:5000
```

---

# Prueba en Linux (WSL)

Para probar exactamente el mismo entorno que utiliza Render se recomienda utilizar WSL2.

Abrir Ubuntu

```powershell
Ubuntu
```

Ir al proyecto

```bash
cd /mnt/b/whatsapp
```

Actualizar paquetes

```bash
apt update
```

Instalar soporte para entornos virtuales

```bash
apt install python3.12-venv
```

Crear entorno virtual

```bash
python3 -m venv .venv-linux
```

Activar

```bash
source .venv-linux/bin/activate
```

Actualizar pip

```bash
python -m pip install --upgrade pip
```

Instalar dependencias

```bash
pip install -r requirements.txt
```

Ejecutar Gunicorn

```bash
gunicorn app:app
```

La aplicación quedará disponible en

```
http://127.0.0.1:8000
```

---

# Despliegue en Render
https://whatsapp-mw1b.onrender.com
## Build Command

```text
pip install -r requirements.txt
```

## Start Command

```text
gunicorn app:app
```

---

# Variables de entorno

Agregar las siguientes variables en Render.

```
VERIFY_TOKEN

ACCESS_TOKEN

PHONE_NUMBER_ID
```

(Agregar aquí las variables reales utilizadas por el proyecto.)

---

# Flujo del despliegue

GitHub

↓

Render

↓

Gunicorn

↓

Flask

↓

WhatsApp Cloud API

↓

Cliente

---

# Notas

- Windows se utiliza únicamente para desarrollo.
- Linux (WSL) permite probar el mismo entorno que utilizará Render.
- Render ejecuta Ubuntu Linux, por lo que Gunicorn funciona sin modificaciones.
- No reutilizar el entorno virtual de Windows dentro de WSL. Cada sistema operativo debe tener su propio entorno virtual.