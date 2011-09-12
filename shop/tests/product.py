# -*- coding: utf-8 -*-
from decimal import Decimal
from shop.models.productmodel import Product
from shop.models.ordermodel import Order, OrderItem
from django.test.testcases import TestCase

class ProductTestCase(TestCase):
    fixtures = ['shop_test_products']

    def setUp(self):
        self.product = Product.objects.get(id=1)
        self.product.active = False
        self.product.save()
    
    def test_unicode_returns_proper_stuff(self):
        ret = self.product.__unicode__()
        self.assertEqual(ret, self.product.name)
        
    def test_active_filter_returns_only_active_products(self):
        ret1 = len(Product.objects.active())
        # Set self.product to be active
        self.product.active = True
        self.product.save()
        ret2 = len(Product.objects.active())
        self.assertNotEqual(ret1, ret2)
        self.assertEqual(ret1, 0)
        self.assertEqual(ret2, 1)

    def test_get_name_works_properly_by_default(self):
        res = self.product.get_name()
        self.assertEqual(res, self.product.name)
    
class ProductStatisticsTestCase(TestCase):
    fixtures = ['shop_test_order_items']
	
    def setUp(self):
        self.product = Product.objects.get(name='TestProduct')
        self.product1 = Product.objects.get(name='test')
        self.product2 = Product.objects.get(name='test2')
        self.product3 = Product.objects.get(name='test3')

        self.order = Order.objects.get(id=1)
        
        self.orderitem1 = OrderItem.objects.get(id=2)
        self.orderitem2 = OrderItem.objects.get(id=3)

    def test_top_selling_works(self):
        res = Product.statistics.top_selling_products(10)
        self.assertNotEqual(res, None)
        self.assertEqual(len(res), 3)
        self.assertTrue(self.product3 not in res)

