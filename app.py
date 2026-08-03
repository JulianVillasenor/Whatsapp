from flask import Flask, request, render_template, jsonify
import sheets_service
import util
import whatsappservice

app = Flask(__name__)
@app.route("/", methods=["GET"])
def home():
    return {
        "status": "ok",
        "service": "Viga Constructores WhatsApp Chatbot",
        "endpoints": [
            "/welcome",
            "/whatsapp",
            "/test-whatsapp"
        ]
    }, 200
@app.route('/welcome', methods=['GET'])
def index():
    return render_template('welcome.html')

@app.route('/whatsapp', methods=['GET'])
def VerifyToken():
    try:
        accessToken = "78"
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if token != None and challenge != None and token == accessToken:
            return challenge
        else:
            return "", 400
    except:
        return "", 400
            

@app.route('/whatsapp', methods=['POST'])
def RecivedMessage():
    try:
        body = request.get_json()
        entry = (body['entry'])[0]
        changes = (entry['changes'])[0]
        value = changes['value']
        message = (value['messages'])[0]
        number = message['from']

        text = util.GetTextUser(message)
        texto = text.lower().strip()
        if es_saludo(texto):
            try:
                sheets_service.sicnronizar_planos()
            except Exception as e:
                print("Error al sincronizar planos:", e, flush=True)
        proyectos = sheets_service.get_proyectos()
        GenerateMessage(text, number, proyectos)
        print(text)

        return "EVENT_RECEIVED"
    except:
        return "EVENT_RECEIVED"

@app.route("/test-whatsapp", methods=["GET"])
def test_whatsapp():
    try:
        number = "526622056174"

        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": "Hola Julián 👋 Esta es una prueba desde Render.",
            },
        }

        result = whatsappservice.SendMessageWhatsapp(data)

        return {
            "ok": result
        }, 200 if result else 500

    except Exception as error:
        print("Error en /test-whatsapp:", error)

        return {
            "ok": False,
            "error": str(error),
        }, 500

proyectos = sheets_service.get_proyectos()
#--------------saludos--------------
def es_saludo(texto):
    saludos = {
        "hola",
        "buenas",
        "buenos días",
        "buen día",
        "buenas tardes",
        "buenas noches",
        "qué tal",
        "que tal",
        "hey",
        "hi",
    }

    return texto in saludos
def responder_saludo(number, proyectos):
    lista_proyectos = "\n".join(
        f"• {nombre}"
        for nombre in proyectos
    )

    mensaje = (
        "👋 ¡Hola! Soy el asistente de Viga Constructores.\n\n"
        "Puedo ayudarte a localizar planos de nuestros proyectos.\n\n"
        "Proyectos disponibles:\n"
        f"{lista_proyectos}\n\n"
        "Escribe, por ejemplo:\n"
        "• Plano eléctrico de MONTAÑO\n"
        "• Plano arquitectónico de ZIGA\n"
        "• Plano de aire acondicionado de TAPIAS"
    )

    data = util.TextMessage(mensaje, number)
    return whatsappservice.SendMessageWhatsapp(data)
# ------------ayuda------------
def es_ayuda(texto):
    return texto in {
        "ayuda",
        "menu",
        "menú",
        "opciones",
        "qué puedes hacer",
        "que puedes hacer",
    }
def responder_ayuda(number, proyectos):
    return responder_saludo(number, proyectos)
#-----------despedida--------------
def es_despedida(texto):
    return texto in {
        "gracias",
        "adiós",
        "adios",
        "hasta luego",
        "bye",
    }
def responder_despedida(number):
    mensaje = (
        "Con gusto. 👋\n"
        "Cuando necesites otro plano, escríbeme el proyecto "
        "y el tipo de plano."
    )

    data = util.TextMessage(mensaje, number)
    return whatsappservice.SendMessageWhatsapp(data)
# ----------- detección de proyecto -----------

def detectar_proyecto(texto, proyectos):
    for nombre_visible, codigo_interno in proyectos.items():
        if nombre_visible.lower() in texto:
            return codigo_interno

    return None


def responder_proyecto_no_identificado(number, proyectos):
    lista_proyectos = "\n".join(
        f"• {nombre}"
        for nombre in proyectos
    )

    mensaje = (
        "No pude identificar el proyecto.\n\n"
        "Los proyectos disponibles son:\n"
        f"{lista_proyectos}\n\n"
        "Escribe el nombre del proyecto y el tipo de plano."
    )

    data = util.TextMessage(mensaje, number)
    return whatsappservice.SendMessageWhatsapp(data)
# ----------- detección del tipo de plano -----------

def detectar_tipo_plano(texto):
    if (
        "eléctrico" in texto
        or "electrico" in texto
        or texto.strip() == "ie"
    ):
        return "IE"

    if (
        "arquitectónico" in texto
        or "arquitectonico" in texto
    ):
        return "A"

    if (
        "aire acondicionado" in texto
        or "acondicionado" in texto
    ):
        return "AA"

    return None


def responder_tipo_no_identificado(number):
    mensaje = (
        "No pude identificar el tipo de plano.\n\n"
        "Por ahora puedes solicitar, por ejemplo:\n"
        "• Plano arquitectónico\n"
        "• Plano eléctrico\n"
        "• Plano de aire acondicionado"
    )

    data = util.TextMessage(mensaje, number)
    return whatsappservice.SendMessageWhatsapp(data)
#-----------planos-------------
def responder_consulta_plano(texto, number, proyectos):
    proyecto = detectar_proyecto(texto, proyectos)

    if proyecto is None:
        return responder_proyecto_no_identificado(
            number,
            proyectos,
        )

    tipo = detectar_tipo_plano(texto)

    if tipo is None:
        return responder_tipo_no_identificado(number)

    plano = sheets_service.buscar_plano(
        proyecto,
        tipo,
    )

    if plano is None:
        mensaje = (
            f"No encontré el plano {tipo} "
            f"del proyecto {proyecto}."
        )
    else:
        mensaje = (
            f"Proyecto: {plano['ProyectoCodigo']}\n"
            f"Plano: {plano['TipoPlano']}\n"
            f"Archivo: {plano['NombreArchivo']}\n\n"
            f"{plano['DriveUrl']}"
        )

    data = util.TextMessage(mensaje, number)
    return whatsappservice.SendMessageWhatsapp(data)


def GenerateMessage(text, number, proyectos):
    texto = text.lower().strip()

    if es_saludo(texto):
        return responder_saludo(number, proyectos)

    if es_ayuda(texto):
        return responder_ayuda(number, proyectos)

    if es_despedida(texto):
        return responder_despedida(number)

    return responder_consulta_plano(
        texto,
        number,
        proyectos,
    )


if(__name__ == '__main__'):
    app.run()