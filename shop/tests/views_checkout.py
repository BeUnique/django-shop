#-*- coding: utf-8 -*-
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test.testcases import TestCase

from shop.addressmodel.models import Country, Address
from shop.models.cartmodel import Cart
from shop.models.ordermodel import Order
from shop.tests.util import Mock
from shop.tests.utils.context_managers import SettingsOverride
from shop.views.checkout import CheckoutSelectionView, ThankYouView

        
class ShippingBillingViewTestCase(TestCase):
    fixtures = ['shop_test_users', 'shop_test_addresses']    

    def setUp(self):
        self.user = User.objects.get(id=1)
        
        self.country = Country.objects.get(id=1)
        
        self.address = Address.objects.get(id=1)
        
        self.request = Mock()
        setattr(self.request, 'user', self.user)
        setattr(self.request, 'session', {})
        setattr(self.request, 'method', 'GET')
    
    def test_shipping_address_cache(self):
        setattr(self.request, 'method', 'POST')
        setattr(self.request, 'POST', {})
        
        view = CheckoutSelectionView(request=self.request)
        res = view.get_shipping_address_form()
        self.assertNotEqual(res, None)
        res2 = view.get_shipping_address_form()
        self.assertEqual(res, res2)
    
    def test_shipping_address_form_post(self):
        setattr(self.request, 'method', 'POST')
        setattr(self.request, 'POST', {})
        
        view = CheckoutSelectionView(request=self.request)
        res = view.get_shipping_address_form()
        self.assertNotEqual(res, None)
    
    def test_shipping_address_form_user_preset(self):
        view = CheckoutSelectionView(request=self.request)
        res = view.get_shipping_address_form()
        self.assertNotEqual(res, None)
    
    def test_shipping_address_form_user_no_preset(self):
        setattr(self.request, 'user', self.user)
        
        address = Address.objects.create(country=self.country, user_shipping=self.user)
        address.save()
        
        view = CheckoutSelectionView(request=self.request)
        res = view.get_shipping_address_form()
        self.assertEqual(res.instance, address)
    
    def test_billing_address_cache(self):
        setattr(self.request, 'method', 'POST')
        setattr(self.request, 'POST', {})
        
        view = CheckoutSelectionView(request=self.request)
        res = view.get_billing_address_form()
        self.assertNotEqual(res, None)
        res2 = view.get_billing_address_form()
        self.assertEqual(res, res2)
    
    def test_billing_address_form_post(self):
        setattr(self.request, 'method', 'POST')
        setattr(self.request, 'POST', {})
        
        view = CheckoutSelectionView(request=self.request)
        res = view.get_billing_address_form()
        self.assertNotEqual(res, None)
    
    def test_billing_address_form_user_preset(self):
        view = CheckoutSelectionView(request=self.request)
        res = view.get_billing_address_form()
        self.assertNotEqual(res, None)
    
    def test_billing_address_form_user_no_preset(self):
        setattr(self.request, 'user', self.user)
        
        address = Address.objects.create(country=self.country, user_billing=self.user)
        address.save()
        
        view = CheckoutSelectionView(request=self.request)
        res = view.get_billing_address_form()
        self.assertEqual(res.instance, address)

    #===========================================================================
    # Billing and shipping form
    #===========================================================================

    def test_billing_and_shipping_selection_post(self):
        setattr(self.request, 'method', 'POST')
        setattr(self.request, 'POST', {})
        view = CheckoutSelectionView(request=self.request)
        res = view.get_billing_and_shipping_selection_form()
        self.assertNotEqual(res, None)
        
    def test_billing_and_shipping_selection_get(self):
        view = CheckoutSelectionView(request=self.request)
        res = view.get_billing_and_shipping_selection_form()
        self.assertNotEqual(res, None)
        
    def test_billing_and_shipping_selection_cached(self):
        view = CheckoutSelectionView(request=self.request)
        res = view.get_billing_and_shipping_selection_form()
        res2 = view.get_billing_and_shipping_selection_form()
        self.assertEqual(res, res2)

    #===========================================================================
    # Context Data
    #===========================================================================
    
    def test_get_context_data(self):
        setattr(self.request, 'method', 'GET')
        view = CheckoutSelectionView(request=self.request)
        ctx = view.get_context_data()
        self.assertNotEqual(ctx, None)
        self.assertNotEqual(ctx['shipping_address'], None)
        self.assertNotEqual(ctx['billing_address'], None)
        self.assertNotEqual(ctx['billing_shipping_form'], None)
        
    #===========================================================================
    # Login Mixin
    #===========================================================================

    def test_must_be_logged_in_if_setting_is_true(self):
        with SettingsOverride(SHOP_FORCE_LOGIN=True):
            resp = self.client.get(reverse('checkout_selection'))
            self.assertEqual(resp.status_code, 302)
            self.assertTrue('accounts/login/' in resp._headers['location'][1])


