import requests 
import json

def SendMessageWhatsapp(data):
    try:
        token = "EAAeX9malBk0BSD6MZBMoaRAxaLpSePJOQ75ZC94Tka6PXu5vGvQaXVGR0icyjBZBeCOWGiz431kYHZCSXShrZA2EZCGfHrHV3sh0BdfGut6w7QbRRtXUXTrMuROroqZANsV87wtGacz8njnFPsyau5iRHmRiCJmxZAcGaDZC7uOn4lFDZA1PIxoG7ByhwyCvseex5MyAZDZD"
        api_url = "https://graph.facebook.com/v25.0/1301991842988706/messages"
        headers = {"Content-Type": "application/json", "Authorization": "Bearer " + token}
        response = requests.post(api_url, data = json.dumps(data), headers=headers)
        if response.status_code == 200:
            return True
        return False
    except Exception as exception:
        print("Error: ", exception)
        return False