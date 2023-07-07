from django.urls import path
from . import views

app_name = "api"

urlpatterns = [
    path(r"auth", views.auth, name="auth"),
    path(r"roles", views.get_roles, name="all_roles"),
    path(r"role_submission", views.define_role),
    path(r"get_game", views.get_game, name="get_game"),
    path(r"get_game_info", views.game_info, name="game_info")
]