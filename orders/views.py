from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from .models import menu_items, Order_counter,User_order,Cart, OrderDetails
from django.db.models import Sum
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.urls import reverse
from orders.business_logic import compute_order_total, compute_order_count, compute_confirmation_number

# Create your views here.
counter = Order_counter.objects.first()
if counter==None:
    set_counter = Order_counter(counter=1)
    set_counter.save()

#temperory - untill register is created
 #  counter=Order_counter.objects.first()
  #  order_number=User_order(user=user,order_number=counter.counter)
   #     order_number.save()
    #    counter.counter=counter.counter+1
     #   counter.save()

def index(request):
    if not request.user.is_authenticated:
        return render(request, "deliver.html", {"message": None})
    order_number = User_order.objects.get(user=request.user, status='initiated').order_number

    item_total = compute_order_total(Cart.objects.filter(user=request.user, number=order_number))
    context = {
        "Checkout":Cart.objects.filter(user=request.user, number=order_number),
        "Total": item_total,
        "Order_number": order_number,
        "user": request.user,
        "menu_items": menu_items.objects.all(),

    }
    print(context)
    return render(request, "index.html", context)

def register(request):
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]
        password2=request.POST["password2"]
        first_name = request.POST["password2"]

        if password != password2:
            return render(request, "register.html", {"message": "Passwords do not match"})

        user = User.objects.create_user(username=username, password=password)
        user.save()
        counter = Order_counter.objects.first()
        order_number = User_order(user=user, order_number=counter.counter)
        order_number.save()
        counter.counter = counter.counter+1
        counter.save()

        return render(request, "login.html", {"message": "Successfully registerd. Now you can login"})
    
    return render(request, "register.html")

def loginView(request):
    
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
          login(request, user)
          return  HttpResponseRedirect(reverse("index"))
        else:
          return render(request, "login.html", {"message": "Invalid credentials"})
    return render(request, "login.html")


def deliver(request):

    return render(request, "deliver.html")

def test(request):

    return render(request, "test.html")


def logoutView(request):
    logout(request)
    return render(request, "login.html", {"message":"Logged out."})


def add(request):

    menu_item_name = request.POST["menu_item"]
    menu_item_price = menu_items.objects.get(name=menu_item_name).price
    order_number = User_order.objects.get(user=request.user, status='initiated').order_number
    add = Cart(user=request.user, number=order_number, name=menu_item_name, price=menu_item_price)
    add.save()

    # Business logic of item totals #
    item_count = len(list(Cart.objects.filter(user=request.user, number=order_number)))
    item_count = 0 if item_count == 0 else item_count
    item_total = compute_order_total(Cart.objects.filter(user=request.user, number=order_number))
    context = {
        "Checkout": Cart.objects.filter(user=request.user, number=order_number),
        "Total": item_total,
        "Order_number": order_number,
        "user": request.user,
        "item_count": item_count,
        "menu_items": menu_items.objects.all(),
    }

    return render(request, "index.html", context)


def deleteView(request, name, price):

    order_number = User_order.objects.get(user=request.user, status='initiated').order_number
    item = Cart.objects.filter(user=request.user, number=order_number, name=name, price=price)[0]

    item.delete()

    item_count = compute_order_count(Cart.objects.filter(user=request.user, number=order_number))
    item_count = 0 if item_count == 0 else item_count
    item_total = compute_order_total(Cart.objects.filter(user=request.user, number=order_number))

    context = {
        "Checkout": Cart.objects.filter(user=request.user, number=order_number),
        "Total": item_total,
        "Order_number": order_number,
        "user": request.user,
        "menu_items": menu_items.objects.all(),
        "item_count": item_count
    }

    return render(request, "index.html", context)

def myOrders(request):

    # Get Order Number for user
    order_number = User_order.objects.get(user=request.user, status='initiated').order_number

    totals_dict = compute_order_total(Cart.objects.filter(user=request.user, number=order_number))

    img_locations = list(OrderDetails.objects.filter(user=request.user, number=order_number).values())

    cartinfos = list(Cart.objects.filter(user=request.user, number=order_number).values())

    item_count = compute_order_count(Cart.objects.filter(user=request.user, number=order_number))
    for idx, item in enumerate(cartinfos):
        item.update({'img_location': img_locations[idx]['img_location']})
    context = {
        "Checkout": cartinfos,
        "Total": totals_dict,
        "Order_number": order_number,
        "user":request.user,
        "All_my_orders": User_order.objects.filter(user=request.user),
        "Status": User_order.objects.get(user=request.user, order_number=order_number).status,
        "item_count": item_count
    }
    return render(request, "myOrders.html", context)

def confirmOrder(request):

   order_number = User_order.objects.get(user=request.user, status='initiated').order_number
   status = User_order.objects.get(user=request.user, status='initiated')
   status.status = 'Pending'
   status.order_confirmation = compute_confirmation_number()
   status.save()

   counter=Order_counter.objects.first()
   new_order_number = User_order(user=request.user, order_number=counter.counter)
   new_order_number.save()
   counter.counter = counter.counter+1
   counter.save()

   item_total = compute_order_total(Cart.objects.filter(user=request.user, number=order_number))
   context = {
       "Checkout": Cart.objects.filter(user=request.user, number=order_number),
       "Total": item_total,
       "Order_number": order_number,
       "user": request.user,
       "All_my_orders": User_order.objects.filter(user=request.user),
       "Status": User_order.objects.get(user=request.user, order_number=order_number).status,
       'order_confirmation': User_order.objects.get(user=request.user, order_number=order_number).order_confirmation
   }
   return render(request, "order_completion.html", context)
    

def staff_order(request, user, order_number):
    user = User.objects.get(username=user)
    context = {
        "Checkout": Cart.objects.filter(user=user, number=order_number),
        "Total": list(Cart.objects.filter(user=user, number=order_number).aggregate(Sum('price')).values())[0],
        "Order_number": order_number,
        "user": user,
        "All_orders": User_order.objects.exclude(status='initiated'),
        "Status": User_order.objects.get(user=user, order_number=order_number).status
    }
    return render(request, "staff_order.html", context)

def complete_order(request, user, order_number):
    user = User.objects.get(username=user)
    complete = User_order.objects.get(user=user,order_number=order_number)
    complete.status = "completed"
    complete.save()

    context = {
        "Checkout": Cart.objects.filter(user=user,number=order_number),
        "Total": list(Cart.objects.filter(user=user,number=order_number).aggregate(Sum('price')).values())[0],
        "Order_number": order_number,
        "user": request.user,
        "All_orders": User_order.objects.exclude(status='initiated'),
        "Status": User_order.objects.get(user=user, order_number=order_number).status
    }
    return render(request, "staff_order.html", context)


def add_tip_total(request, order_number):

    totals_dict = compute_order_total(Cart.objects.filter(user=request.user, number=order_number))
    print(totals_dict)
    return JsonResponse(totals_dict)

