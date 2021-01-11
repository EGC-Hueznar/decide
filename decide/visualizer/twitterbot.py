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

def send_twitter_report(voting):
    if isinstance(voting,Voting):
        message = send_twitter_report_voting(voting)
    elif isinstance(voting,VotacionBinaria):
        message = send_twitter_report_binary(voting)
    elif isinstance(voting,Votacion):
        message = send_twitter_report_normal(voting)
    elif isinstance(voting,VotacionPreferencia):
        message = send_twitter_report_preferencia(voting)    
    return message

def send_twitter_report_voting(voting):
    vot_id = voting.id
    vot_name = voting.name
    vot_desc = voting.desc
    vot_q = voting.question
    options = voting_q.options.all()
    post = voting.postproc
   
    tweet = "Votación: " + voting.name +"\n"
    tweet += "Descripción: " + str(voting_desc) +"\n"
    tweet += str(voting_q) + "\n"
    tweet += "\nResultados: \n"
    for option in post:
        tweet += option.get('option') + " - " + str(option.get('votes')) + " votos \n"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api.update_status(tweet)

def send_twitter_report_binary(v):
    vot_id = v.id
    vot_title = v.titulo
    vot_desc = v.descripcion
   
    tweet = "Votación: " + v.titulo +"\n"
    tweet += "Descripción: " + v.descripcion +"\n"
    tweet += vot_question + "\n"
    tweet += "\nResultados: \n"
    tweet += "Sí: " +str(VotacionBinaria.Numero_De_Trues(v)) + "\n"
    tweet += "No: " +str(VotacionBinaria.Numero_De_Falses(v)) + "\n"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api.update_status(tweet)

def send_twitter_report_normal(v):
    voting_id = v.id
    voting_title = v.titulo
    voting_desc = v.descripcion
    voting_questions = v.preguntas.all()
    
    tweet = "Votación: " + voting_title +"\n"
    tweet  += "Descripción: " + str(voting_desc) + "\n"
    for question in voting_questions:
        tweet  += question.textoPregunta + "\n"
        if Pregunta.Respuesta_Minima(question) == "None":
            tweet  += "No hay respuestas a esta pregunta \n"
        else:
            tweet  += "Respuesta más baja: " + str(Pregunta.Respuesta_Minima(question)) + "\n"
            tweet  += "Respuesta más alta: " + str(Pregunta.Respuesta_Maxima(question)) + "\n"
            tweet  += "Calificación Media: " + str(Pregunta.Media_De_Las_Respuestas(question)) + "\n\n"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api.update_status(tweet)

def send_twitter_report_preferencia(v):
    voting_id = v.id
    voting_title = v.titulo
    voting_desc = v.descripcion
    voting_questions = v.preguntasPreferencia.all()

    tweet = "Votación: " + voting_title +"\n"
    tweet += "Descripción: " + str(voting_desc) + "\n\n"
    for question in voting_questions:
        tweet += question.textoPregunta + "\n"
        if PreguntaPreferencia.Numero_De_Opciones(question) == 0 :
            tweet += "Sin opciones \n"
        else:
            question_ans = question.opcionesRespuesta.all()
            for ans in question_ans:
                tweet += "- " + ans.nombre_opcion + ": " + str(OpcionRespuesta.Media_Preferencia(ans))+"\n"
    tweet += "\n"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api.update_status(tweet)