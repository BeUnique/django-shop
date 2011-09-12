from shop.models.ordermodel import OrderExtraInfo, Order
from django.test.testcases import TestCase
from django.contrib.auth.models import User
from shop.tests.util import Mock
from shop.shop_api import ShopAPI
from decimal import Decimal

class ShopApiTestCase(TestCase):
    fixtures = ['shop_test_users', 'shop_test_orders']
    def setUp(self):
        self.user = User.objects.get(username="test")
        
        self.request = Mock()
        setattr(self.request, 'user', None)
        
        self.order = Order.objects.get(id=1)
        self.api = ShopAPI()

    def test_add_extra_info(self):
        res = self.api.add_extra_info(self.order, 'test')
        # Assert that an ExtraOrderInfo item was created
        oei = OrderExtraInfo.objects.get(order=self.order)
        self.assertEqual(oei.text, 'test')

    def test_is_order_payed(self):
        res = self.api.is_order_payed(self.order)
        self.assertEqual(res, False)

    def test_is_order_complete(self):
        res = self.api.is_order_completed(self.order)
        self.assertEqual(res, False)

    def test_get_order_total(self):
        res = self.api.get_order_total(self.order)
        self.assertEqual(res, Decimal('10'))
    
    def test_get_order_subtotal(self):
        res = self.api.get_order_subtotal(self.order)
        self.assertEqual(res, Decimal('10'))

    def test_get_order_short_name(self):
        res = self.api.get_order_short_name(self.order)
        self.assertEqual(res, '1-10')
    
    def test_get_order_unique_id(self):
        res = self.api.get_order_unique_id(self.order)
        self.assertEqual(res, 1)
    
    def test_get_order_for_id(self):
        res = self.api.get_order_for_id(1)
        self.assertEqual(res, self.order)



    
    



    
    
