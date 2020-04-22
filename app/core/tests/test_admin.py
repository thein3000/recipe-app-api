from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse 

class AdminSiteTests(TestCase):

    def setUp(self):
        """ Initial Setup for admin site tests"""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email       = "admin@gmail.com",
            password    = "secretos"
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email       = "user@gmail.com",
            password    = "secretos",
            name        = "Carlos Fuentes"
        )

    def test_users_listed(self):
        """ Test that users are listed in the user page"""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email) 

    def test_user_change_page(self):
        """ Test that the user change page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEquals(res.status_code, 200)

    def test_user_add_page(self):
        """ Test that the user add page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEquals(res.status_code, 200)