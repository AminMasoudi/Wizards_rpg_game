from django.urls import path
from . import views

app_name = "api"

urlpatterns = [
    path(r"auth", views.auth, name="auth"),
    path(r"roles", views.get_roles, name="all_roles"),
    path(r"role_submission", views.define_role),
]