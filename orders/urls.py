from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add/<str:name>/<str:price>", views.add, name="add"),
    path("del/<str:name>/<str:price>", views.deleteView, name="delete"),
    path("register", views.register, name="register"),
    path("login", views.loginView, name="login"),
    path("logout", views.logoutView, name="logout"),
    path("confirmed/<str:order_number>", views.confirmOrder, name="confirmOrder"),
    path("my_orders/<str:order_number>", views.myOrders, name="myOrders"),
    path("staff_order/<str:user>/<str:order_number>", views.staff_order, name="staff_order"),
    path("complete_order/<str:user>/<str:order_number>", views.complete_order, name="complete_order"),
]
