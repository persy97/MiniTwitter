
"""     Imports     """

from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from .models import *
from django.views.decorators.csrf import csrf_exempt


"""     Helper Functions    """


#   Invalid Parameter Error Function
def invalid_parameters():
    my_response = dict()
    my_response['status'] = 422
    my_response['message'] = "Parameters invalid/missing"
    return my_response


#   Invalid Request Error Function
def invalid_request():
    my_response = dict()
    my_response['status'] = 405
    my_response['message'] = "Invalid request"
    return my_response


#   Invalid Access Error Function
def invalid_access():
    my_response = dict()
    my_response['status'] = 403
    my_response['message'] = "Access Denied"
    return my_response


"""     Function to follow the routes   """

#   Method               --->    POST
#   Endpoint             --->    /createuser
#   Parameters Required  --->    username, password1, password2


@csrf_exempt
def create_user(request):
    my_response = dict()
    if request.user.is_authenticated:
        my_response['status'] = 200
        my_response['message'] = "User Logged In"
    elif not request.method == 'POST':
        my_response = invalid_request()
    elif not request.POST.get('username') or not request.POST.get('password1') or not request.POST.get('password2'):
        my_response = invalid_parameters()
    else:
        try:
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                authenticate(username=username, password=password)
                instance = UserDetails()
                instance.username = request.POST.get('username')
                instance.save()
                my_response['status'] = 200
                my_response['message'] = "Account created."

            elif not request.POST.get('username'):
                my_response['status'] = 403
                my_response['message'] = "Username missing"

            elif not request.POST.get('password1') == request.POST.get('password2'):
                my_response['status'] = 403
                my_response['message'] = "Both Passwords don't match"

            else:
                my_response['status'] = 403
                my_response['message'] = "Please try another username and/or a strong password"
        except:
            my_response['status'] = 403
            my_response['message'] = "Username Already taken, Please try another username and/or a strong password"

    return JsonResponse(my_response)


#   Method               --->    POST
#   Endpoint             --->    /login
#   Parameters Required  --->    username, password

@csrf_exempt
def user_login(request):
    my_response = dict()
    if not request.method == 'POST':
        my_response = invalid_request()
    elif not request.POST.get('username') or not request.POST.get('password'):
        my_response = invalid_parameters()

    elif not request.user.is_authenticated and request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))

        if user is None:
            my_response['status'] = 404
            my_response['message'] = "User not Found!"
        else:
            login(request, user)
            my_response['status'] = 200
            my_response['message'] = "User Logged In"
    else:
        my_response['status'] = 200
        my_response['message'] = "User Logged In"
    return JsonResponse(my_response)


#   Method               --->    Any
#   Endpoint             --->    /logout
#   Parameters Required  --->    No Parameters

@csrf_exempt
def logout(request):
    my_response = dict()

    if request.user.is_authenticated:
        logout(request)
        my_response['status'] = 200
        my_response['message'] = "User logged out"

    else:
        my_response = invalid_access()

    return JsonResponse(my_response)


#   Method               --->    POST
#   Endpoint             --->    /follow
#   Parameters Required  --->    follow

@csrf_exempt
def follow(request):
    my_response = dict()

    my_response['status'] = 405
    if not request.method == 'POST':
        my_response = invalid_request()
    elif not request.user.is_authenticated:
        my_response = invalid_access()

    # If proper parameters have not been passed at the endpoint

    elif not request.POST.get('follow'):
        my_response = invalid_parameters()
    else:
        followuser = request.POST.get('follow')
        try:
            followcheck = UserDetails.objects.get(username=followuser)

            # If the user tries to follow himself

            if str(followcheck.username).lower() == str(request.user.username).lower():
                my_response['status'] = 405
                my_response['message'] = "invalid request"
            else:
                try:
                    my_response['status'] = 200
                    my_response['message'] = "Follow list updated"

                    my_instance = Followers.objects.get(username=request.user.username)
                    my_instance = my_instance.objects.get(follow=followuser)

                except:
                    my_instance = Followers()
                    my_instance.username = str(request.user.username)
                    my_instance.follow = str(followcheck.username)
                    my_instance.save()
        except:
            my_response['message'] = "invalid request"

    return JsonResponse(my_response)


