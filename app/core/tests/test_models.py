from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_succesful(self):
        """ Tests succesful creation of a user by using email """
        email       = "cfuentes@gmail.com"
        password    = "secretos"

        user = get_user_model().objects.create_user(
            email       = email,
            password    = password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_user_email_is_normalized(self):
        """ Tests that email is normalized for new users """
        email       = "cfuentes@GMAIL.COM"
        password    = "secretos"

        user = get_user_model().objects.create_user(
            email       = email,
            password    = password
        )

        self.assertEqual(user.email, email.lower())
        
    def test_new_user_inavalid_email(self):
        """ Tests that error is raised if user is being created without email """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email       = None,
                password    = "secretos"
            )

    def test_create_super_user(self):
        """ Tests creation of super user """
        user = get_user_model().objects.create_superuser(
                email       = "cfuentes@gmail.com",
                password    = "secretos"
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)