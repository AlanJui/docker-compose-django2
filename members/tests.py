from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from members.models import Member

# Create your tests here.
class ModelTestCase(TestCase):

    def setUp(self):
        print('\n-------------------------')
        print('Setup Test Environment...')
        self.member_first_name = 'ZhengZhong'
        self.member_last_name = 'Ju'
        self.member = Member(
            first_name=self.member_first_name,
            last_name=self.member_last_name,
        )

    def test_model_can_create_a_member( self ):
        print('Test for Model can Created.')
        old_count = Member.objects.count()
        self.member.save()
        new_count = Member.objects.count()
        self.assertNotEqual(old_count, new_count)

class ViewTestCase(TestCase):

    def setUp(self):
        print('\n-------------------------')
        print('Setup Test Environment...')

        self.client = APIClient()

        # Create Test User
        User.objects.create_user('test_user', password='Passw0rd')

        self.client.login(username='test_user', password='Passw0rd')

        self.request_data = {
            'first_name': 'Stacy',
            'last_name': 'Wu',
        }

        self.response = self.client.post(
            reverse('member-list'),
            self.request_data,
            format='json'
        )

    def test_api_can_create_a_record( self ):
        print('Test for CREATE.')

        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Member.objects.count(), 1)
        self.assertEqual(self.response.data['first_name'], self.request_data['first_name'])
        self.assertEqual(self.response.data['last_name'], self.request_data['last_name'])

    def test_api_can_get_a_record( self ):
        print('Test for READ.')
        member = Member.objects.get()
        response = self.client.get(
            reverse('member-detail', kwargs={'pk': member.id}),
            follow='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertContains(response, member)
        self.assertEqual(response.data[ 'first_name' ], self.request_data[ 'first_name' ])
        self.assertEqual(response.data[ 'last_name' ], self.request_data[ 'last_name' ])

    def test_api_can_update_a_record( self ):
        print('Test for UPDATE.')
        member = Member.objects.get()
        changed_data = {
            'first_name': 'Alan',
            'last_name': 'Jui'
        }
        response = self.client.put(
            reverse('member-detail', kwargs={'pk': member.id}),
            changed_data,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[ 'first_name' ], changed_data[ 'first_name' ])
        self.assertEqual(response.data[ 'last_name' ], changed_data[ 'last_name' ])

    def test_api_can_delete_a_record( self ):
        print('Test for DELETE.')
        member = Member.objects.get()
        response = self.client.delete(
            reverse('member-detail', kwargs={'pk': member.id}),
            format='json',
            follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)