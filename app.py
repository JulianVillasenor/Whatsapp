from flask import Flask, request, render_template, jsonify
import os
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
        number = os.getenv("WHATSAPP_TEST_RECIPIENT")

        if not number:
            return jsonify({
                "ok": False,
                "error": (
                    "No existe la variable de entorno "
                    "WHATSAPP_TEST_RECIPIENT."
                ),
            }), 500

        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": (
                    "✅ Mensaje enviado desde Render.\n\n"
                    "El chatbot de Viga Constructores "
                    "ya puede comunicarse con WhatsApp."
                ),
            },
        }

        response = whatsappservice.SendMessageWhatsapp(data)

        return jsonify({
            "ok": True,
            "message": "Solicitud enviada a WhatsApp.",
            "meta_response": response,
        }), 200

    except Exception as error:
        print(f"Error en /test-whatsapp: {error}")

        return jsonify({
            "ok": False,
            "error": str(error),
        }), 500

def GenerateMessage(text, number):
    if "text" in text:
        data = util.TextMessage("Text", number)
    elif "format" in text:
        data = util.TextFormatMessage(number)
    elif "image" in text:
        data = util.ImageMessage(number)
    elif "audio" in text:
        data = util.AudioMessage(number)
    elif "document" in text:
        data = util.DocumentMessage(number)
    elif "video" in text:
        data = util.VideoMessage(number)
    elif "button" in text:
        data = util.ButtonsMessage(number)
    elif "location" in text:
        data = util.LocationMessage(number)
    elif "list" in text:
        data = util.ListMessage(number)
    else:
        data = util.TextMessage("No entendi el mensaje", number)
    whatsappservice.SendMessageWhatsapp(data)


if(__name__ == '__main__'):
    app.run()