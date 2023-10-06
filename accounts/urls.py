from django.urls import path, reverse_lazy

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import get_user_model

from django.views.generic import DetailView

from .views import ProfileDetailView, ProfileUpdateView

app_name = 'accounts'
urlpatterns = [
    path('login/', LoginView.as_view(template_name = 'login.html', next_page = reverse_lazy('home')), name = 'login'),
    path('logout/', LogoutView.as_view(next_page = reverse_lazy('home')), name = 'logout'),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name = 'profile'),
    path('update/', ProfileUpdateView.as_view(), name = 'update')
]