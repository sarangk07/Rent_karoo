from django.urls import path
from . import views


urlpatterns = [
    path("register/", views.register, name="register"),
    path("", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("dashbord/", views.dashbord, name="dashbord"),
    path("editProfile/", views.editProfile, name="editProfile"),
    path("forgotpassword/", views.forgotpassword, name="forgotpassword"),
    path("activate/<uidb64>/<token>", views.activate, name="activate"),
    path(
        "resetpassword_validate/<uidb64>/<token>",
        views.resetpassword_validate,
        name="resetPassword_validate",
    ),
    path("resetPassword/", views.resetPassword, name="resetPassword"),
    path("cancel/<int:id>", views.cancel, name="cancel"),
    path("changePassword/", views.changePassword, name="changePassword"),
]
