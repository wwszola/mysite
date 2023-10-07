from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView, RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', RedirectView.as_view(pattern_name = 'home', permanent = True)),
    path('home/', TemplateView.as_view(template_name = 'home.html'), name = 'home')
]
