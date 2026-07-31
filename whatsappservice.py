import requests 
import json

def SendMessageWhatsapp(data):
    try:
        token = "EAAeX9malBk0BSCQmFmA0ycSZBLZCSPvobOXvXZBJutdQgoyfFcSG5xefrrQ9BvdPEAh2z0ABeNRP2dPdQK8NVRmqOzgfTSLyMKx0eBFESZA1s0WCteKmr0Gkgz9slM5y3hW6ZBKG7yehRtO95AOeHkW1G0tDNYMWLWwcyJl0hmky2ZCJz2GDTpnvX2i0nBeyyWFwZDZD"
        api_url = "https://graph.facebook.com/v25.0/1301991842988706/messages"
        headers = {"Content-Type": "application/json", "Authorization": "Bearer " + token}
        response = requests.post(api_url, data = json.dumps(data), headers=headers)
        if response.status_code == 200:
            return True
        return False
    except Exception as exception:
        print("Error: ", exception)
        return False