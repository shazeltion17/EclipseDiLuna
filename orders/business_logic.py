import math
import string
import random
from decimal import *
from django.db.models import Sum

def compute_order_total(x):
    tax_rate = .07
    sub_total = list(x.aggregate(Sum('price')).values())[0]
    try:
        tax = round(Decimal(tax_rate) * Decimal(sub_total),2)
        final_total = tax + Decimal(sub_total)
    except:
        tax = 0
        final_total = 0
        sub_total = 0
    return {'tax': tax, 'sub_total': sub_total, 'final_total': final_total}

def compute_order_count(order_query):
    count = len(list(order_query))
    return count

def compute_confirmation_number():
    confirmation_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    print(confirmation_number)
    return confirmation_number

