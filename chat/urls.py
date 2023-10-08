from django.urls import path

from .views import IndexChatView, PostMessageView

app_name = "chat"
urlpatterns = [
    path("", IndexChatView.as_view(), name="index"),
    path("post/", PostMessageView.as_view(), name="post"),
]
