from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product, Order, OrderItem, Review
from .management.commands.load_product import Command as LoadProductCommand
from wishlist.models import Wishlist
from cart.models import Cart, CartItem
from django.core.management import call_command
from io import StringIO
import json
import tempfile
import os

class ProductModelTest(TestCase):
    def setUp(self):
        self.product_data = {
            "store_url": "https://www.tokopedia.com/enombatik",
            "store_address": "Kabupaten Jogja",
            "product_name": "Batik ENOM - Outer Batik - Batik Wanita Modern Saujana Series - Rivera",
            "price": "Rp341.050",
            "image_urls": [
                "https://images.tokopdeledia.net/img/cache/500-square/hDjmkQ/2024/10/3/06febf3c-7a29-4635-8db5-d4dafdeb8622.jpg.webp?ect=4g",
                "https://images.tokopedia.net/img/cache/100-square/hDjmkQ/2024/10/3/06febf3c-7a29-4635-8db5-d4dafdeb8622.jpg.webp?ect=4g",
            ],
            "additional_info": "Batik ENOM - Outer Batik - Batik Wanita Modern Saujana Series - Rivera\n\nSaujana adalah karya batik yang mengekspresikan keindahan alam...",
            "product_link": "https://www.tokopedia.com/enombatik/batik-enom-outer-batik-batik-wanita-modern-saujana-series-rivera?extParam=src%3Dshop%26whid%3D2983681",
            "category": "pakaian_wanita"
        }
        self.product = Product.objects.create(**self.product_data)

    def test_product_creation(self):
        self.assertTrue(isinstance(self.product, Product))
        self.assertEqual(self.product.__str__(), self.product.product_name)

    def test_product_fields(self):
        for field, value in self.product_data.items():
            self.assertEqual(getattr(self.product, field), value)

class ProductViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.product = Product.objects.create(
            store_url="https://www.tokopedia.com/test",
            store_address="Test Address",
            product_name="Test Product",
            price="Rp100.000",
            image_urls=["https://example.com/image.jpg"],
            additional_info="Test info",
            product_link="https://www.tokopedia.com/test/product",
            category="pakaian_pria"
        )

    def test_product_list_view(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shopping/product_list.html')
        self.assertContains(response, self.product.product_name)

    def test_product_detail_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('product_detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shopping/product_detail.html')

    def test_product_detail_check(self):
        response = self.client.get(reverse('product_detail_check', args=[self.product.id]))
        self.assertEqual(response.status_code, 403)  
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('product_detail_check', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)

    def test_filter_products(self):
        response = self.client.get(reverse('filter_products'), {'category': 'pakaian_pria'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['product_name'], "Test Product")

    def test_add_to_wishlist(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('add_to_wishlist', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'added')

        # Test removing from wishlist
        response = self.client.post(reverse('add_to_wishlist', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'removed')

    def test_add_to_cart(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('add_to_cart', args=[self.product.id]), 
                                    data=json.dumps({'quantity': 1}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('produk berhasil dimasukkan ke keranjang', data['message'])

    def test_get_product(self):
        response = self.client.get(reverse('get_product', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['product_name'], "Test Product")

class LoadProductCommandTest(TestCase):
    def setUp(self):
        self.command = LoadProductCommand()

    def test_determine_category(self):
        self.assertEqual(self.command.determine_category("Batik Wanita", "pakaian_batik_perempuan"), "pakaian_wanita")
        self.assertEqual(self.command.determine_category("Batik Pria", "pakaian_batik_laki"), "pakaian_pria")
        self.assertEqual(self.command.determine_category("Kain Batik", "kain_batik"), "aksesoris")
        self.assertEqual(self.command.determine_category("Gelang Batik", "sesuatu_jogja"), "aksesoris")

    def test_load_json_file(self):
        test_data = [
            {
                "Store URL": "https://www.tokopedia.com/test",
                "Store Address": "Test Address",
                "Product Name": "Test Product",
                "Price": "Rp100.000",
                "Image URLs": ["https://example.com/image.jpg"],
                "Additional Info": "Test info",
                "Product Link": "https://www.tokopedia.com/test/product"
            }
        ]

        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            json.dump(test_data, temp_file)

        products = self.command.load_json_file(temp_file.name, "pakaian_batik_laki")
        os.unlink(temp_file.name)

        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].product_name, "Test Product")
        self.assertEqual(products[0].category, "pakaian_pria")

    def test_load_product_command(self):
        out = StringIO()
        call_command('load_product', stdout=out)
        self.assertIn('Successfully loaded total of', out.getvalue())

class ProductCardTemplateTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            store_url="https://www.tokopedia.com/test",
            store_address="Test Address",
            product_name="Test Product",
            price="Rp100.000",
            image_urls=["https://example.com/image.jpg"],
            additional_info="Test info",
            product_link="https://www.tokopedia.com/test/product",
            category="pakaian_pria"
        )

    def test_product_card_rendering(self):
        response = self.client.get(reverse('product_list'))
        self.assertContains(response, self.product.product_name)
        self.assertContains(response, self.product.price)
        self.assertContains(response, self.product.image_urls[0])
        self.assertContains(response, self.product.get_category_display())

class ProductGridTemplateTest(TestCase):
    def setUp(self):
        self.products = [
            Product.objects.create(
                store_url=f"https://www.tokopedia.com/test{i}",
                store_address=f"Test Address {i}",
                product_name=f"Test Product {i}",
                price=f"Rp{i}00.000",
                image_urls=[f"https://example.com/image{i}.jpg"],
                additional_info=f"Test info {i}",
                product_link=f"https://www.tokopedia.com/test/product{i}",
                category="pakaian_pria"
            ) for i in range(1, 4)
        ]

    def test_product_grid_rendering(self):
        response = self.client.get(reverse('product_list'))
        for product in self.products:
            self.assertContains(response, product.product_name)
            self.assertContains(response, product.price)

    def test_empty_product_grid(self):
        Product.objects.all().delete()
        response = self.client.get(reverse('product_list'))
        self.assertNotContains(response, "No products found in this category.")

class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.product = Product.objects.create(
            store_url="https://www.tokopedia.com/test",
            store_address="Test Address",
            product_name="Test Product",
            price="Rp100.000",
            image_urls=["https://example.com/image.jpg"],
            additional_info="Test info",
            product_link="https://www.tokopedia.com/test/product",
            category="pakaian_pria"
        )
        self.order = Order.objects.create(user=self.user)
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            price=100000
        )

    def test_order_creation(self):
        self.assertTrue(isinstance(self.order, Order))
        self.assertEqual(self.order.user, self.user)

    def test_order_item_creation(self):
        self.assertTrue(isinstance(self.order_item, OrderItem))
        self.assertEqual(self.order_item.order, self.order)
        self.assertEqual(self.order_item.product, self.product)
        self.assertEqual(self.order_item.quantity, 2)
        self.assertEqual(self.order_item.price, 100000)

class ReviewModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.product = Product.objects.create(
            store_url="https://www.tokopedia.com/test",
            store_address="Test Address",
            product_name="Test Product",
            price="Rp100.000",
            image_urls=["https://example.com/image.jpg"],
            additional_info="Test info",
            product_link="https://www.tokopedia.com/test/product",
            category="pakaian_pria"
        )
        self.review = Review.objects.create(
            user=self.user,
            product=self.product,
            rating=4,
            text="Great product!"
        )

    def test_review_creation(self):
        self.assertTrue(isinstance(self.review, Review))
        self.assertEqual(self.review.user, self.user)
        self.assertEqual(self.review.product, self.product)
        self.assertEqual(self.review.rating, 4)
        self.assertEqual(self.review.text, "Great product!")

    def test_review_str_method(self):
        expected_str = f"Review by {self.user.username} for {self.product.product_name}"
        self.assertEqual(str(self.review), expected_str)