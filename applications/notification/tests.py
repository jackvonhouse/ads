from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from applications.notification.models import Notification


class NotificationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.client.force_authenticate(user=self.user)

    def test_notification_creation(self):
        response = self.client.post('/api/notification/', {
            'user': self.user.id,
            'message': 'Test notification'
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Notification.objects.count(), 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.message, 'Test notification')

    def test_notification_retrieval(self):
        Notification.objects.create(user=self.user, message='Test notification')
        response = self.client.get('/api/notification/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['message'], 'Test notification')
