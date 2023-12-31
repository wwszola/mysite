from django.urls import path

from .views import CreateRoomView, EnterRoomView, JoinRoomView, PlayView

app_name = "clickergame"
urlpatterns = [
    path("room/new", CreateRoomView.as_view(), name="create"),
    path("room/<int:pk>", PlayView.as_view(), name="play"),
    path("room/<int:pk>/enter", EnterRoomView.as_view(), name="enter"),
    path("room/<int:pk>/join", JoinRoomView.as_view(), name="join"),
]
