from fixture_generator import fixture_generator

from django.contrib.auth.models import User
from shop.models.ordermodel import Order
from decimal import Decimal

@fixture_generator(User)
def test_users():
	user = User.objects.create(username='test', email='test@example.com')

@fixture_generator(Order)	
def test_orders():
	order = Order()
	order.order_subtotal = Decimal('0.00')
	order.order_total = Decimal('10.00')
	order.shipping_cost = Decimal('0')
    
	order.shipping_address_text = 'shipping address example'
	order.billing_address_text = 'billing address example'
    
	order.save()