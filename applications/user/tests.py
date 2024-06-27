from django.contrib.auth.models import User
from rest_framework.test import APITestCase


class UserAuthTests(APITestCase):
    def test_user_registration(self):
        response = self.client.post('/api/user/register/', {
            'username': 'testuser',
            'password': 'testpassword123',
            'email': 'testuser@example.com'
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)

    def test_user_login(self):
        User.objects.create_user(username='testuser', password='testpassword123')
        response = self.client.post('/api/user/login/', {
            'username': 'testuser',
            'password': 'testpassword123'
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
