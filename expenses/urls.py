from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("login/", views.SignInView.as_view(), name="login"),
    path("signup/", views.signup, name="signup"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("password/", auth_views.PasswordChangeView.as_view(
        template_name="password.html", success_url=reverse_lazy("password_done")
    ), name="password"),
    path("password/done/", auth_views.PasswordChangeDoneView.as_view(
        template_name="password_done.html"
    ), name="password_done"),
    path("expenses/new/", views.expense_form, name="expense_new"),
    path("expenses/<int:pk>/edit/", views.expense_form, name="expense_edit"),
    path("expenses/<int:pk>/delete/", views.expense_delete, name="expense_delete"),
]
