from django.urls import path
from . import views

urlpatterns = [
    path("profil/", views.profil, name="profil"),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout1, name='logout'),
    path('verify_email/', views.Verify_EmailView.as_view(), name='verify_email'),
    path('add_to_cart/<int:id>', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path("profil/", views.profil, name="profil"),
        path("cart/", views.cart_view, name="cart"),
    path("cart/<int:id>/update/", views.cart_update, name="cart_update"),
    path("cart/<int:id>/remove/", views.cart_remove, name="cart_remove"),
    path("checkout/", views.checkout, name="checkout"),
    path("messages/", views.messages_view, name="messages"),
    path("messages/<int:product_id>/<int:user_id>/", views.messages_view, name="messages"),
    path("orders_history/", views.order_history, name="order_history"),

]