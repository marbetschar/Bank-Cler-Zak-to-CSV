import requests
import uuid

class ApiClient:

    def __init__(self):
        self.__scheme = 'https://'
        self.__host = 'zak.prd.cler.ch'
        self.__headers = {
            'Accept-Language': 'de',
            'Accept-Encoding': 'identity',
            'ClientId': 'clerzakr7',
            'User-Agent': 'Zak/3.51.0.11854 (Android 14)',
            'X-Zak-Device-Id': str(uuid.uuid4()),
            'X-Same-Domain': 'forCsrfProtection',
            'Connection': 'close'
        }
        self.__cookies = None

    def __url(self, path):
        return self.__scheme + self.__host + path

    def __session_open(self):
        response = requests.get(
            url=self.__url('/public/api/open'),
            headers=self.__headers,
            cookies=self.__cookies
        )

        if not response.ok:
            response.raise_for_status()

        self._cookies = response.cookies

    def __session_close(self):
        response = requests.delete(url=self.__url('/auth/rest/public/authentication'))

        if not response.ok:
            response.raise_for_status()

        self.__cookies = None

    def __password_check(self, username, password):
        response = requests.post(
            url=self.__url('/auth/rest/public/authentication/password/check'),
            json={'password': password, 'username': username},
            headers=self.__headers,
            cookies=self.__cookies
        )

        if not response.ok:
            response.raise_for_status()

        self.__cookies = response.cookies

    def login(self, username, password):
        self.__session_open()
        self.__password_check(username, password)

    def logout(self):
        self.__session_close()

    def transactions(self):
        response = requests.get(
            url=self.__url('/cler-ws-0.0.1/webapi/transaction'),
            headers=self.__headers,
            cookies=self.__cookies
        )

        if not response.ok:
            response.raise_for_status()

        return response.json()
