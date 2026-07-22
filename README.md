# WhatsApp Chatbot - Viga Constructores

Chatbot desarrollado con Flask y la WhatsApp Cloud API de Meta para automatizar la atención a clientes de Viga Constructores.

## Características

- Verificación del Webhook de Meta
- Recepción de mensajes de WhatsApp
- Envío automático de respuestas
- Integración con WhatsApp Cloud API
- Desplegado en Render
- Arquitectura preparada para integrar ChatGPT y Google Drive

---

# Tecnologías

- Python 3.13
- Flask
- Requests
- Gunicorn
- WhatsApp Cloud API
- Render

---

# Requisitos

- Python 3.13+
- Git
- Cuenta de Meta Developers
- Cuenta de WhatsApp Business
- Cuenta de Render

---

# Instalación

Clonar el proyecto

```bash
git clone https://github.com/JulianVillasenor/Whatsapp.git
cd Whatsapp
```

Crear entorno virtual

Windows

```powershell
python -m venv .venv
```

Activar entorno

PowerShell

```powershell
Set-ExecutionPolicy RemoteSigned -Scope Process
.\.venv\Scripts\Activate.ps1
```

Instalar dependencias

```powershell
pip install -r requirements.txt
```

---

# Ejecutar localmente

```powershell
python app.py
```

Servidor disponible en

```
http://127.0.0.1:5000
```

---

# Endpoints

## GET /welcome

Prueba del servidor.

Respuesta

```
welcome developer
```

---

## GET /whatsapp

Utilizado por Meta para verificar el Webhook.

Parámetros

```
hub.verify_token
hub.challenge
```

---

## POST /whatsapp

Recibe mensajes enviados por WhatsApp Cloud API.

---

# Despliegue en Render

Build Command

```text
pip install -r requirements.txt
```

Start Command

```text
gunicorn app:app
```

---

# Variables de entorno

```
WHATSAPP_TOKEN

PHONE_NUMBER_ID

VERIFY_TOKEN
```

---

# Flujo del chatbot

Cliente

↓

WhatsApp

↓

Meta Cloud API

↓

Render

↓

Flask

↓

Procesamiento del mensaje

↓

Respuesta al cliente

---

# Estado del proyecto

- ✔ Webhook funcionando
- ✔ Recepción de mensajes
- ✔ Envío de mensajes
- ✔ Deploy en Render
- 🔄 Chatbot en desarrollo
- 🔄 Integración con Google Drive
- 🔄 Solicitud automática de planos

---

# Autor

Julian Villaseñor