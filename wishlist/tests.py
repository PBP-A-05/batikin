from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Wishlist
from shopping.models import Product

class WishlistTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")
        
        # Create sample products
        self.product1 = Product.objects.create(
            product_name="Product 1", price="50000", store_url="http://example.com",
            store_address="123 Example Street", image_urls=["http://example.com/image1.jpg"],
            additional_info="Info 1", product_link="http://example.com/product1", category="pakaian_pria"
        )
        self.product2 = Product.objects.create(
            product_name="Product 2", price="150000", store_url="http://example.com",
            store_address="456 Example Street", image_urls=["http://example.com/image2.jpg"],
            additional_info="Info 2", product_link="http://example.com/product2", category="aksesoris"
        )
    
    def test_wishlist_view(self):
        # Test rendering of wishlist page
        response = self.client.get(reverse('wishlist_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wishlist/wishlist_view.html')
        self.assertIn('wishlist_items', response.context)
        self.assertIn('wishlist_count', response.context)

    def test_add_to_wishlist(self):
        # Test adding product to wishlist
        response = self.client.post(reverse('add_to_wishlist', args=[self.product1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Wishlist.objects.filter(user=self.user, product=self.product1).exists())
        self.assertEqual(response.json()['status'], 'added')

    def test_add_to_wishlist_with_get_method(self):
        # Test invalid GET request for add_to_wishlist view
        response = self.client.get(reverse('add_to_wishlist', args=[self.product1.id]))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Invalid request method')

    def test_remove_from_wishlist(self):
        # Add and then remove product from wishlist
        Wishlist.objects.create(user=self.user, product=self.product1)
        response = self.client.post(reverse('remove_from_wishlist', args=[self.product1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Wishlist.objects.filter(user=self.user, product=self.product1).exists())
        self.assertEqual(response.json()['success'], True)

    def test_remove_from_wishlist_with_nonexistent_product(self):
        # Test removing a product not in wishlist
        response = self.client.post(reverse('remove_from_wishlist', args=[self.product1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['message'], 'Produk tidak ditemukan di wishlist.')

    def test_remove_from_wishlist_with_get_method(self):
        # Test invalid GET request for remove_from_wishlist view
        response = self.client.get(reverse('remove_from_wishlist', args=[self.product1.id]))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['message'], 'Invalid request method')

    def test_sorting_wishlist_items(self):
        # Add two products to wishlist and test sorting
        Wishlist.objects.create(user=self.user, product=self.product1)
        Wishlist.objects.create(user=self.user, product=self.product2)

        # Sort by ascending price
        response = self.client.get(reverse('wishlist_view') + '?sort=price_asc')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['wishlist_items'][0].product, self.product1)

        # Sort by descending price
        response = self.client.get(reverse('wishlist_view') + '?sort=price_desc')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['wishlist_items'][0].product, self.product2)

    def test_save_note_to_wishlist(self):
        # Test saving a note to a wishlist item
        Wishlist.objects.create(user=self.user, product=self.product1)
        response = self.client.post(
            reverse('save_note', args=[self.product1.id]), 
            data={'note': 'Sample note'}
        )
        self.assertEqual(response.status_code, 200)
        wishlist_item = Wishlist.objects.get(user=self.user, product=self.product1)
        self.assertEqual(wishlist_item.note, 'Sample note')
        self.assertEqual(response.json()['message'], 'Catatan berhasil disimpan!')

    def test_save_note_to_nonexistent_wishlist_item(self):
        # Test saving a note for product not in wishlist
        response = self.client.post(reverse('save_note', args=[self.product1.id]), data={'note': 'Sample note'})
        self.assertEqual(response.status_code, 200)
        wishlist_item = Wishlist.objects.get(user=self.user, product=self.product1)
        self.assertEqual(wishlist_item.note, 'Sample note')

    def test_save_note_with_get_method(self):
        # Test invalid GET request for save_note view
        response = self.client.get(reverse('save_note', args=[self.product1.id]))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Invalid request method')

    def test_wishlist_view_empty_state(self):
        # Test wishlist view with no items
        response = self.client.get(reverse('wishlist_view'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tidak ada item di wishlist")
