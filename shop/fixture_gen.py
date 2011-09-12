from fixture_generator import fixture_generator

from django.contrib.auth.models import User
from shop.addressmodel.models import Address, Country
from shop.models.ordermodel import Order, OrderItem, ExtraOrderItemPriceField, \
    ExtraOrderPriceField
from shop.models.cartmodel import Cart
from shop.models.productmodel import Product
from decimal import Decimal

@fixture_generator(User)
def test_users():
	user = User.objects.create(username='test', email='test@example.com')
	user.first_name = 'Test'
	user.last_name = 'Toto'
	user.save()

@fixture_generator(Order, requires=['shop.test_users'])	
def test_orders():
    order = Order()
    order.order_subtotal = Decimal('10.00')
    order.order_total = Decimal('10.00')
    order.shipping_cost = Decimal('0')
    order.shipping_address_text = 'shipping address example'
    order.billing_address_text = 'billing address example'
    order.save()

    order2 = Order()
    order2.user = User.objects.get(id=1)
    order2.order_subtotal = Decimal('100') # One item worth 100
    order2.order_total = Decimal('120') # plus a test field worth 10
    order2.status = Order.PROCESSING
    order2.save()
	
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
	
    product1 = Product()
    product1.name = 'test'
    product1.slug = 'test'
    product1.unit_price = Decimal('1.0')
    product1.save()
    
    product2 = Product()
    product2.name = 'test2'
    product2.slug = 'test2'
    product2.unit_price = Decimal('1.0')
    product2.save()
    
    product3 = Product()
    product3.name = 'test3'
    product3.slug = 'test3'
    product3.unit_price = Decimal('1.0')
    product3.save()

@fixture_generator(Cart, requires=['shop.test_users'])
def test_carts():
	cart = Cart()
	cart.user = User.objects.get(username='test')
	cart.save()
	
@fixture_generator(Country)
def test_countries():
	country = Country.objects.create(name='CH')
		
@fixture_generator(Address, requires=['shop.test_countries'])
def test_addresses():
    address = Address()
    address.address = 'address'
    address.address2 = 'address2'
    address.zip_code = '1234'
    address.state = 'ZH'
    address.country = Country.objects.get(id=1)
    address.is_billing = False
    address.is_shipping = True
    address.save()	
	
    address2 = Address()
    address2.address = '2address'
    address2.address2 = '2address2'
    address2.zip_code = '21234'
    address2.state = '2ZH'
    address2.country = Country.objects.get(id=1)
    address2.is_billing = True
    address2.is_shipping = False
    address2.save()

@fixture_generator(OrderItem, requires=['shop.test_orders',
										'shop.test_products'])
def test_order_items():
    orderitem = OrderItem()
    orderitem.order = Order.objects.get(id=2)
    orderitem.product_name = 'Test item'
    orderitem.unit_price = Decimal("100")
    orderitem.quantity = 1
    orderitem.line_subtotal = Decimal('100')
    orderitem.line_total = Decimal('110')
    orderitem.save()
	
    orderitem1 = OrderItem()
    orderitem1.order = Order.objects.get(id=1)
    orderitem1.product = Product.objects.get(id=2)
    orderitem1.quantity = 5
    orderitem1.save()
    
    orderitem2 = OrderItem()
    orderitem2.order = Order.objects.get(id=1)
    orderitem2.product = Product.objects.get(id=3)
    orderitem2.quantity = 1
    orderitem2.save()

@fixture_generator(ExtraOrderPriceField, requires=['shop.test_order_items'])
def test_extra_order_price_field():
    eof = ExtraOrderPriceField()
    eof.order = Order.objects.get(id=2)
    eof.label = "Fake Taxes"
    eof.value = Decimal("10")
    eof.save()

@fixture_generator(ExtraOrderItemPriceField, requires=['shop.test_extra_order_price_field'])
def test_extra_order_item_price_field():
    eoif = ExtraOrderItemPriceField()
    eoif.order_item = OrderItem.objects.get(id=1)
    eoif.label = 'Fake extra field'
    eoif.value = Decimal("10")
    eoif.save()