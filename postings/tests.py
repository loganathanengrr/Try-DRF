from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse as api_reverse

from rest_framework_jwt.settings import api_settings

from .models import BlogPost

payload_handler = api_settings.JWT_PAYLOAD_HANDLER
encode_handler  = api_settings.JWT_ENCODE_HANDLER

User = get_user_model()

class BlogPostAPITestCase(APITestCase):

    def setUp(self):
        user_obj = User(username="test", email="test@test.com")
        user_obj.set_password("testpass")
        user_obj.save()
        blog_post = BlogPost.objects.create(
            user=user_obj,
            title='new title',
            content='new content'
            )
    def test_single_user(self):
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)
    
    def test_single_post(self):
        post_count = BlogPost.objects.count()
        self.assertEqual(post_count, 1)
    
    def test_get_list(self):
        data = {}
        url  = api_reverse('api-postings:post-listcreate')
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_post_item(self):
        data = {
            "title":"post-1",
            "content":"some content"
        }
        url = api_reverse('api-postings:post-listcreate')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_get_item(self):
        blog_post = BlogPost.objects.first()
        data = {}
        url = blog_post.get_api_url()
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_update_item(self):
        blog_post = BlogPost.objects.first()
        url = blog_post.get_api_url()
        data = {'title': 'Some title', 'content': 'some random content'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_update_item_with_user(self):
        blog_post = BlogPost.objects.first()
        user_obj = User.objects.first()
        url = blog_post.get_api_url()
        data = {'title': "Some title", 'content': 'some random content'}
        payload = payload_handler(user_obj)
        token_resp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT '+ token_resp)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_post_item_with_user(self):
        user_obj = User.objects.first()
        url = api_reverse("api-postings:post-listcreate")
        data = {'title': "test title-2", 'content': 'new content'}
        payload = payload_handler(user_obj)
        token_resp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_resp)
        response = self.client.post(url, data, format='json')
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_user_ownership(self):
        owner = User.objects.create(username="testsuser2")
        blog_post = BlogPost.objects.create(
            user=owner,
            title='New title',
            content='some_random_content'
        )
        user_obj = User.objects.first()
        self.assertNotEqual(user_obj.username, owner.username)
        payload = payload_handler(user_obj)
        token_resp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT '+ token_resp)
        url = blog_post.get_api_url()
        data = {"title":"some test title", "content":"some random content"}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_login_and_update(self):
        data = {
            'username': "test",
            'password':'testpass'
        }
        login_url =  api_reverse('api-login')
        login_resp = self.client.post(login_url, data, format='json')
        self.assertEqual(login_resp.status_code, status.HTTP_200_OK)
        token = login_resp.get('token')
        if token is not None:
            blog_post = BlogPost.objects.first()
            url =  blog_post.get_api_url()
            data = {
                "title":"new2 title",
                "content":"new content"
                }
            self.client.credentials(HTTP_AUTHORIZATION="JWT "+token)
            response = self.client.post(url, data, format=json)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
