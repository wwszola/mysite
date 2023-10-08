from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q


class Message(models.Model):
    user_author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
    guest_author = models.CharField(max_length=50, null=True)
    content = models.TextField(null=False)
    pub_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="only_one_author_type",
                check=(
                    (Q(user_author__isnull=True) & Q(guest_author__isnull=False))
                    | (Q(user_author__isnull=False) & Q(guest_author__isnull=True))
                ),
            )
        ]

    @property
    def author(self):
        if self.user_author is not None:
            return self.user_author.get_username()
        else:
            return self.guest_author
