
def API_launch():
    
    global app_config
    global tweepy

# Twitter API configuration
    consumer_key = app_config.twitter["consumer_key"]
    consumer_secret = app_config.twitter["consumer_secret"]

    access_token = app_config.twitter["access_token"]
    access_token_secret = app_config.twitter["access_token_secret"]

# Start
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    return api

def followers_list(number_followers=200):

    global api
    followers = api.followers(count=number_followers)

    followers_name = []
    for follower in followers:
        followers_name.append(str(follower.screen_name))
        return followers_name

def create_db(database_name='bot_detection.db'):

    global sqlite3
    conn = sqlite3.connect(database_name)
    
def create_table(database_name='bot_detection.db'):
    
    global sqlite3
    conn = sqlite3.connect(database_name)
    conn.execute('''CREATE TABLE TWEETS
       (ID INT PRIMARY KEY      NOT NULL,
       NAME            TEXT     NOT NULL,
       DATE            TEXT     NOT NULL,
       TEXT            TEXT     NOT NULL,
       MENTIONS        TEXT     NOT NULL);''')
    conn.close()

def feed_table(ID ,NAME,DATE ,TEXT,MENTIONS,database_name='bot_detection.db'):
    
    global sqlite3
    conn = sqlite3.connect(database_name)
    conn.execute("INSERT INTO TWEETS (ID,NAME,DATE,TEXT,MENTIONS) VALUES (?,?,?,?,?)"
             ,(ID, NAME ,DATE,TEXT, MENTIONS))

    conn.commit()
    conn.close()
    
def tweet_info(follower,tweets_number=100):

    global api
    global json
    global unicodedata
    user_info = api.user_timeline(screen_name = follower,count = tweets_number)

    tweet = {}
    name_mentions = []

    for i,status in enumerate(user_info):
        tweet = status._json
        text = tweet['text']
        date = tweet['created_at']
        entities = tweet['entities']
        user_mentions = entities['user_mentions']
        for mention in user_mentions:
            dict_mentions = mention
            name_mentions = dict_mentions['screen_name']
    
    ID_string   = i
    name_string = follower       
    text_string = unicodedata.normalize('NFKD', text).encode('ascii','ignore')
    date_string = unicodedata.normalize('NFKD', date).encode('ascii','ignore')
    name_mentions_string = unicodedata.normalize('NFKD', name_mentions).encode('ascii','ignore')
    
    feed_table(ID_string,
        name_string,
        text_string,
        date_string,
        name_mentions_string)


    