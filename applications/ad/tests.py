from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from applications.ad.models import Ad
from applications.category.models import Category


class AdTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.category = Category.objects.create(name='Books')
        self.client.force_authenticate(user=self.user)

    def test_create_ad(self):
        with open('tests/1.png', 'rb') as img:
            response = self.client.post('/api/ads/', {
                'title': 'Old Bookshelf',
                'description': 'A wooden bookshelf in good condition.',
                'category': self.category.id,
                'image': img,
                'user': self.user.id
            }, format='multipart')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Ad.objects.count(), 1)

    def test_edit_ad(self):
        ad = Ad.objects.create(
            title='Old Bookshelf',
            description='A wooden bookshelf in good condition.',
            category=self.category,
            user=self.user
        )

        response = self.client.put(f'/api/ads/{ad.id}/', {
            'title': 'Updated Bookshelf',
            'description': 'A very good wooden bookshelf.',
            'category': self.category.id,
            'user': self.user.id
        })

        self.assertEqual(response.status_code, 200)

        ad.refresh_from_db()

        self.assertEqual(ad.title, 'Updated Bookshelf')
        self.assertEqual(ad.description, 'A very good wooden bookshelf.')

    def test_delete_ad(self):
        ad = Ad.objects.create(
            title='Old Bookshelf',
            description='A wooden bookshelf in good condition.',
            category=self.category,
            user=self.user
        )

        response = self.client.delete(f'/api/ads/{ad.id}/')

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Ad.objects.count(), 0)


class AdCreationWithoutUserTests(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Books')

    def test_create_ad_without_user(self):
        response = self.client.post('/api/ads/', {
            'title': 'Old Bookshelf',
            'description': 'A wooden bookshelf in good condition.',
            'category': self.category.id
        })

        self.assertEqual(response.status_code, 401)


class AdEditDeleteTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='testpassword123')
        self.user2 = User.objects.create_user(username='user2', password='testpassword123')
        self.category = Category.objects.create(name='Books')
        self.ad = Ad.objects.create(
            title='Old Bookshelf',
            description='A wooden bookshelf in good condition.',
            category=self.category,
            user=self.user1
        )

    def test_edit_other_users_ad(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.put(f'/api/ads/{self.ad.id}/', {
            'title': 'Updated Bookshelf',
            'description': 'A very good wooden bookshelf.',
            'category': self.category.id,
            'user': self.user2.id
        })
        self.assertEqual(response.status_code, 403)

    def test_delete_other_users_ad(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(f'/api/ads/{self.ad.id}/')
        self.assertEqual(response.status_code, 403)


class AdViewUnauthorizedTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.category = Category.objects.create(name='Books')
        self.ad = Ad.objects.create(
            title='Old Bookshelf',
            description='A wooden bookshelf in good condition.',
            category=self.category,
            user=self.user
        )

    def test_view_ad_unauthorized(self):
        self.client.logout()
        response = self.client.get(f'/api/ads/{self.ad.id}/')
        self.assertEqual(response.status_code, 401)
