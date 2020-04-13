from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.add, name="add"),
    path("del/<str:name>/<str:price>", views.deleteView, name="delete"),
    path("register", views.register, name="register"),
    path("login", views.loginView, name="login"),
    path("logout", views.logoutView, name="logout"),
    path("confirmed", views.confirmOrder, name="confirmOrder"),
    path("my_orders", views.myOrders, name="myOrders"),
    path("staff_order/<str:user>/<str:order_number>", views.staff_order, name="staff_order"),
    path("complete_order/<str:user>/<str:order_number>", views.complete_order, name="complete_order"),
    path("deliver", views.deliver, name="deliver"),
    path("test", views.test, name="test"),
    path("add_tip_total/<str:order_number>", views.add_tip_total, name="add_tip_total"),
]
