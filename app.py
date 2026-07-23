from flask import Flask, request, render_template
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
            "/whatsapp"
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

def GenerateMessage(text, number):
    if "text" in text:
        data = util.TextMessage("Text", number)
    if "format" in text:
        data = util.TextFormatMessage(number)
    if "image" in text:
        data = util.ImageMessage(number)
    if "audio" in text:
        data = util.AudioMessage(number)
    if "document" in text:
        data = util.DocumentMessage(number)
    if "video" in text:
        data = util.VideoMessage(number)
    if "button" in text:
        data = util.ButtonsMessage(number)
    if "location" in text:
        data = util.LocationMessage(number)
    if "list" in text:
        data = util.ListMessage(number)
    whatsappservice.SendMessageWhatsapp(data)


if(__name__ == '__main__'):
    app.run()