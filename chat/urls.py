from django.urls import path

from .views import PostMessageView, ReadMessagesPartialView

app_name = "chat"
urlpatterns = [
    path("post/", PostMessageView.as_view(), name="post"),
    path("read/<int:length>", ReadMessagesPartialView.as_view(), name="read"),
]
