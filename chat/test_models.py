from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.utils import IntegrityError
from django.test import TestCase

from .models import Message


def get_new_authenticated_user():
    user_model = get_user_model()
    return user_model.objects.create(username="test_user", password="test_password")


class MessageModelTests(TestCase):
    def test_only_one_author_type_constraint(self):
        auth_user = get_new_authenticated_user()
        guest_name = "test_guest_name"
        with self.assertRaises(IntegrityError), transaction.atomic():
            message = Message.objects.create(user_author=auth_user, guest_author=guest_name, content="Test content.")
            message.delete()
        auth_user.delete()
