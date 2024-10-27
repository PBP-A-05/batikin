# tests.py

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
from .models import Profile, Address
from .forms import CombinedForm


class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_profile_creation(self):
        profile, created = Profile.objects.get_or_create(user=self.user)
        self.assertTrue(created)
        self.assertEqual(profile.user.username, 'testuser')

    def test_profile_str(self):
        profile, _ = Profile.objects.get_or_create(user=self.user)
        self.assertEqual(str(profile), "testuser's Profile")

    def test_profile_default_profile_picture(self):
        profile, _ = Profile.objects.get_or_create(user=self.user)
        self.assertEqual(
            profile.profile_picture,
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTOizmxkQV5rf4N9ayOC3pojndp0nzIDAFUtg&s"
        )


class AddressModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.address = Address.objects.create(user=self.user, title='Home', address='123 Test Street')

    def test_address_creation(self):
        self.assertEqual(self.address.title, 'Home')
        self.assertEqual(self.address.address, '123 Test Street')
        self.assertEqual(self.address.user.username, 'testuser')

    def test_address_str(self):
        self.assertEqual(str(self.address), 'Home - 123 Test Street')


class CombinedFormTest(TestCase):
    def test_combined_form_valid(self):
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': '1234567890',
        }
        form = CombinedForm(data=data)
        self.assertTrue(form.is_valid())

    def test_combined_form_invalid(self):
        data = {
            'first_name': '',
            'last_name': '',
            'phone_number': '1234567890',
        }
        form = CombinedForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)
        self.assertIn('last_name', form.errors)


class ProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('user_profile:profile')
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_profile_view_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        login_url = settings.LOGIN_URL + '?next=' + self.url
        self.assertRedirects(response, login_url)

    def test_profile_view_get(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account.html')
        self.assertIn('form', response.context)
        self.assertIn('addresses', response.context)
        self.assertIn('open_modal', response.context)

    def test_profile_view_open_modal(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.url + '?open_modal=true')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['open_modal'])

        response = self.client.get(self.url + '?open_modal=false')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['open_modal'])


class UpdateProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('user_profile:update_profile')
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_update_profile_redirect_if_not_logged_in(self):
        response = self.client.post(self.url)
        login_url = settings.LOGIN_URL + '?next=' + self.url
        self.assertRedirects(response, login_url)

    def test_update_profile_invalid_method(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertEqual(json_response['status'], 'error')
        self.assertEqual(json_response['message'], 'Invalid request method')

    def test_update_profile_valid_post(self):
        self.client.login(username='testuser', password='12345')
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': '1234567890',
            'address_0-title': 'Home',
            'address_0-address': '123 Test Street',
            'address_1-title': 'Work',
            'address_1-address': '456 Work Ave',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertEqual(json_response['status'], 'success')
        self.assertEqual(json_response['first_name'], 'Test')
        self.assertEqual(json_response['last_name'], 'User')
        self.assertEqual(json_response['phone_number'], '1234567890')
        self.assertEqual(len(json_response['addresses']), 2)

        # Verify that addresses are saved correctly
        addresses = Address.objects.filter(user=self.user)
        self.assertEqual(addresses.count(), 2)
        self.assertTrue(addresses.filter(title='Home', address='123 Test Street').exists())
        self.assertTrue(addresses.filter(title='Work', address='456 Work Ave').exists())

    def test_update_profile_invalid_data(self):
        self.client.login(username='testuser', password='12345')
        data = {
            'first_name': '',
            'last_name': '',
            'phone_number': '1234567890',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertEqual(json_response['status'], 'error')
        self.assertIn('first_name', json_response['errors'])
        self.assertIn('last_name', json_response['errors'])

    def test_update_profile_replace_addresses(self):
        self.client.login(username='testuser', password='12345')
        # Create initial addresses
        Address.objects.create(user=self.user, title='Old Home', address='Old Address')
        self.assertEqual(Address.objects.filter(user=self.user).count(), 1)

        # Update profile with new addresses
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': '1234567890',
            'address_0-title': 'New Home',
            'address_0-address': 'New Address',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)

        # Verify that old addresses are deleted
        addresses = Address.objects.filter(user=self.user)
        self.assertEqual(addresses.count(), 1)
        self.assertTrue(addresses.filter(title='New Home', address='New Address').exists())
        self.assertFalse(addresses.filter(title='Old Home').exists())


class GetAddressesViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('user_profile:get_addresses')
        self.user = User.objects.create_user(username='testuser', password='12345')
        Address.objects.create(user=self.user, title='Home', address='123 Test Street')

    def test_get_addresses_not_logged_in(self):
        response = self.client.get(self.url)
        login_url = settings.LOGIN_URL + '?next=' + self.url
        self.assertRedirects(response, login_url)

    def test_get_addresses_logged_in(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertIn('addresses', json_response)
        self.assertEqual(len(json_response['addresses']), 1)
        self.assertEqual(json_response['addresses'][0]['title'], 'Home')
        self.assertEqual(json_response['addresses'][0]['address'], '123 Test Street')


class PemesananViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('user_profile:pemesanan')
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_pemesanan_view_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        login_url = settings.LOGIN_URL + '?next=' + self.url
        self.assertRedirects(response, login_url)

    def test_pemesanan_view_logged_in(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pemesanan.html')


class BookingViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('user_profile:booking')
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_booking_view_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        login_url = settings.LOGIN_URL + '?next=' + self.url
        self.assertRedirects(response, login_url)

    def test_booking_view_logged_in(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking.html')
