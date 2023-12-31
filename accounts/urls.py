from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, reverse_lazy

from .views import AccountDeleteView, ProfileDetailView, ProfileUpdateView, RegisterView

app_name = "accounts"
urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path(
        "login/", LoginView.as_view(template_name="accounts/login.html", next_page=reverse_lazy("home")), name="login"
    ),
    path("logout/", LogoutView.as_view(next_page=reverse_lazy("home")), name="logout"),
    path("profile/<int:pk>", ProfileDetailView.as_view(), name="profile"),
    path("update/", ProfileUpdateView.as_view(), name="update"),
    path("delete/", AccountDeleteView.as_view(), name="delete"),
]
