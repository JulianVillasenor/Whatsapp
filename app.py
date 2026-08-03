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
        GenerateMessage(text, number)
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

def GenerateMessage(text, number):
    texto = text.lower()

    if "montaño" in texto or "montano" in texto:
        proyecto = "MONTANO"
    elif "ziga" in texto:
        proyecto = "ZIGA"
    else:
        data = util.TextMessage(
            "No pude identificar el proyecto.",
            number
        )
        return whatsappservice.SendMessageWhatsapp(data)

    if (
        "eléctrico" in texto
        or "electrico" in texto
        or texto.strip() == "ie"
    ):
        tipo = "IE"
    elif "arquitectónico" in texto or "arquitectonico" in texto:
        tipo = "A"
    elif "aire" in texto or "acondicionado" in texto:
        tipo = "AA"
    else:
        data = util.TextMessage(
            "No pude identificar el tipo de plano.",
            number
        )
        return whatsappservice.SendMessageWhatsapp(data)

    plano = sheets_service.buscar_plano(proyecto, tipo)

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


if(__name__ == '__main__'):
    app.run()