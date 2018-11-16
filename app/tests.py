from django.test import TestCase
from django.urls import include, path, reverse
from rest_framework.test import APITestCase
from django.utils import six
import ast


class AccountTests(APITestCase):
    urlpatterns = [
        path('', include('app.urls')),
    ]

    """     Testing of /createuser endpoint """

    # To test if the account is created or not
    def test_create_account(self):

        url = reverse('createuser')

        response = self.client.post(url, {'username': 'test1', 'password1': 'persy@123', 'password2': 'persy@123'})
        response_content = response.content
        if six.PY3:
            response_content = response.content.decode("utf-8")

        response_content = ast.literal_eval(response_content)

        self.assertEqual(response_content['status'], 200)

    # To test response if we enter a wrong username/password
    def test_create_account_with_wrong_password(self):
        url = reverse('createuser')

        response = self.client.post(url, {'username': 'test1', 'password1': 'ppersy@123', 'password2': 'persy@123'})

        response_content = response.content
        if six.PY3:
            response_content = response.content.decode("utf-8")

        response_content = ast.literal_eval(response_content)

        self.assertEqual(response_content['status'], 403)

    """     Testing of /login endpoint  """
    # To Test response if we login with correct Password
    def test_login_with_correct_password(self):

        # To create a user at first

        url = reverse('createuser')
        self.client.post(url, {'username': 'test1', 'password1': 'persy@123', 'password2': 'persy@123'})

        # Login as a user

        url = reverse('login')
        response = self.client.post(url, {'username': 'test1', 'password': 'persy@123'})

        response_content = response.content
        if six.PY3:
            response_content = response.content.decode("utf-8")

        response_content = ast.literal_eval(response_content)

        self.assertEqual(response_content['status'], 200)

    """     Testing of /follow endpoint     """
    def test_follow(self):
        # Create User1
        self.client.post(reverse('createuser'),
                         {'username': 'test1', 'password1': 'persy@123', 'password2': 'persy@123'})
        # Create User2
        self.client.post(reverse('createuser'),
                         {'username': 'test2', 'password1': 'persy@123', 'password2': 'persy@123'})

        # Login using User1 account
        self.client.post(reverse('login'), {'username': 'test1', 'password': 'persy@123'})

        response = self.client.post(reverse('follow'), {'follow': 'test2'})
        response_content = response.content
        if six.PY3:
            response_content = response.content.decode("utf-8")

        response_content = ast.literal_eval(response_content)

        self.assertEqual(response_content['status'], 200)

    """ Testing of /unfollow endpoint"""
    def test_unfollow(self):
        # Create User1
        self.client.post(reverse('createuser'),
                         {'username': 'test1', 'password1': 'persy@123', 'password2': 'persy@123'})
        # Create User2
        self.client.post(reverse('createuser'),
                         {'username': 'test2', 'password1': 'persy@123', 'password2': 'persy@123'})

        # Login using User1 account
        self.client.post(reverse('login'), {'username': 'test1', 'password': 'persy@123'})

        # Follow User2 from User1 account
        self.client.post(reverse('follow'), {'follow': 'test2'})

        response = self.client.post(reverse('unfollow'), {'unfollow': 'test2'})

        response_content = response.content
        if six.PY3:
            response_content = response.content.decode("utf-8")

        response_content = ast.literal_eval(response_content)

        self.assertEqual(response_content['status'], 200)

        # On trying to unfollow a user that is not in your follow list
        response = self.client.post(reverse('unfollow'), {'unfollow': 'test4'})

        response_content = response.content
        if six.PY3:
            response_content = response.content.decode("utf-8")

        response_content = ast.literal_eval(response_content)
        self.assertEqual(response_content['status'], 405)

    """     Testing /tweet endpoint"""

    def test_create_tweet(self):
        # To create a user at first
        self.client.post(reverse('createuser'), {'username': 'test1', 'password1': 'persy@123', 'password2': 'persy@123'})
        self.client.post(reverse('login'), {'username': 'test1', 'password': 'persy@123'})

        response = self.client.post(reverse('tweet'), {'tweet': 'I am doing well'})

        response_content = response.content
        if six.PY3:
            response_content = response.content.decode("utf-8")

        response_content = ast.literal_eval(response_content)
        self.assertEqual(response_content['status'], 200)

    """ Testing /readtweet endpoint """
    def test_read_tweet(self):
        self.client.post(reverse('createuser'),
                         {'username': 'test1', 'password1': 'persy@123', 'password2': 'persy@123'})
        self.client.post(reverse('login'), {'username': 'test1', 'password': 'persy@123'})

        self.client.post(reverse('tweet'), {'tweet': 'I am doing well'})
        self.client.post(reverse('tweet'), {'tweet': 'I am doing very well'})

        # If User tries to read a tweet he is authenticated to read
        response = self.client.get(reverse('readtweet'), {'tweetid': 1})
        self.assertEqual(response.status_code, 200)

        # If user try to read a tweet that he is not authenticated to read
        response = self.client.get(reverse('readtweet'), {'tweetid': 12})

        response_content = response.content
        if six.PY3:
            response_content = response.content.decode("utf-8")
        response_content = ast.literal_eval(response_content)
        self.assertEqual(response_content['status'], 403)


    """     To test the /deletetweet endpoint  """
    def test_delete_tweet(self):
        self.client.post(reverse('createuser'),
                         {'username': 'test1', 'password1': 'persy@123', 'password2': 'persy@123'})
        self.client.post(reverse('login'), {'username': 'test1', 'password': 'persy@123'})

        self.client.post(reverse('tweet'), {'tweet': 'I am doing well'})
        self.client.post(reverse('tweet'), {'tweet': 'I am doing very well'})

        # If user is trying to delete a tweet and user is not authenticated to delete it
        response = self.client.post(reverse('deletetweet'), {'tweetid': 12})

        response_content = response.content
        if six.PY3:
            response_content = response.content.decode("utf-8")
        response_content = ast.literal_eval(response_content)

        self.assertEqual(response_content['status'], 403)

        # If user is trying to delete his own tweet
        response = self.client.post(reverse('deletetweet'), {'tweetid': 1})

        response_content = response.content

        if six.PY3:
            response_content = response.content.decode("utf-8")
        response_content = ast.literal_eval(response_content)

        self.assertEqual(response_content['status'], 200)

    """     To test the /like endpoint  """
    def test_like_tweet(self):
        self.client.post(reverse('createuser'),
                         {'username': 'test1', 'password1': 'persy@123', 'password2': 'persy@123'})
        self.client.post(reverse('login'), {'username': 'test1', 'password': 'persy@123'})

        self.client.post(reverse('tweet'), {'tweet': 'I am doing well'})
        self.client.post(reverse('tweet'), {'tweet': 'I am doing very well'})

        #    On trying to like a tweet that doesn't exist
        response = self.client.post(reverse('like_tweet'), {'tweetid': 123})

        response_content = response.content

        if six.PY3:
            response_content = response.content.decode("utf-8")
        response_content = ast.literal_eval(response_content)

        self.assertEqual(response_content['status'], 403)

        #    On trying to like a tweet that exists

        response = self.client.post(reverse('like_tweet'), {'tweetid': 1})

        response_content = response.content

        if six.PY3:
            response_content = response.content.decode("utf-8")
        response_content = ast.literal_eval(response_content)

        self.assertEqual(response_content['status'], 200)




