from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView, TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("chat/", include("chat.urls")),
    path("", RedirectView.as_view(pattern_name="home", permanent=True)),
    path("home/", TemplateView.as_view(template_name="home.html"), name="home"),
]
