from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Pizza, Pasta, Order_counter,User_order,Cart, Sub, DinnerPlatter, Salad
from django.db.models import Sum
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.urls import reverse

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
        return render(request,"login.html",{"message":None})
    order_number=User_order.objects.get(user=request.user,status='initiated').order_number
    context = {
        "Checkout":Cart.objects.filter(user=request.user,number=order_number),
        "Total":list(Cart.objects.filter(user=request.user,number=order_number).aggregate(Sum('price')).values())[0],
        "Order_number":order_number,
        "user":request.user,
        "pizzas":Pizza.objects.all(),
        "pastas":Pasta.objects.all(),
        "subs":Sub.objects.all(),
        "salads":Salad.objects.all(),
        "dinner_platters":DinnerPlatter.objects.all()
    }

    return render(request,"index.html",context)

def register(request):
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]
        password2=request.POST["password2"]

        if password != password2:
            return render(request,"register.html",{"message":"Passwords donot match"})

        user = User.objects.create_user(username=username,password=password)
        user.save()
        counter = Order_counter.objects.first()
        order_number = User_order(user=user,order_number=counter.counter)
        order_number.save()
        counter.counter=counter.counter+1
        counter.save()

        return render(request,"login.html",{"message":"Successfully registerd. Now you can login"})
    
    return render(request,"register.html")

def loginView(request):
    
    if request.method=="POST":
      username=request.POST["username"]
      password=request.POST["password"]
      user=authenticate(request,username=username,password=password)
      if user is not None:
          login(request,user)
          return HttpResponseRedirect(reverse("index"))
      else:
          return render(request,"login.html",{"message":"Invalid credentials"}) 
    return render(request,"login.html") 
   

def logoutView(request):
    logout(request)
    return render(request,"login.html",{"message":"Logged out."})

def add(request,name,price):
    order_number = User_order.objects.get(user=request.user,status='initiated').order_number

    add = Cart(user=request.user,number=order_number,name=name,price=price)
    add.save()

    context = {
        "Checkout":Cart.objects.filter(user=request.user,number=order_number),
        "Total":list(Cart.objects.filter(user=request.user,number=order_number).aggregate(Sum('price')).values())[0],
        "Order_number":order_number,
        "user":request.user,
        "pizzas":Pizza.objects.all(),
        "pastas":Pasta.objects.all(),
        "subs":Sub.objects.all(),
        "salads":Salad.objects.all(),
        "dinner_platters":DinnerPlatter.objects.all()
    }

    return render(request,"index.html",context)

def deleteView(request,name,price):
    order_number = User_order.objects.get(user=request.user,status='initiated').order_number

    item = Cart.objects.filter(user=request.user,number=order_number,name=name,price=price)[0]
    item.delete()

    context = {
        "Checkout":Cart.objects.filter(user=request.user,number=order_number),
        "Total":list(Cart.objects.filter(user=request.user,number=order_number).aggregate(Sum('price')).values())[0],
        "Order_number":order_number,
        "user":request.user,
        "pizzas":Pizza.objects.all(),
        "pastas":Pasta.objects.all(),
        "subs":Sub.objects.all(),
        "salads":Salad.objects.all(),
        "dinner_platters":DinnerPlatter.objects.all()
    }

    return render(request,"index.html",context)

def myOrders(request,order_number):
    context = {
        "Checkout":Cart.objects.filter(user=request.user,number=order_number),
        "Total":list(Cart.objects.filter(user=request.user,number=order_number).aggregate(Sum('price')).values())[0],
        "Order_number":order_number,
        "user":request.user,
        "All_my_orders":User_order.objects.filter(user=request.user),
        "Status":User_order.objects.get(user=request.user,order_number=order_number).status
    }
    return render(request,"myOrders.html",context)

def confirmOrder(request,order_number):
   status = User_order.objects.get(user=request.user,status='initiated')
   status.status = 'pending'
   status.save()

   counter=Order_counter.objects.first()
   new_order_number = User_order(user=request.user,order_number=counter.counter)
   new_order_number.save()
   counter.counter = counter.counter+1
   counter.save()

   return myOrders(request,order_number)
    

def staff_order(request,user,order_number):
    user = User.objects.get(username=user)
    context = {
        "Checkout":Cart.objects.filter(user=user,number=order_number),
        "Total":list(Cart.objects.filter(user=user,number=order_number).aggregate(Sum('price')).values())[0],
        "Order_number":order_number,
        "user":user,
        "All_orders":User_order.objects.exclude(status='initiated'),
        "Status":User_order.objects.get(user=user,order_number=order_number).status
    }
    return render(request,"staff_order.html",context)

def complete_order(request,user,order_number):
    user = User.objects.get(username=user)
    complete=User_order.objects.get(user=user,order_number=order_number)
    complete.status = "completed"
    complete.save()

    context = {
        "Checkout":Cart.objects.filter(user=user,number=order_number),
        "Total":list(Cart.objects.filter(user=user,number=order_number).aggregate(Sum('price')).values())[0],
        "Order_number":order_number,
        "user":request.user,
        "All_orders":User_order.objects.exclude(status='initiated'),
        "Status":User_order.objects.get(user=user,order_number=order_number).status
    }
    return render(request,"staff_order.html",context)






