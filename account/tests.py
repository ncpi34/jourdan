from django.db.models.fields.files import FieldFile
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

# https://django-testing-docs.readthedocs.io/en/latest/views.html

class LoginTest(TestCase):
    User = get_user_model()

    def setUp(self):
        self.user = self.User.objects.create_user(email='normal@user.com', password='foo', username='normal',
                                                  company_name='company', siret_number='huhfuidhuie',
                                                  special_prices=[
                                                      {"article_code": "795413", "price_without_taxes": 3.68},
                                                      {"article_code": "857469", "price_without_taxes": 4.94},
                                                      {"article_code": "871397", "price_without_taxes": 5.39}
                                                  ])

    def test_login_user(self):
        self.client.login(username='normal', password='foo')
        response = self.client.get(reverse('website:home'))
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'website/home.html')
        self.client.logout()

    def test_access_profile_without_authentication(self):
        url = reverse('account:profile')
        response = self.client.get(url)
        self.assertTemplateNotUsed(response, 'account/profile.html')
        self.failUnlessEqual(response.status_code, 302)

    def test_create_user(self):
        self.assertEqual(self.user.email, 'normal@user.com')
        self.assertEqual(self.user.username, 'normal')
        self.assertFalse(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
        try:
            # check fields
            self.assertContains(self.user.ci, FieldFile)
            self.assertEqual(self.user.phone, '')
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            self.User.objects.create_user()
        with self.assertRaises(TypeError):
            self.User.objects.create_user(email='', username='')
        with self.assertRaises(ValueError):
            self.User.objects.create_user(email='', username='', password="foo")
