from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from shopping.models import Product
from cart.models import Cart, CartItem, Order, OrderItem
from user_profile.models import Address
from decimal import Decimal
import json
import uuid

class CartViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.product = Product.objects.create(
            id=uuid.uuid4(),
            store_url="https://www.tokopedia.com/enombatik",
            store_address="Kabupaten Jogja",
            product_name="Batik ENOM - Outer Batik",
            price="341050",
            image_urls=["https://example.com/image.jpg"],
            additional_info="Batik ENOM - Outer Batik",
            product_link="https://www.tokopedia.com/enombatik/batik-enom-outer-batik",
            category="pakaian_wanita"
        )
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=1, price=Decimal('341050'))
        self.address = Address.objects.create(user=self.user, title="Home", address="123 Test St")

    def test_view_cart(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('cart:view_cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/view_cart.html')

    def test_add_to_cart(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(
            reverse('cart:add_to_cart', args=[self.product.id]),
            data=json.dumps({'quantity': 1}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue('message' in response_data or 'status' in response_data)

    def test_remove_from_cart(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('cart:remove_from_cart', args=[self.cart_item.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', json.loads(response.content))

    def test_update_cart_item(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(
            reverse('cart:update_cart_item', args=[self.cart_item.id]),
            data=json.dumps({'quantity': 2}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', json.loads(response.content))

    def test_sort_cart_items(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('cart:sort_cart_items'), {'sort_by': 'women'})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(json.loads(response.content), list)

    def test_create_order(self):
        self.client.login(username='testuser', password='12345')
        order_data = {
            'address_id': self.address.id,
            'items': [{'product_id': str(self.product.id), 'quantity': 1, 'price': '341050'}]
        }
        response = self.client.post(
            reverse('cart:create_order'),
            data=json.dumps(order_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('status', json.loads(response.content))

    def test_get_orders_by_user(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('cart:get-order'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('orders', json.loads(response.content))

class CartModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.product = Product.objects.create(
            id=uuid.uuid4(),
            store_url="https://www.tokopedia.com/enombatik",
            store_address="Kabupaten Jogja",
            product_name="Batik ENOM - Outer Batik",
            price="341050",
            image_urls=["https://example.com/image.jpg"],
            additional_info="Batik ENOM - Outer Batik",
            product_link="https://www.tokopedia.com/enombatik/batik-enom-outer-batik",
            category="pakaian_wanita"
        )

    def test_cart_creation(self):
        cart = Cart.objects.create(user=self.user)
        self.assertTrue(isinstance(cart, Cart))
        self.assertEqual(cart.user, self.user)

    def test_cart_item_creation(self):
        cart = Cart.objects.create(user=self.user)
        cart_item = CartItem.objects.create(cart=cart, product=self.product, quantity=1, price=Decimal('341050'))
        self.assertTrue(isinstance(cart_item, CartItem))
        self.assertEqual(cart_item.product, self.product)
        self.assertEqual(cart_item.quantity, 1)

    def test_order_creation(self):
        address = Address.objects.create(user=self.user, title="Home", address="123 Test St")
        order = Order.objects.create(user=self.user, address=address, total_price=Decimal('341050'))
        self.assertTrue(isinstance(order, Order))
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.total_price, Decimal('341050'))

    def test_order_item_creation(self):
        address = Address.objects.create(user=self.user, title="Home", address="123 Test St")
        order = Order.objects.create(user=self.user, address=address, total_price=Decimal('341050'))
        order_item = OrderItem.objects.create(order=order, product=self.product, quantity=1, price=Decimal('341050'))
        self.assertTrue(isinstance(order_item, OrderItem))
        self.assertEqual(order_item.order, order)
        self.assertEqual(order_item.product, self.product)
        self.assertEqual(order_item.quantity, 1)
        self.assertEqual(order_item.price, Decimal('341050'))