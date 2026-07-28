import requests 
import json

def SendMessageWhatsapp(data):
    try:
        token = "EAAeX9malBk0BSAG15puYj2ZBvdxMQFZCy2Nf1bachVkkAzi0zOQBGuGF4VInbsZBloZCkKWp1fbFqL4rPkavaPFo5sP0BDEoPAZALlkcf0Ne6QlwomNXXWhktQWAz4RZA3xS1IqGDf6igNVFwlM4BWIQfHZCuSDjK6dVdqeZATdZA9Gujjz5MK6YVgOwUBXVWpvkTMW01aNRS83owlkVzw1bMSDzy9JZB2OXZBAcmonw3dlBkvSZClKqvG93akkFfDpIRXZA67W65qSArW0bwWQPWvgoneofrUAZDZD"
        api_url = "https://graph.facebook.com/v25.0/1135356866337944/messages"
        headers = {"Content-Type": "application/json", "Authorization": "Bearer " + token}
        response = requests.post(api_url, data = json.dumps(data), headers=headers)
        if response.status_code == 200:
            return True
        return False
    except Exception as exception:
        print("Error: ", exception)
        return False