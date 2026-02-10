from django.urls import path

from . import views

urlpatterns = [
    path("product/<int:product_id>/xabar/", views.sotuvchiga_yozish, name="sotuvchiga_yozish"),
    path("xabarlarim/", views.xabarlarim, name="xabarlarim"),
]