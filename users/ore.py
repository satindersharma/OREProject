import requests
import json
from django.conf import settings
from urllib.parse import urlencode, quote
class OREMixin:
    def create_ore_user(self,data):
        '''
        create ORE User
        '''
        url = settings.OREID_APP_URL + "custodial/new-user"
        payload = json.dumps(data)
        headers = {
        'api-key': settings.OREID_API_KEY,
        'service-key': settings.OREID_API_SERVICE_KEY,
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        res = response.json()
        return res

    def send_login_code(self,email):
        '''
        Send a varification code to given email
        '''
        url = settings.OREID_APP_URL + f"account/login-passwordless-send-code?provider=email&email={email}"
        payload = {}
        headers = {
        'api-key': settings.OREID_API_KEY,
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        res = response.json()
        return res    
        
    def verify_login_code(self,email,code):
        '''
        Veriy login code
        '''
        url = settings.OREID_APP_URL + f"account/login-passwordless-verify-code?email={email}&provider=email&code={code}"
        payload = {}
        headers = {
        'api-key': settings.OREID_API_KEY,
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        res = response.json()
        return res        
    def authenticate_ore_user(self,email,code):
        '''
        Passwordless Login - Authenticate ORE User
        return html string
        '''
        callback_url  = quote(settings.OREID_APP_CALLBACK_URL)
        url = f"https://service.oreid.io/auth?provider=email&callback_url={callback_url}&email={email}&code={code}"
        payload = {}
        headers = {
        'api-key': settings.OREID_API_KEY,
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        res = response.text
        return res