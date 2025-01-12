from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from beauty_city_app import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path(
        "register/",
        views.UserRegistrationView.as_view(),
        name="user_registration",
    ),
    path("login/", views.UserLoginView.as_view(), name="user_login"),
    path("logout/", views.UserLogoutView.as_view(), name="user_logout"),
    path("test-div/", views.TestDivView.as_view(), name="test_div"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
