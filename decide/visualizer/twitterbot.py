import tweepy
from voting.models import *
consumer_key = 'ZXutSjYogRFQ1cGSqBExHdFYQ'
consumer_secret_key = 'bOQoMVaIcYUrTzPba0ogudtIZi6HJZtfTdBaG09EVG60UN6k8Y'
access_token = '1346151287306530817-DshaN1ufww133bG0S8KKSRFWpaBn0y'
access_token_secret = 'vlIKntFymAL3Us2CcnkdbYpa1i2LJ9Q9RwVAt9OFSp668'

def send_twitter_report_json(voting):
    voting_id = voting.get('id')
    voting_name = voting.get('name')
    voting_desc = voting.get('desc')
    voting_q = voting.get('question').get('desc')
    voting_start = voting.get('start_date')
    voting_end = voting.get('end_date') 

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


# Envío de reporte desde un objeto voting
def send_twitter_report_voting(voting):
        voting_id = voting.id
        voting_name = voting.name
        voting_desc = voting.desc
        voting_q = voting.question
        voting_start = voting.start_date
        voting_end = voting.end_date

        status = "Votación no comenzada"
        if voting_start is not None:     
            if voting_end is None:
                a = str(voting_start).split(" ")[0].split("-")
                start_date=a[2] + " del " + a[1] + " de " + a[0]
                status = "Votación en Curso. Comenzada el " + start_date
            else:
                a = str(voting_end).split(" ")[0].split("-")
                end_date=a[2] + " del " + a[1] + " de " + a[0]
                status = "Votación Finalizada el " + end_date

        options = voting_q.options.all()
        post = voting.postproc

        text = "REPORTE DE ESTADO VOTING\n\n"
        text += "Votación: " + str(voting_id) + " - " + voting_name +"\n"
        text += "Estado: " + status + "\n"
        text += "Descripción: " + str(voting_desc) + "\n\n"
        
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        return api.update_status(text)



# Envío de reporte desde un objeto Votación Binaria
def send_twitter_report_binary(v):
    voting_id = v.id
    voting_title = v.titulo
    voting_desc = v.descripcion
    voting_start = v.fecha_inicio
    voting_end = v.fecha_fin
    status = "Votación no comenzada"
    if voting_start is not None:     
        if voting_end is None:
            a = str(voting_start).split(" ")[0].split("-")
            start_date=a[2] + " del " + a[1] + " de " + a[0]
            status = "Votación en Curso. Comenzada el " + start_date
        else:
            a = str(voting_end).split(" ")[0].split("-")
            end_date=a[2] + " del " + a[1] + " de " + a[0]
            status = "Votación Finalizada el " + end_date
    text = "REPORTE DE ESTADO VOTACIÓN BINARIA\n\n"
    text += "Votación: " + str(voting_id) + " - " + voting_title +"\n"
    text += "Estado: " + status + "\n"
    text += "Descripción: " + str(voting_desc) + "\n\n"
    text += "Nº de respuestas Sí: " +str(VotacionBinaria.Numero_De_Trues(v)) + "\n"
    text += "Nº de respuestas No: " +str(VotacionBinaria.Numero_De_Falses(v)) + "\n"
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api.update_status(text)

