import requests
import json

def get_access_token(client_id, client_secret):
    auth_url = 'https://login.uber.com/oauth/v2/token'
    grant_type = 'client_credentials'
    scope = 'eats.deliveries direct.organizations'
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': grant_type,
        'scope': scope
    }
    response = requests.post(auth_url, data=payload)
    token_info = response.json()
    if response.status_code == 200:
        access_token = token_info.get('access_token')
        return access_token
    else:
        print("Erro ao obter o token:", token_info)
        return None

def create_quote(access_token):
    url = "https://api.uber.com/v1/customers/a2654670-b8d6-5a67-ab1d-b21344941381/delivery_quotes"
    payload = json.dumps({
        "pickup_address": "{\"street_address\":[\"100 Maiden Ln\"],\"city\":\"New York\",\"state\":\"NY\",\"zip_code\":\"10023\",\"country\":\"US\"}",
        "dropoff_address": "{\"street_address\":[\"30 Lincoln Center Plaza\"],\"city\":\"New York\",\"state\":\"NY\",\"zip_code\":\"10023\",\"country\":\"US\"}",
        "pickup_latitude": 40.7066581,
        "pickup_longitude": -74.0071868,
        "dropoff_latitude": 38.9298375,
        "dropoff_longitude": -77.0582303,
        "pickup_ready_dt": "2024-08-22T14:00:00.000Z",
        "pickup_deadline_dt": "2024-08-22T14:30:00.000Z",
        "dropoff_ready_dt": "2024-08-22T14:30:00.000Z",
        "dropoff_deadline_dt": "2024-08-22T16:00:00.000Z",
        "pickup_phone_number": "+15555555555",
        "dropoff_phone_number": "+15555555555",
        "manifest_total_value": 1000,
        "external_store_id": "my_store_123"
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'Postman/UberEatsMarketplaceCollections',
        'Authorization': f"Bearer {access_token}",
        'Cookie': '__cf_bm=Sk.L7Jl679gGIXR91BnTG08m5wayWDKKKslF6QZmYwM-1722038507-1.0.1.1-xLYhS01qwA9r7V_ERxK1cyvB3fPv2HrXa5g8x8dJlzvuzTZQFsYDneNpO660RkYWkcYT27Ut4aoIZgLe8UYx5g'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()

    
def create_delivery(access_token, quote_id):
    url = "https://api.uber.com/v1/customers/a2654670-b8d6-5a67-ab1d-b21344941381/deliveries"

    payload = json.dumps({
        "pickup_name": "Store Name",
        "pickup_address": "{\"street_address\":[\"100 Maiden Ln\"],\"city\":\"New York\",\"state\":\"NY\",\"zip_code\":\"10023\",\"country\":\"US\"}",
        "pickup_phone_number": "+15555555555",
        "dropoff_name": "Gordon Shumway",
        "dropoff_address": "{\"street_address\":[\"30 Lincoln Center Plaza\"],\"city\":\"New York\",\"state\":\"NY\",\"zip_code\":\"10023\",\"country\":\"US\"}",
        "dropoff_phone_number": "+15555555555",
        "quote_id": quote_id,
        "manifest_items": [
            {
            "name": "Bow tie",
            "quantity": 1,
            "size": "small",
            "dimensions": {
                "length": 20,
                "height": 20,
                "depth": 20
            },
            "price": 100,
            "must_be_upright": False,
            "weight": 300,
            "vat_percentage": 1250000
            }
        ]
        })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}',
        'User-Agent': 'Postman/UberEatsMarketplaceCollections',
        'Cookie': '__cf_bm=y1FCMYYrWmetR7NyU_Mw2A0JbG_IdpARmiNI91I2FJ8-1723748006-1.0.1.1-YYQ3EBuxjSFEdzv75qHX.fO9sM8.jSa.M.I4TafHbYgUFbEdDcnmtUYgNNOIpGQ0Ss.cT7m9VR8WOulaSbNL3Q'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()


client_id = 'o27H5apNOH7754Zc6_wcsKETdUXhZkih'
client_secret = 'M5anb8uIl0KlkpaI7RoH6HsFVNmzRuURzljwZfEv'

# Obtenha o token de acesso
access_token = get_access_token(client_id, client_secret)
print("\nAccess Token:", access_token, "\n")

# Crie uma entrega
quote_response = create_quote(access_token)
print("\nQuote Response:", quote_response, "\n")

delivery_respose = create_delivery(access_token, quote_response['id'])
print("\nDelivery Response:", delivery_respose, "\n")
