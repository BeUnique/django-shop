from django.test.testcases import TestCase

from classytags.tests import DummyParser, DummyTokens

from ..models.productmodel import Product
from ..templatetags.shop_tags import Products


class ProductsTestCase(TestCase):
    fixtures = ['shop_test_products']
    def setUp(self):
	    # Set active products
		# We have 3 active + 1 non-active
        product = Product.objects.get(id=2)
        product.active = True
        product.save()
        product2 = Product.objects.get(id=3)
        product2.active = True
        product2.save()
		
    def test01_should_return_all_active_products(self):
        tag = Products(DummyParser(), DummyTokens())
        result = tag.get_context({}, None)
        self.assertTrue(result.has_key('products'))
        self.assertEqual(len(result['products']), 3)

    def test02_should_return_objects_given_as_argument(self):
        tag = Products(DummyParser(), DummyTokens())
        arg_objects = Product.objects.filter(active=False)
        result = tag.get_context({}, arg_objects)
        self.assertTrue(result.has_key('products'))
        self.assertEqual(len(result['products']), 1)

    def test03_should_return_empty_array_if_no_objects_found(self):
        tag = Products(DummyParser(), DummyTokens())
        arg_objects = Product.objects.filter(slug='non-existant-slug')
        result = tag.get_context({}, arg_objects)
        self.assertEqual(len(result['products']), 0)
