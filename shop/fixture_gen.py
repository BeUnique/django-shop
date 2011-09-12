from fixture_generator import fixture_generator

from django.contrib.auth.models import User
from shop.models.ordermodel import Order
from shop.models.cartmodel import Cart
from shop.models.productmodel import Product
from decimal import Decimal

@fixture_generator(User)
def test_users():
	user = User.objects.create(username='test', email='test@example.com')
	user.first_name = 'Test'
	user.last_name = 'Toto'
	user.save()

@fixture_generator(Order)	
def test_orders():
	order = Order()
	order.order_subtotal = Decimal('0.00')
	order.order_total = Decimal('10.00')
	order.shipping_cost = Decimal('0')
    
	order.shipping_address_text = 'shipping address example'
	order.billing_address_text = 'billing address example'
    
	order.save()
	
@fixture_generator(Product)
def test_products():
	product = Product()
	product.name = "TestProduct"
	product.slug = "TestProduct"
	product.short_description = "TestProduct"
	product.long_description = "TestProduct"
	product.active = True
	product.unit_price = Decimal('100')
	product.save()

@fixture_generator(Cart, requires=['shop.test_users'])
def test_carts():
	cart = Cart()
	cart.user = User.objects.get(username='test')
	cart.save()