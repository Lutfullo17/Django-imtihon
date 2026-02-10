from django.urls import path
from . import views

urlpatterns = [
    path("sotuvchi/", views.mahsular, name="mahsulotlarim"),
    path("sotuvchi/qoshish/", views.mahsulot_add, name="mahsulot_qoshish"),
    path("sotuvchi/<int:id>/tahrir/", views.mahsulot_edit, name="mahsulot_tahrirlash"),
    path("sotuvchi/<int:id>/ochir/", views.mahsulot_delete, name="mahsulot_ochirish"),
    path("maxsulotlar/", views.maxsulotlar, name="maxsulotlar"),
    path("product/<int:id>/", views.maxsulot_detail, name="mahsulot_detail"),

    path("product/<int:id>/like/", views.like_toggle, name="like_toggle"),
    path("sevimlilar/", views.sevimlilar, name="sevimlilar"),

    path("product/<int:id>/comment/add/", views.comment_qoshish, name="comment_qoshish"),
    path("comment/<int:id>/edit/", views.comment_tahrir, name="comment_tahrir"),
    path("comment/<int:id>/delete/", views.comment_ochir, name="comment_ochir"),

    path("seller/dashboard/", views.seller_dashboard, name="seller_dashboard"),
    path("seller/comments/", views.seller_comments, name="seller_comments"),
    path("seller/categories/", views.category_list, name="category_list"),
    path("seller/categories/create/", views.category_create, name="category_create"),
    path("seller/categories/<int:pk>/edit/", views.category_update, name="category_update"),
    path("seller/categories/<int:pk>/delete/", views.category_delete, name="category_delete"),
    path("seller/sold/", views.seller_sotgan_maxs, name="seller_sold_items"),

]
