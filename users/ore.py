import requests
import json
from django.conf import settings
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