class ShippingBillingViewOrderStuffTestCase(TestCase):
    fixtures = ['shop_test_orders', 'shop_test_addresses']    

    def setUp(self):
        self.user = User.objects.get(id=1)
        
        self.order = Order.objects.get(id=1)
        
        self.country = Country.objects.get(id=1)
        
        self.s_add = Address.objects.get(id=1) # Shipping
        
        self.b_add = Address.objects.get(id=2) # Billing
        
        self.request = Mock()
        setattr(self.request, 'user', self.user)
        setattr(self.request, 'session', {})
        setattr(self.request, 'method', 'GET')
        
    def check_order_address(self):
        order = self.order
        self.assertEqual(order.shipping_address_text, self.s_add.as_text())
        self.assertEqual(order.billing_address_text, self.b_add.as_text())

    def test_assigning_to_order_from_view_works(self):
        view = CheckoutSelectionView(request=self.request)
        view.save_addresses_to_order(self.order, self.s_add, self.b_add)
        
        self.check_order_address()
        
    def test_assigning_to_order_from_view_works_with_name_and_address(self):
        self.s_add.name = 'toto'
        self.s_add.address2 = 'address2'
        self.s_add.save()
        self.b_add.name = 'toto'
        self.b_add.address2 = 'address2'
        self.b_add.save()
        
        view = CheckoutSelectionView(request=self.request)
        view.save_addresses_to_order(self.order, self.s_add, self.b_add)
        
        self.check_order_address()


class CheckoutCartToOrderTestCase(TestCase):
    fixtures = ['shop_test_carts']

    def setUp(self):
        self.user = User.objects.get(id=1)
        
        self.request = Mock()
        setattr(self.request, 'user', self.user)
        setattr(self.request, 'session', {})
        setattr(self.request, 'method', 'GET')

        self.cart = Cart.objects.get(id=1)

    def test_order_created(self):
        
        view = CheckoutSelectionView(request=self.request)
        res = view.create_order_object_from_cart()
        self.assertEqual(res.order_total, Decimal('0'))

class ThankYouViewTestCase(TestCase):
    fixtures = ['shop_test_orders']

    def setUp(self):
        self.user = User.objects.get(id=1)
        
        self.request = Mock()
        setattr(self.request, 'user', self.user)
        setattr(self.request, 'session', {})
        setattr(self.request, 'method', 'GET')

        self.order = Order.objects.get(id=2)

    def test_get_context_gives_correct_order(self):
        view = ThankYouView(request=self.request)
        self.assertNotEqual(view, None)
        res = view.get_context_data()
        self.assertNotEqual(res, None)
        # refresh self.order from db (it was saved in the view)
        self.order = Order.objects.get(pk=self.order.pk)
        self.assertEqual(self.order.status, Order.COMPLETED)
        ctx_order = res.get('order', None)
        self.assertNotEqual(ctx_order, None)
        self.assertEqual(ctx_order, self.order)
