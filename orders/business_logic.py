import math
from django.db.models import Sum

def compute_order_total(x):
    price = list(x.aggregate(Sum('price')).values())[0]
    return price