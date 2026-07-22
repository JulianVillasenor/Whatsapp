import requests 
import json

def SendMessageWhatsapp(data):
    try:
        token = "EAAeX9malBk0BSPZAxcOasSosZAID6JzhMav3gcZC1ZApybTEPhZBAUI2jIZAaOp7C3WVOVJFLEyZCCCQdyh9dntqN1ZBiHcHR2YKIHIpjKTi1eoTytZC1Sd0e83PmWEZBqEK4wSfGEBZAl6ZCf2idhZBZAcm3VTi3DEjZBwfcjlH2ASvuAkTmZBpRECBcEPZBEoC5ZCa5dklR0yDCSaLgGZBOjFBiU4lhTnyRyyLo6RJiuc1ZAAVXLVEHf4a6IlecEZB8ALOdwyfLFIzq2QjCFA01yK8uXr1ToiR0K9th"
        api_url = "https://graph.facebook.com/v25.0/1135356866337944/messages"
        
        headers = {"Content-Type": "application/json", "Authorization": "Bearer " + token}
        response = requests.post(api_url, data = json.dumps(data), headers=headers)

        if response.status_code == 200:
            return True
        return False
    except Exception as exception:
        print("Error: ", exception)
        return False