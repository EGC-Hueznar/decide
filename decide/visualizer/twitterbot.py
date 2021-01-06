import tweepy
from voting.models import *
consumer_key = 'ZXutSjYogRFQ1cGSqBExHdFYQ'
consumer_secret_key = 'bOQoMVaIcYUrTzPba0ogudtIZi6HJZtfTdBaG09EVG60UN6k8Y'
access_token = '1346151287306530817-DshaN1ufww133bG0S8KKSRFWpaBn0y'
access_token_secret = 'vlIKntFymAL3Us2CcnkdbYpa1i2LJ9Q9RwVAt9OFSp668'

def send_twitter_report_json(voting):
    vot_id = voting.get('id')
    vot_name = voting.get('name')
    vot_question = voting.get('question').get('desc')

    options = voting.get('question').get('options')
    post = voting.get('postproc')

    tweet = "Votación: " + vot_name +"\n"
    tweet += vot_question + "\n"
    tweet += "\nResultados: \n"
    for option in post:
        tweet += option.get('option') + " - " + str(option.get('votes')) + " votos \n"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api.update_status(tweet)

