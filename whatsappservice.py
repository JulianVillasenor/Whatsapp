import requests 
import json

def SendMessageWhatsapp(data):
    try:
        token = "EAAeX9malBk0BSPPySmYNHgZCr21dWBHZAZCAhdk5kLFqfJj4QOzZBb7Umk1pZCF30cOPW96EBjswbvgR2UOERAlwm3OaZBunKD2xSuPWqrZANdTFLrn6zkQUZBeScpDFWb958T6DVrpaPvPfS4K7uX96r0PkrtTPTuH21ot9HJvwur35RVIfoK6JECimp6ybWTayLXvluoAnUKIiYArZCNcZCVFKx1GZAUFZCL8up6TxylKZCwO0FpuT3uRM6YZC608K0incLUCgaj2gpMmafvht94iSkZAQIAx"
        api_url = "https://graph.facebook.com/v25.0/1135356866337944/messages"
        headers = {"Content-Type": "application/json", "Authorization": "Bearer " + token}
        response = requests.post(api_url, data = json.dumps(data), headers=headers)
        if response.status_code == 200:
            return True
        return False
    except Exception as exception:
        print("Error: ", exception)
        return False