#   Method               --->    POST
#   Endpoint             --->    /unfollow
#   Parameters Required  --->    unfollow

@csrf_exempt
def unfollow(request):
    my_response = dict()

    my_response['status'] = 405
    if not request.method == 'POST':
        my_response = invalid_request()
    elif not request.user.is_authenticated:
        my_response = invalid_access()

    # If proper parameters have not been passed in the endpoint
    elif request.POST.get('unfollow') is None:
        my_response = invalid_parameters()

    else:
        unfollowuser = str(request.POST.get('unfollow'))
        try:
            unfollowcheck = UserDetails.objects.get(username=unfollowuser)

            # If the user tries to unfollow himself

            if str(unfollowcheck.username).lower() == str(request.user.username).lower():
                my_response['status'] = 405
                my_response['message'] = "invalid request"

            # If the user tries to unfollow other users

            else:
                my_response['status'] = 200
                my_response['message'] = "Follow list updated"
                my_instance = Followers.objects.get(username=str(request.user.username), follow=str(unfollowuser))

                my_instance.delete()
        except:
            my_response['message'] = "invalid request"

    return JsonResponse(my_response)


#   Method               --->    POST
#   Endpoint             --->    /tweet
#   Parameters Required  --->    tweet

@csrf_exempt
def tweet(request):
    my_response = dict()

    my_response['status'] = 405
    if not request.method == 'POST':
        my_response = invalid_request()

    # If the user is not authenticated
    elif not request.user.is_authenticated:
        my_response['status'] = invalid_access()

    # If proper parameters have not been passed in the endpoint
    elif request.POST.get('tweet') is None:
        my_response = invalid_parameters()
    else:
        tweetsinstance = Tweets()
        tweetsinstance.username = request.user.username
        tweetsinstance.tweet = request.POST.get('tweet')
        tweetsinstance.save()
        my_response['status'] = 200
        my_response['message'] = "Tweet Updated"

    return JsonResponse(my_response)


#   Method               --->    GET
#   Endpoint             --->    /readtweet
#   Parameters Required  --->    tweetid

@csrf_exempt
def read_tweets(request):
    my_response = dict()

    my_response['status'] = 405

    # If the user is not authenticated
    if not request.user.is_authenticated:
        my_response = invalid_access()
    elif not request.method == 'GET':
        my_response = invalid_access()

    else:
        # If no parameter has been passed in the endpoint
        if request.GET.get('tweetid') is None:
            tweets = []
            instance = Tweets.objects.filter(username=request.user.username)
            for i in instance:
                mylist = dict()
                mylist['tweet_id'] = i.id
                mylist['tweet'] = i.tweet
                mylist['tweet_by'] = i.username
                mylist['type'] = i.type
                if i.thread:
                    mylist['reply_to'] = i.thread.id
                else:
                    mylist['reply_to'] = None
                tweets.append(mylist)

            my_response['status'] = 200
            my_response['tweets'] = tweets
        # If the tweetID has been provided as a parameter in the endpoint
        else:

            tweets = []
            try:
                instance = Tweets.objects.get(id=request.GET.get('tweetid'))

                if instance is None:
                    my_response = invalid_access()
                else:
                    tweetedby = instance.username

                    # If the user is trying to retrieve his own tweet

                    if tweetedby == request.user.username:
                        mylist = dict()
                        mylist['tweet_id'] = instance.id
                        mylist['tweet'] = instance.tweet
                        mylist['tweet_by'] = instance.username
                        if instance.thread:
                            mylist['reply_to'] = instance.thread.id
                        else:
                            mylist['reply_to'] = None
                        tweets.append(mylist)
                        my_response['status'] = 200
                        my_response['tweets'] = tweets
                        return JsonResponse(my_response)

                    # If he is trying to retrieve tweet from one of the user he follows

                    follow_instance = Followers.objects.filter(username=request.user.username, follow=tweetedby)
                    if not follow_instance:
                        my_response = invalid_access()
                    else:
                        mylist = dict()
                        mylist['tweet_id'] = instance.id
                        mylist['tweet'] = instance.tweet
                        mylist['tweet_by'] = instance.username
                        tweets.append(mylist)
                        my_response['status'] = 200
                        my_response['tweets'] = tweets

            except:
                my_response = invalid_access()

    return JsonResponse(my_response)


