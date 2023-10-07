from urllib.parse import urljoin

from django.contrib.auth import get_user_model
from django.db import models


class UserGithubInfo(models.Model):
    auth_user = models.OneToOneField(
        primary_key=True, to=get_user_model(), on_delete=models.CASCADE, related_name="github_info"
    )
    handle = models.CharField(max_length=39)

    def get_profile_url(self):
        return urljoin("https://github.com", self.handle)
