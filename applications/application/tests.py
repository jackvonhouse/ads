from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from applications.ad.models import Ad
from applications.category.models import Category
from applications.application.models import Application
from applications.notification.models import Notification


class ApplicationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.user = User.objects.create_user(username='user', password='testpassword123')
        self.category = Category.objects.create(name='Books')
        self.ad = Ad.objects.create(
            title='Old Bookshelf',
            description='A wooden bookshelf in good condition.',
            category=self.category,
            user=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_create_application(self):
        response = self.client.post('/api/application/', {
            'ad': self.ad.id,
            'user': self.user.id,
            'comment': 'I would love to have this.',
            'reward': 1337
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Application.objects.count(), 1)
        self.assertEqual(Notification.objects.count(), 1)

        notification = Notification.objects.first()

        self.assertEqual(notification.user, self.user)
        self.assertIn('Новая заявка на Ваше объявление', notification.message)

    def test_accept_application(self):
        application = Application.objects.create(
            ad=self.ad,
            user=self.user,
            comment='I would love to have this.',
            reward=1337
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.post(f'/api/application/{application.id}/accept/')

        self.assertEqual(response.status_code, 200)

        application.refresh_from_db()

        self.assertTrue(application.is_accepted)
        self.assertEqual(Notification.objects.count(), 1)

        notification = Notification.objects.first()

        self.assertEqual(notification.user, self.user)
        self.assertIn('Ваша заявка на объявление', notification.message)

    def test_create_application_unauthorized(self):
        self.client.logout()
        response = self.client.post('/api/application/', {
            'ad': self.ad.id,
            'user': self.user.id,
            'comment': 'I would love to have this.',
            'reward': '1337'
        })

        self.assertEqual(response.status_code, 401)
