import requests 
import json

def SendMessageWhatsapp(data):
    try:
        token = "EAARZA8QCCYmMBR5pRw69uf8OeAuxb85SvUuQ0JzXwUzmmVWZCZA0AqzwOyZBS5i30KWencWyyo2Jzj2qpBnE7Hh1WcWeUgkBVuy4RCfCN691uhZBqBLoj3vj02QMXWWdRUZB9ZBuxKKHBLkBEa6L4GZCYEwsIFZCcDTO0mZAwdI3HBZCGpjrOufPXfPifTh4kb0NeHUR3Fnjnv65ZCJbNKX4DF5lzpZApZCIApwvSw6e8Dsnf9k3DAEFds9EFht7cSMpt7uTZAtZB7VEPak1I79qpeNGifZAgrSsZD"
        api_url = "https://graph.facebook.com/v25.0/1217536118101270/messages"
        
        headers = {"Content-Type": "application/json", "Authorization": "Bearer " + token}
        response = requests.post(api_url, data = json.dumps(data), headers=headers)

        if response.status_code == 200:
            return True
        return False
    except Exception as exception:
        print("Error: ", exception)
        return False