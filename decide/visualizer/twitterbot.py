import tweepy
from voting.models import *
consumer_key = 'ZXutSjYogRFQ1cGSqBExHdFYQ'
consumer_secret = 'bOQoMVaIcYUrTzPba0ogudtIZi6HJZtfTdBaG09EVG60UN6k8Y'
access_token = '1346151287306530817-DshaN1ufww133bG0S8KKSRFWpaBn0y'
access_token_secret = 'vlIKntFymAL3Us2CcnkdbYpa1i2LJ9Q9RwVAt9OFSp668'

def send_twitter_report_json(voting):
    voting_id = voting.get('id')
    voting_name = voting.get('name')
    voting_desc = voting.get('desc')
    voting_q = voting.get('question').get('desc')
    voting_start = voting.get('start_date')
    voting_end = voting.get('end_date')
    voting_tally = voting.get('tally')

    status = "Votación no comenzada"
    if voting_start is not None:     
        if voting_end is None:
            a = voting_start.split("T")[0].split("-")
            start_date=a[2] + " del " + a[1] + " de " + a[0]
            status = "Votación en Curso. Comenzada el " + start_date
        else:
            a = voting_end.split("T")[0].split("-")
            end_date=a[2] + " del " + a[1] + " de " + a[0]
            status = "Votación Finalizada el " + end_date

    post = voting.get('postproc')

    text = "REPORTE DE ESTADO VOTING\n\n"
    text += "Votación: " + str(voting_id) + " - " + voting_name +"\n"
    text += "Estado: " + status + "\n"
    text += "Descripción: " + voting_desc + "\n\n"
      
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api.update_status(text)
# Selector de tipos de votación   
def send_twitter_report(voting):
    if isinstance(voting,VotacionBinaria):
        message = send_twitter_report_binary(voting)
    elif isinstance(voting,Voting):
        message = send_twitter_report_voting(voting)
    return message

