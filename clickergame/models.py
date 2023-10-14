from django.contrib.auth import get_user_model
from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=128)
    password = models.CharField(max_length=256, blank=True)
    capacity = models.IntegerField(default=4)

    def is_full(self):
        return Task.objects.filter(room=self).count() >= self.capacity


class Task(models.Model):
    room = models.ForeignKey(Room, on_delete=models.RESTRICT)
    worker = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    goal = models.IntegerField(default=100)
    progress = models.IntegerField(blank=True, default=0)
    last_update = models.DateTimeField(blank=True)

    def advance(self, increment, updated):
        if updated < self.last_update:
            raise ValueError("New update datetime is earlier than last update.")
        if increment <= 0:
            raise ValueError("Advance increment needs to be greater than zero.")

        self.progress = min(self.goal, self.progress + increment)
        self.last_update = updated

    def is_finished(self):
        return self.progress >= self.goal
