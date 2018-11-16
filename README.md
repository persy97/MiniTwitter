# Mini Twitter

  Language Used	-	[Python 3.5](https://www.python.org/)<br>
  Framework Used	-	[Django](https://www.djangoproject.com/) (Version 2.0.2)<br>

## Requirements
  [Python 3.5](https://www.python.org/) <br>
  [pip](https://pip.pypa.io/en/stable/installing/)<br>
  pip install Django==2.0.2<br>
  pip install djangorestframework==3.7.7<br>
 
## Database Used
  sqlite3
  
## Steps to setup the API Server

  1. Clone the repository to your local machine.
  2. Ensure that path environment for Python is set.
  3. Open terminal and go to the base directory of the repository.
  4. Run the following commands to install the required frameworks:
    1. pip install django==2.0.2
    2. pip install djangorestframework==3.7.7
  4. Run the command "python manage.py makemigrations".
  5. Run the command "python manage.py migrate".
  ### To run all the tests of Unit testing/Integration testing
     Run the command "python manage.py test".
  ### To start the API server
     Run the command "python manage.py runserver".
  
   <b>Server will run at http://127.0.0.1:8000/</b>
 <br><br>


 ## API Documentation
  
  ### API Endpoints
  
 1.     Method               --->    POST
        Endpoint             --->    /createuser
        Parameters Required  --->    username, password1, password2
        Description          --->    To create new user, password should be strong (User Registration).
        Authentication       --->    Not Required
  
 2.     Method               --->    POST 
        Endpoint             --->    /login 
        Parameters Required  --->    username, password
        Description          --->    To log in to the API with valid credentials.
        Authentication       --->    Not Required

 3.     Method               --->    Any 
        Endpoint             --->    /logout 
        Parameters Required  --->    No Parameters
        Description          --->    To log out the user.
        Authentication       --->    Required


 4.     Method               --->    POST
        Endpoint             --->    /follow
        Parameters Required  --->    follow
        Description          --->    To follow another user.
        Authentication       --->    Required

 5.     Method               --->    POST
        Endpoint             --->    /unfollow
        Parameters Required  --->    unfollow
        Description          --->    To unfollow another user.
        Authentication       --->    Required


 6.     Method               --->    POST
        Endpoint             --->    /tweet
        Parameters Required  --->    tweet
        Description          --->    To post a tweet.
        Authentication       --->    Required


 7.     Method               --->    GET
        Endpoint             --->    /readtweet
        Parameters Required  --->    tweetid (Not necessary)
        Description          --->    To read tweet. If Parameters are not passed, list of tweets by that user will be shown.
        Authentication       --->    Required


 8.     Method               --->    POST
        Endpoint             --->    /deletetweet
        Parameters Required  --->    tweetid
        Description          --->    To delete one of the tweets.
        Authentication       --->    Required


 9.     Method               --->    POST
        Endpoint             --->    /like
        Parameters Required  --->    tweetid
        Description          --->    To like one of the tweets.
        Authentication       --->    Required


10.     Method               --->    POST
        Endpoint             --->    /unlike
        Parameters Required  --->    tweetid
        Description          --->    To unlike one of the likes tweets.
        Authentication       --->    Required


11.     Method               --->    POST
        Endpoint             --->    /retweet
        Parameters Required  --->    tweetid
        Description          --->    To retweet one of the tweets ("+rt " will be added in front of original tweet).
        Authentication       --->    Required


12.     Method               --->    POST
        Endpoint             --->    /reply
        Parameters Required  --->    tweetid, reply
        Description          --->    To reply to a tweet with some text.
        Authentication       --->    Required
        
        
### Status Codes
  
    200   --->    OK
    404   --->    Not Found
    403   --->    Access Denied
    405   --->    Invalid Request
    422   --->    Invalid Parameters
    
### Example Json Response
  Endpoint - /readtweet
```javascript
  {
      "tweets": 
                [
                  { "tweet_by": "test1",
                    "tweet_id": 1,
                    "tweet": "I am feeling good",
                    "reply_to": null,
                    "type": "nt"
                  },
                  { "tweet_by": "test1",
                    "tweet_id": 2,
                    "tweet": "It was a tiring day",
                    "reply_to": null,
                    "type": "nt"
                   },
                   {  "tweet_by": "test1",
                      "tweet_id": 4, 
                      "tweet": "+rt I am feeling good", 
                      "reply_to": null, 
                      "type": "rt"
                    }, 
                    {  "tweet_by": "test1", 
                       "tweet_id": 5, 
                       "tweet": "Was it really a good day?", 
                       "reply_to": 1, 
                       "type": "rp"
                     }
                  ],
      "status": 200
  }
 ```
  Endpoint - /retweet
  ```javascript
  
  {
    "status": 200,  
    "message": "Tweet Retweeted"
  }
  
  ```
