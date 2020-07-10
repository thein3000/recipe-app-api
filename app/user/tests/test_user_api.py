from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')

def create_user(**params):
    return get_user_model().objects.create(**params)


class PublicUserApiTests(TestCase):
    """ Test the users API (public) """
    
    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_succesful(self):
        """ Test creation of user with valid payload is successful """
        payload = {
            "email": "test@gmail.com",
            "name": "Carlos Fuentes",
            "password": "Secretos1"
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn(payload['password'], res.data)

    def test_user_exists(self):
        """ Test that creation of duplicate user fails"""
        payload = {
            "email": "test@gmail.com",
            "name": "Carlos Fuentes",
            "password": "Secretos1"
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """ Test that user creation fail when password has less then 8 characters """
        payload = {
            "email": "test@gmail.com",
            "name": "Carlos Fuentes",
            "password": "1234567"
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)
