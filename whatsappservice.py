import requests 
import json

def SendMessageWhatsapp(data):
    try:
        token = "EAAeX9malBk0BSOZAhZCQ8jQ7oW5uNgbYnQZBdNmJgkR93x9WxFqwxHIkZA6avj9Nn7xJ28ZBRW7FPysrIQRbtO4aPWRWHZB1gvzZAd3caD1NL40vQP0qT6PoibFPugztgSV3J5Jc8uMfQnu1BTT6Uo6f6HleZCGz6JS6S2pUDWZCZBImDR9JgZC8YbGL0F2pN0iuUhhEjCOa8bsZBtQ0DTZCmyWxbgzpbz7KKOD4hUtgmsxkfWOna0DqINZAP6822eP7PhNA0Mw4yUZBwdjSybBg6W1rFNLR6LV"
        api_url = "https://graph.facebook.com/v25.0/1135356866337944/messages"
        headers = {"Content-Type": "application/json", "Authorization": "Bearer " + token}
        response = requests.post(api_url, data = json.dumps(data), headers=headers)
        if response.status_code == 200:
            return True
        return False
    except Exception as exception:
        print("Error: ", exception)
        return False