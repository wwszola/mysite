from django.test import TransactionTestCase
from django.urls import reverse

from .models import Room


class PlayViewTests(TransactionTestCase):
    def test_no_password_room_allows_to_enter_directly(self):
        room = Room.objects.create(name="test room", password="")
        play_url = reverse("clickergame:play", kwargs={"pk": room.pk})
        response = self.client.get(play_url)
        self.assertEqual(response.status_code, 200)
        room.delete()

    def test_password_protected_room_redirects_to_enter_view(self):
        room = Room.objects.create(name="test room", password="password")
        play_url = reverse("clickergame:play", kwargs={"pk": room.pk})
        response = self.client.get(play_url)
        self.assertEqual(response.status_code, 302)
        enter_url = reverse("clickergame:enter", kwargs={"pk": room.pk})
        self.assertURLEqual(response.url, enter_url)
        room.delete()
