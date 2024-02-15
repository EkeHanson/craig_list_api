# from django.test import TestCase
# from django.contrib.auth import get_user_model
#
# User = get_user_model()
#
#
# class CustomUserTestCase(TestCase):
#     def test_create_user(self):
#         # Create a regular user
#         user = User.objects.create_user(
#             email='regularuser@example.com',
#             password='testpass',
#             user_type='client',  # Choose the appropriate user type
#             date_of_birth='1990-01-01',  # Set a valid date of birth
#             # Add any other relevant fields
#         )
#
#         # Assert that the user was created successfully
#         self.assertEqual(user.email, 'regularuser@example.com')
#
