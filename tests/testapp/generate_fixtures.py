import os
 
def generate_fixtures():
	os.system(get_fixture_cmd('test_users', 'shop_test_users.json'))
	os.system(get_fixture_cmd('test_addresses', 'shop_test_addresses.json'))
	os.system(get_fixture_cmd('test_carts', 'shop_test_carts.json'))
	os.system(get_fixture_cmd('test_orders', 'shop_test_orders.json'))
	os.system(get_fixture_cmd('test_order_items', 'shop_test_order_items.json'))
	os.system(get_fixture_cmd('test_products', 'shop_test_products.json'))
	os.system(get_fixture_cmd('test_extra_order_item_price_field', 
								  'shop_extra_order_item_price_field.json'))

def get_fixture_cmd(fixture_name, filename):
	cmd = "python manage.py generate_fixture shop.{0} > ../../shop/fixtures/{1}".format(
		fixture_name,
		filename
	)
	return cmd

if __name__ == '__main__':
	os.environ['DJANGO_SETTINGS_MODULE'] = "testapp.settings"
	generate_fixtures()