import unittest
import uuid

import requests

SERVICE_URL = 'http://localhost:8080'


class MyTestCase(unittest.TestCase):

    def test_status_returns_ok(self):
        r = requests.get(f'{SERVICE_URL}/status')
        self.assertEqual('OK', r.json()['status'])

    def test_version_returns_some_version(self):
        r = requests.get(f'{SERVICE_URL}/version')
        self.assertEqual(200, r.status_code)
        json = r.json()
        self.assertIsNotNone(json['version'])

    def test_get_without_bearer_returns_401(self):
        r = requests.get(f'{SERVICE_URL}/user')
        self.assertEqual(401, r.status_code)

    def test_login_without_correct_user_returns_401(self):
        auth = {'email': 'none', 'password': 'nope'}
        r = requests.post(f'{SERVICE_URL}/user/login', json=auth)
        self.assertEqual(401, r.status_code)

    def test_registration_unique_user(self):
        user = {'first_name': 'John', 'last_name': 'Snow', 'email': f'JohnSnow-{str(uuid.uuid4())}@castle.black',
                'password': 'Wind1'}
        r = requests.put(f'{SERVICE_URL}/user/register', json=user)
        self.assertEqual(200, r.status_code)

        j = r.json()
        self.assertIsNotNone(j['auth_token'])
        self.assertEqual('Successfully registered.', j['message'])
        self.assertEqual('success', j['status'])

    def test_registration_duplicated_user(self):
        user = {'first_name': 'John', 'last_name': 'Snow', 'email': f'JohnSnow-{str(uuid.uuid4())}@castle.black',
                'password': 'Wind1'}
        r = requests.put(f'{SERVICE_URL}/user/register', json=user)
        self.assertEqual(200, r.status_code)

        r = requests.put(f'{SERVICE_URL}/user/register', json=user)
        self.assertEqual(409, r.status_code)

    def test_login_self(self):
        user = {'first_name': 'John', 'last_name': 'Snow', 'email': f'JohnSnow-{str(uuid.uuid4())}@castle.black',
                'password': 'Wind1'}
        r = requests.put(f'{SERVICE_URL}/user/register', json=user)
        self.assertEqual(200, r.status_code)

        auth = {'email': user['email'], 'password': user['password']}
        r = requests.post(f'{SERVICE_URL}/user/login', json=auth)
        self.assertEqual(200, r.status_code)
        self.assertIsNotNone(r.json()['auth_token'])

    def test_get_self(self):
        user = {'first_name': 'John', 'last_name': 'Snow', 'email': f'JohnSnow-{str(uuid.uuid4())}@castle.black',
                'password': 'Wind1'}
        r = requests.put(f'{SERVICE_URL}/user/register', json=user)
        self.assertEqual(200, r.status_code)

        token = r.json()['auth_token']
        r = requests.get(f'{SERVICE_URL}/user', headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(200, r.status_code)
        j = r.json()
        self.assertEqual(user['email'], j['data']['email'])


if __name__ == '__main__':
    unittest.main()