#   Method               --->    POST
#   Endpoint             --->    /deletetweet
#   Parameters Required  --->    tweetid

@csrf_exempt
def delete_tweet(request):
    my_response = dict()

    if not request.method == 'POST':
        my_response = invalid_request()

    # If the user is not authenticated
    elif not request.user.is_authenticated:
        my_response = invalid_access()

    # If incorrect parameters have been passed in the endpoint
    elif request.POST.get('tweetid') is None:
        my_response = invalid_parameters()

    else:
        try:
            tweet_instance = Tweets.objects.get(id=request.POST.get('tweetid'))
            tweet_instance.delete()
            my_response['status'] = 200
            my_response['message'] = "Tweet Deleted"

        except:
            my_response = invalid_access()

    return JsonResponse(my_response)


#   Method               --->    POST
#   Endpoint             --->    /like
#   Parameters Required  --->    tweetid

@csrf_exempt
def like_tweet(request):
    my_response = dict()
    if not request.user.is_authenticated:
        my_response = invalid_access()
    elif not request.method == 'POST':
        my_response = invalid_request()

    elif request.POST.get('tweetid') is None:
        my_response = invalid_parameters()

    else:
        tweet_id = request.POST.get('tweetid')

        tweet_instance = Tweets.objects.filter(id = tweet_id)
        if not tweet_instance:
            my_response = invalid_access()
        else:
            likes_instance = Likes()
            likes_instance.username = request.user.username
            likes_instance.tweet_id = tweet_id
            likes_instance.save()
            my_response['status'] = 200
            my_response['message'] = "Tweet is liked."

    return JsonResponse(my_response)


#   Method               --->    POST
#   Endpoint             --->    /unlike
#   Parameters Required  --->    tweetid

@csrf_exempt
def unlike_tweet(request):
    my_response = dict()
    if not request.user.is_authenticated:
        my_response = invalid_access()

    elif not request.method == 'POST':
        my_response = invalid_request()

    elif request.POST.get('tweetid') is None:
        my_response = invalid_parameters()

    else:
        tweet_id = request.POST.get('tweetid')

        tweet_instance = Tweets.objects.filter(id=tweet_id)
        if not tweet_instance:
            my_response = invalid_request()
        else:
            try:
                likes_instance = Likes.objects.get(id=tweet_id)
                likes_instance.delete()
                my_response['status'] = 200
                my_response['message'] = "Tweet is unliked."
            except:
                my_response = invalid_request()

    return JsonResponse(my_response)


@csrf_exempt
def retweet(request):
    my_response = dict()
    if not request.user.is_authenticated:
        my_response = invalid_access()

    elif not request.method == 'POST':
        my_response = invalid_request()

    elif request.POST.get('tweetid') is None:
        my_response = invalid_parameters()

    else:
        tweetid = request.POST.get('tweetid')
        try:
            original_tweet_instance = Tweets.objects.get(id=tweetid)
            new_tweet = original_tweet_instance.tweet
            new_tweet = "+rt "+new_tweet
            tweets_instance = Tweets()
            tweets_instance.username = request.user.username
            tweets_instance.tweet = new_tweet
            tweets_instance.type = "rt"
            tweets_instance.save()
            my_response['status'] = 200
            my_response['message'] = "Tweet Retweeted"

        except:
            my_response = invalid_request()

    return JsonResponse(my_response)

@csrf_exempt
def reply(request):
    my_response = dict()
    if not request.user.is_authenticated:
        my_response = invalid_access()

    elif not request.method == 'POST':
        my_response = invalid_request()

    elif request.POST.get('tweetid') is None or not request.POST.get('reply'):
        my_response = invalid_parameters()

    else:
        tweet_id = request.POST.get('tweetid')
        reply = request.POST.get('reply')
        try:
            tweet_instance = Tweets.objects.get(id=tweet_id)
            new_tweet_instance = Tweets()
            new_tweet_instance.username = request.user.username
            new_tweet_instance.tweet = reply
            new_tweet_instance.type = "rp"
            new_tweet_instance.thread = tweet_instance
            new_tweet_instance.save()
            my_response['status'] = 200
            my_response['message'] = "Tweet Retweeted"
        except:
            my_response = invalid_request()

    return JsonResponse(my_response)



