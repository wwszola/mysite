from django.db import models
from django.contrib.auth import get_user_model

from urllib.parse import urljoin

class UserGithubInfo(models.Model):
    auth_user = models.OneToOneField(
        primary_key = True,
        to = get_user_model(), 
        on_delete = models.CASCADE, 
        related_name = 'github_info'
    )
    handle = models.CharField(max_length = 39)

    def get_profile_url(self):
        return urljoin('https://github.com', self.handle)

