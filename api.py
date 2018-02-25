from datetime import datetime
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import LegacyApplicationClient


class CybApi:

    def __init__(self, username, password, client_id, client_secret, url):
        self.username = username
        self.password = password
        self.client_id = client_id
        self.client_secret = client_secret
        self._base_url = url

        # Get a token via the Resource Owner Password Credential Grant OAuth2 API
        oauth = OAuth2Session(client=LegacyApplicationClient(client_id=client_id))
        self._token = oauth.fetch_token(
                verify=False,
                token_url=self._base_url + "o/token/",
                username=username, password=password,
                client_id=client_id, client_secret=client_secret
                )
        # Make a client for connecting to the API.
        self._client = OAuth2Session(
                client_id,
                token=self._token,
                auto_refresh_url=self._base_url + "o/token/",
                auto_refresh_kwargs={
                    "client_id": client_id,
                    "client_secret": client_secret
                    },
                token_updater=self._token_updater
                )

    def _token_updater(self, token):
        self._token = token


    def register_internrole(self, username, roles):
        url = self._base_url + "api/intern/internroles"
        data = {"username": username, "role": roles}

        request = self._client.post(url, data=data, verify=False)

        if request.status_code == 201:
            return True
        else:
            return False

    def register_card(self, user_id, card_num):
        url = self._base_url + "api/core/cards"
        data = {"card_number": str(card_num), "user": int(user_id)}
        request = self._client.post(url, data=data, verify=False)

        if request.status_code == 201:
            return True
        else:
            return False

    def get_users(self):
        url = self._base_url + 'api/core/users'
        response = self._client.get(url)

        if response.status_code != 200:
            raise Exception('%s: %s' % (response.status_code, response.text))

        return response.json()

    def get_roles(self, username):
        url = self._base_url + '/api/intern/interns?user=&user__username='+username
        response = self._client.get(url)

        if response.status_code != 200:
            raise Exception('%s: %s' % (response.status_code, response.text))

        return response.json()

    def get_sm(self):
        url = self._base_url + 'api/intern/internroles?intern=&role=15&role__id='
        response = self._client.get(url)

        if response.status_code != 200:
            raise Exception('%s: %s' % (response.status_code, response.text))

        return response.json()

    def get_km(self):
        url = self._base_url + 'api/intern/internroles?intern=&role=16&role__id='
        response = self._client.get(url)

        if response.status_code != 200:
            raise Exception('%s: %s' % (response.status_code, response.text))

        return response.json()
    
    def get_userid(self, username):
        url = self._base_url + '/api/core/users?id=&username='+username+'&realname=&email=&is_superuser=1&is_staff=1&is_active=1&date_joined='
        response = self._client.get(url)

        if response.status_code != 200:
            raise Exception('%s: %s' % (response.status_code, response.text))

        return response.json()
