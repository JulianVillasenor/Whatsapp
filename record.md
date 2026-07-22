# Development Record

## 2026-06-26

### Inicio del proyecto

Se creó el repositorio.

---

## 2026-06-29

### Flask

Problema

No se podía leer el mensaje recibido.

Causa

La estructura del JSON era incorrecta.

Antes

```python
entry['entry']
```

Después

```python
entry['changes']
```

Resultado

Se imprimió correctamente:

```
hi user
```

---

## 2026-07-02

### Azure

Problema

Azure no permitía crear la VM.

Error

```
Operation cannot be completed without additional quota.
```

Decisión

Se migró completamente el proyecto a Render.

---

## 2026-07-02

### Render

Estado

✅ Deploy exitoso.

URL

```
https://whatsapp-mw1b.onrender.com
```

---

## 2026-07-02

### Webhook

Meta verificó correctamente el endpoint.

GET

```
/whatsapp
```

Respuesta

```
12345
```

POST

```
this is a text message
```