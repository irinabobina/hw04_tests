from django.contrib import admin
from django.urls import include, path
from django.contrib.flatpages import views

urlpatterns = [
    path("auth/", include("users.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
    path("about/", include("django.contrib.flatpages.urls")),
]

urlpatterns += [
    path("about-us/", views.flatpage, {"url": "/about-us/"}, name="about"),
    path("terms/", views.flatpage, {"url": "/terms/"}, name="terms"),
    path("about-author/", views.flatpage,
         {"url": "/about-author/"}, name="about-author"),
    path("about-spec/", views.flatpage,
         {"url": "/about-spec/"}, name="about-spec"),
]

urlpatterns += [
    path("", include("posts.urls")),
]