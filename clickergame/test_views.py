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


class EnterViewTests(TransactionTestCase):
    def test_no_password_room_redirects(self):
        room = Room.objects.create(name="test room", password="")
        enter_url = reverse("clickergame:enter", kwargs={"pk": room.pk})
        response = self.client.get(enter_url)
        self.assertEqual(response.status_code, 302)
        play_url = reverse("clickergame:play", kwargs={"pk": room.pk})
        self.assertURLEqual(response.url, play_url)
        room.delete()

    def test_password_protected_room_correct_password(self):
        room = Room.objects.create(name="test room", password="password")
        enter_url = reverse("clickergame:enter", kwargs={"pk": room.pk})
        response = self.client.post(enter_url, data={"password": "password"})
        self.assertEqual(response.status_code, 302)
        play_url = reverse("clickergame:play", kwargs={"pk": room.pk})
        self.assertURLEqual(response.url, play_url)
        room.delete()

    def test_password_protected_room_wrong_password(self):
        room = Room.objects.create(name="test room", password="password")
        enter_url = reverse("clickergame:enter", kwargs={"pk": room.pk})
        response = self.client.post(enter_url, data={"password": "wrongpassword"})
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        expected_error = form.get_incorrect_password_error()
        error_msg = expected_error.message % expected_error.params
        self.assertFormError(form=form, field="password", errors=error_msg)
        room.delete()

    def test_password_protected_room_remembers_access(self):
        room = Room.objects.create(name="test room", password="password")
        enter_url = reverse("clickergame:enter", kwargs={"pk": room.pk})
        play_url = reverse("clickergame:play", kwargs={"pk": room.pk})
        response = self.client.post(enter_url, data={"password": "password"})
        self.assertEqual(response.status_code, 302)
        self.assertURLEqual(response.url, play_url)

        response = self.client.get(enter_url)
        self.assertEqual(response.status_code, 302)
        self.assertURLEqual(response.url, play_url)
        room.delete()
