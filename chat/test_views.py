from django.test import TestCase
from django.urls import reverse

from .models import Message


class PostMessageViewTests(TestCase):
    def test_anonymous_user_posts_guest_message(self):
        post_message_url = reverse("chat:post")
        message_content = "test anonymous user posts guest message"
        self.client.post(post_message_url, {"content": message_content})
        message = Message.objects.first()
        self.assertEquals(message.content, message_content)
        self.assertIsNotNone(message.guest_author)
        message.delete()
