import requests 
import json

def SendMessageWhatsapp(data):
    try:
        token = "EAARZA8QCCYmMBR4w3rjxDUNF12K1F1CiEsk0DwRiYZAEWzcgrhxIUio4pQbZBK9HZCVCWsOhTF6cnYLZBZA63pO5eszHZAvMwhTEGcLqyBkW8HFsf7201IujdlJRWWDzXBq1ZBRgowmlEmYBZBOYF4iBtyvsxgNk8qlXtJ1FVhrLsF6rb1M94VIOP0pdIZC6sNNrZCz6sMXn8yfVFTZAZB4lsAzwWk4B3ZC3PTGuM0HrPhDyWz9oq6aNvVsOPTEY2eFe40m1mc3Ok7buJ1Oo0ixtjUNY4aNwZDZD"
        api_url = "https://graph.facebook.com/v25.0/1217536118101270/messages"
        
        headers = {"Content-Type": "application/json", "Authorization": "Bearer " + token}
        response = requests.post(api_url, data = json.dumps(data), headers=headers)

        if response.status_code == 200:
            return True
        return False
    except Exception as exception:
        print("Error: ", exception)
        return False