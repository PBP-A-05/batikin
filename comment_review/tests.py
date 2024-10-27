from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from shopping.models import Product
from comment_review.models import Review
from comment_review.forms import ReviewForm
import uuid

class ReviewModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=100.0,
        )
        self.review = Review.objects.create(
            user=self.user,
            product=self.product,
            rating=4,
            review="Great product!"
        )

    def test_review_creation(self):
        self.assertIsInstance(self.review, Review)
        self.assertEqual(self.review.rating, 4)
        self.assertEqual(str(self.review), f"Review by {self.user.username} for {self.product.name}: {self.review.rating} stars")


class ReviewFormTest(TestCase):

    def test_review_form_valid(self):
        form_data = {'rating': 5, 'review': 'Excellent product!'}
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_review_form_invalid(self):
        form_data = {'rating': 'not_a_number'}
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())


class ReviewViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=100.0,
        )
        self.review = Review.objects.create(
            user=self.user,
            product=self.product,
            rating=4,
            review="Great product!"
        )

    def test_create_review_view(self):
        self.client.login(username='testuser', password='password')
        url = reverse('comment_review:create_review', args=[self.product.id])
        response = self.client.post(url, {'rating': 5, 'review': 'Excellent product!'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('redirect_url', response.json())

    def test_edit_review_view(self):
        self.client.login(username='testuser', password='password')
        url = reverse('comment_review:edit_review', args=[self.review.id, self.product.id])
        response = self.client.post(url, {'rating': 3, 'review': 'Updated review'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.review.refresh_from_db()
        self.assertEqual(self.review.rating, 3)
        self.assertEqual(self.review.review, 'Updated review')

    def test_delete_review_view(self):
        self.client.login(username='testuser', password='password')
        url = reverse('comment_review:delete_review', args=[self.review.id])
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Review.objects.filter(id=self.review.id).exists())
