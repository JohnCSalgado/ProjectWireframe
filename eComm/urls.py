from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('success', views.success),
    path("storefront", views.storefront),
    path('addItem/', views.addItem),
    path('<int:item_id>/delete/', views.deleteItem),
    path("purchase",views.purchase),
    path("checkout/", views.checkout),
    path('logout', views.logout),
]