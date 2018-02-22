from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from members.models import Member

# Create your tests here.

# Using the standard RequestFactory API to create a form POST request
# factory= APIRequestFactory()
# request = factory.post('/api/members/', {'first_name': 'Test Case', 'last_name': 'RESTful API'})


class MemberViewTestCase(APITestCase):
    # url_reverse = reverse('api:member-list')
    url = '/api/members/'
    url_detail = '/api/members/{}/'


    def setUp(self):
        print('Setup Test Environment:')

        self.client = APIClient()

        # Create Test User
        User.objects.create_user('test_user', password='Passw0rd')

        self.client.login(username='test_user', password='Passw0rd')

        self.request_data = {
            'first_name': 'Stacy',
            'last_name': 'Wu',
            'member_id': 2,
        }

        self.member = Member.objects.create(
            first_name='Alan',
            last_name='Jui',
            member_id=1
        )

    def test_api_member_create( self ):
        print('Test for CREATE:')
        self.response = self.client.post(
            self.url,
            self.request_data,
            format='json'
        )
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Member.objects.count(), 2)
        self.assertEqual(Member.objects.get(pk=self.member.id).first_name, 'Alan')
        self.assertEqual(Member.objects.get(pk=self.member.id).last_name, 'Jui')