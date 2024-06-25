from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from api.v1.accounts.models import Account
from api.v1.contacts.models import Contact, AreaCode, Telecom

class ContactUnitTest(TestCase):
    def setUp(self):
        # Set up non-modified objects used by all test methods
        self.telecom = Telecom.objects.create(name='Test Telecom')
        self.area_code = AreaCode.objects.create(code='123', telecom=self.telecom)
        self.account = Account.objects.create_user(
            username='testuser',
            password='12345',
            email='test@example.com',
        )
        self.contact = Contact.objects.create(
            name='Test Contact',
            area_code=self.area_code,
            number='12345678',
            email='test@example.com',
            address='Test Address',
            account=self.account
        )

    def test_contact_content(self):
        expected_object_name = f'{self.contact.name}'
        self.assertEquals(expected_object_name, 'Test Contact')

    def test_contact_account(self):
        account = Account.objects.get(username='testuser')
        self.assertEquals(self.contact.account, account)

    def test_contact_area_code(self):
        area_code = AreaCode.objects.get(code='123')
        self.assertEquals(self.contact.area_code, area_code)

class ContactEndpointsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.telecom = Telecom.objects.create(name='Test Telecom')
        self.area_code = AreaCode.objects.create(code='123', telecom=self.telecom)
        self.account = Account.objects.create_user(
            username='testuser',
            password='12345',
            email='test@example.com',
        )
        self.contact = Contact.objects.create(
            name='Test Contact',
            area_code=self.area_code,
            number='12345678',
            email='test@example.com',
            address='Test Address',
            account=self.account
        )
        self.client.login(username='testuser', password='12345')

    def test_area_codes_list(self):
        url = reverse('area-code-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_contacts_list(self):
        url = reverse('contact-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_activities_list(self):
        url = reverse('activity-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class ContactFeatureTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.telecom = Telecom.objects.create(name='Test Telecom')
        self.area_code = AreaCode.objects.create(code='123', telecom=self.telecom)
        self.account = Account.objects.create_user(
            username='testuser',
            password='12345',
            email='test@example.com',
        )
        self.contact = Contact.objects.create(
            name='Test Contact',
            area_code=self.area_code,
            number='12345678',
            email='test@example.com',
            address='Test Address',
            account=self.account
        )
        self.client.login(username='testuser', password='12345')

    def test_create_contact(self):
        url = reverse('contact-list')
        data = {
            'name': 'New Contact',
            'area_code': self.area_code.id,
            'number': '87654321',
            'email': 'new@example.com',
            'address': 'New Address',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Contact.objects.count(), 2)
        self.assertEqual(Contact.objects.get(name='New Contact').number, '87654321')

    def test_update_contact(self):
        url = reverse('contact-detail', kwargs={'uuid': self.contact.uuid})
        data = {
            'name': 'Updated Contact',
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Contact.objects.get(uuid=self.contact.uuid).name, 'Updated Contact')

    def test_number_validation(self):
        # Test with valid number
        contact = Contact(
            name='Test Contact',
            area_code=self.area_code,
            number='12345678',
            email='test@example.com',
            address='Test Address',
            account=self.account
        )
        # Should not raise ValidationError
        try:
            contact.full_clean()
        except ValidationError:
            self.fail("full_clean() raised ValidationError unexpectedly!")

        # Test with invalid number
        contact.number = 'invalid'
        # Should raise ValidationError
        with self.assertRaises(ValidationError):
            contact.full_clean()

    def test_delete_contact(self):
        url = reverse('contact-detail', kwargs={'uuid': self.contact.uuid})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Contact.objects.get(uuid=self.contact.uuid).is_deleted, True)
