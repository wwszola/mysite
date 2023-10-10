from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Message


def get_new_authenticated_user():
    user_model = get_user_model()
    return user_model.objects.create(username="test_user", password="test_password")


class PostMessageViewTests(TestCase):
    def test_anonymous_user_posts_guest_message(self):
        post_message_url = reverse("chat:post")
        message_content = "test anonymous user posts guest message"
        self.client.post(post_message_url, {"content": message_content})
        message = Message.objects.first()
        self.assertEquals(message.content, message_content)
        self.assertIsNotNone(message.guest_author)
        message.delete()

    def test_authenticated_user_cant_post_with_guest_name(self):
        auth_user = get_new_authenticated_user()
        self.client.force_login(auth_user)
        post_message_url = reverse("chat:post")
        message_content = "test authenticated user cant post with guest name"
        guest_name = "forced guest name"
        self.client.post(post_message_url, {"content": message_content, "guest_author": guest_name})
        message = Message.objects.first()
        self.assertEquals(message.content, message_content)
        self.assertEquals(message.author, auth_user.get_username())
        auth_user.delete()
        message.delete()
