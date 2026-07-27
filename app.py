from flask import Flask, request, render_template, jsonify

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