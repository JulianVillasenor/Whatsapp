def GetTextUser(message):
    text = ""
    typeMessage = message['type']

    if typeMessage == "text":
        text = message['text']['body']
    elif typeMessage == "interactive":
        interactiveObject = message['interactive']
        typeInteractive = interactiveObject["type"]
        if typeInteractive == "button_reply":
            text = (interactiveObject["button_reply"])["title"]
        elif typeInteractive == "list_reply":
            text = (interactiveObject["list_reply"])["title"]
        else:
            print("Sin mensaje")
    else:
        print  ("Sin mensaje")
    return text

def TextMessage(text, number):
    data = {
        "messaging_product": "whatsapp",
        "to": number,
        "type": "text",
        "text": {
            "body": text
        }
    }
    return data

def TextFormatMessage(number):
    data = {
        "messaging_product": "whatsapp",
        "to": number,
        "type": "text",
        "text": {
            "body": "This is a formatted message."
        }
    }
    return data

def ImageMessage(number):
    data = {
        "messaging_product": "whatsapp",
        "to": number,
        "type": "image",
        "image": {
            "link": "https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885_1280.jpg"
        }
    }
    return data

def AudioMessage(number):
    data = {
        "messaging_product": "whatsapp",
        "to": number,
        "type": "audio",
        "audio": {
            "link": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
        }
    }
    return data

def DocumentMessage(number):
    data = {
        "messaging_product": "whatsapp",
        "to": number,
        "type": "document",
        "document": {
            "link": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
        }
    }
    return data

def VideoMessage(number):
    data = {
        "messaging_product": "whatsapp",
        "to": number,
        "type": "video",
        "video": {
            "link": "https://html5videoformatconverter.com/data/images/happyfit2.mp4"
        }
    }
    return data

def LocationMessage(number):
    data = {
    "messaging_product": "whatsapp",
    "to": number,
    "type": "location",
    "location": {
        "latitude": "35.30953768280127",
        "longitude": "139.5423362982525",
        "name": "Playa de Yuigahama",
        "address": "4 Chome Yuigahama, Kamakura, Prefectura de Kanagawa 248-0014, Japón"
    }
}
    return data

def ButtonsMessage(number):
    data = {
        "messaging_product": "whatsapp",
        "to": number,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {
                "text": "¿Desea continuar? 😊"
            },
            "action": {
                "buttons": [
                    {
                        "type": "reply",
                        "reply": {
                            "id": "001",
                            "title": "Sí"
                        }
                    },
                    {
                        "type": "reply",
                        "reply": {
                            "id": "002",
                            "title": "No"
                        }
                    }
                ]
            }
        }
    }
    return data

def ListMessage(number):
    data = {
        "messaging_product": "whatsapp",
        "to": number,
        "type": "interactive",
        "interactive": {
            "type": "list",
            "header": {
                "type": "text",
                "text": "Encabezado de la lista"
            },
            "body": {
                "text": "Cuerpo de la lista"
            },
            "footer": {
                "text": "Pie de página de la lista"
            },
            "action": {
                "button": "Ver opciones",
                "sections": [
                    {
                        "title": "Sección 1",
                        "rows": [
                            {
                                "id": "option1",
                                "title": "Opción 1",
                                "description": "Descripción de la opción 1"
                            },
                            {
                                "id": "option2",
                                "title": "Opción 2",
                                "description": "Descripción de la opción 2"
                            }
                        ]
                    },
                    {
                        "title": "Sección 2",
                        "rows": [
                            {
                                "id": "option3",
                                "title": "Opción 3",
                                "description": "Descripción de la opción 3"
                            },
                            {
                                "id": "option4",
                                "title": "Opción 4",
                                "description": "Descripción de la opción 4"
                            }
                        ]
                    }
                ]
            }
        }
    }
    return data