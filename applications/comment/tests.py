from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from applications.ad.models import Ad
from applications.category.models import Category
from applications.comment.models import Comment


class CommentTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='testpassword123')
        self.user2 = User.objects.create_user(username='user2', password='testpassword123')
        self.category = Category.objects.create(name='Books')
        self.ad = Ad.objects.create(
            title='Bookshelf',
            description='A wooden bookshelf in good condition.',
            category=self.category,
            user=self.user1
        )

    def test_create_comment_unauthenticated(self):
        response = self.client.post(f'/api/comment/', {
            'ad': self.ad.id,
            'content': 'Is this still available?'
        })
        self.assertEqual(response.status_code, 401)

    def test_create_comment_authenticated(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.post(f'/api/comment/', {
            'ad': self.ad.id,
            'content': 'Is this still available?'
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.get().content, 'Is this still available?')

    def test_edit_comment(self):
        self.client.force_authenticate(user=self.user2)
        comment = Comment.objects.create(ad=self.ad, user=self.user2, content='Is this still available?')
        response = self.client.put(f'/api/comment/{comment.id}/', {
            'ad': self.ad.id,
            'content': 'Is this bookshelf still available?'
        })
        self.assertEqual(response.status_code, 200)
        comment.refresh_from_db()
        self.assertEqual(comment.content, 'Is this bookshelf still available?')

    def test_delete_comment(self):
        self.client.force_authenticate(user=self.user2)
        comment = Comment.objects.create(ad=self.ad, user=self.user2, content='Is this still available?')
        response = self.client.delete(f'/api/comment/{comment.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Comment.objects.count(), 0)

    def test_edit_other_users_comment(self):
        self.client.force_authenticate(user=self.user1)
        comment = Comment.objects.create(ad=self.ad, user=self.user2, content='Is this still available?')
        response = self.client.put(f'/api/comment/{comment.id}/', {
            'content': 'Is this bookshelf still available?'
        })
        self.assertEqual(response.status_code, 403)

    def test_delete_other_users_comment(self):
        self.client.force_authenticate(user=self.user1)
        comment = Comment.objects.create(ad=self.ad, user=self.user2, content='Is this still available?')
        response = self.client.delete(f'/api/comment/{comment.id}/')
        self.assertEqual(response.status_code, 403)
