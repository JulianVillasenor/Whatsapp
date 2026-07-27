import requests 
import json

def SendMessageWhatsapp(data):
    try:
        token = "EAAeX9malBk0BSC4ZCl660dcHDaR5ujNDCEbBWVA6Si9jS5RAxtkpexPicu6MVWX0UQp8IeipDuX5ZAIGZB4l6OCLwTyei4UgAEfGwc6b8pZCFcZCErbbsUfKnzGSrZC3S4kJKRFWYXIZCTLZB3MsLknzexwrw73xNRQo5l1R8WtFMC7RYTxi95lCrcmmKdJL5J5h1cSognYlj3B9fsMv1rT6GRdtbXJGtkAfYGy13fmiCb3piW2EIcq3X0tJJQylq9fLiIQZAEwZAhOcucMQRbm1t3VpXKzAZDZD"
        api_url = "https://graph.facebook.com/v25.0/1135356866337944/messages"
        headers = {"Content-Type": "application/json", "Authorization": "Bearer " + token}
        response = requests.post(api_url, data = json.dumps(data), headers=headers)
        if response.status_code == 200:
            return True
        return False
    except Exception as exception:
        print("Error: ", exception)
        return False