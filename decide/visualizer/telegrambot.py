import telegram
from voting.models import *

# Envio de reporte desde una voting con formato json
def send_telegram_report_json(voting):
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

    options = voting.get('question').get('options')
    post = voting.get('postproc')

    text = "REPORTE DE ESTADO VOTING\n\n"
    text += "Votación: " + str(voting_id) + " - " + voting_name +"\n"
    text += "Estado: " + status + "\n"
    text += "Descripción: " + voting_desc + "\n\n"
    if voting_tally is None:
        text += "Pregunta: " + voting_q + "\n"
        for option in options:
            text += "Opción " + str(option.get('number')) + " - " + option.get('option') + "\n"
        text += "\nEsperando el resultado del recuento"
    else:
        text += "Pregunta: " + voting_q + "\n"
        for option in post:
            text += "Opción " + str(option.get('number')) + " - " + option.get('option') + " - " + str(option.get('votes')) + " votos \n"
        text += "\nResultados de la Votación: \n"
        for option in post:
            text += option.get('option') + " - " + str(option.get('postproc')) + "\n"
      
    bot_token = '1415070510:AAE49OJPu4viYNo5Tfov4vzkoIyeNf_JBr4'
    bot = telegram.Bot(bot_token)
    id = -1001318632551
    return bot.send_message(id, text)
# Selector de tipos de votación   
def send_telegram_report(voting):
    if isinstance(voting,VotacionBinaria):
        message = send_telegram_report_binary(voting)
    elif isinstance(voting,Voting):
        message = send_telegram_report_voting(voting)
    elif isinstance(voting,Votacion):
        message = send_telegram_report_normal(voting)
    elif isinstance(voting,VotacionPreferencia):
        message = send_telegram_report_preferencia(voting)
    elif isinstance(voting,VotacionMultiple):
        message = send_telegram_report_mult(voting)
    return message
# Envío de reporte desde un objeto voting
def send_telegram_report_voting(voting):
        voting_id = voting.id
        voting_name = voting.name
        voting_desc = voting.desc
        voting_q = voting.question
        voting_start = voting.start_date
        voting_end = voting.end_date
        voting_tally = voting.tally

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
        if voting_tally is None:
            text += "Pregunta: " + str(voting_q) + "\n"
            for option in options:
                text += "Opción " + str(option.number) + " - " + option.option+ "\n"
            if voting_end is not None:
                text += "\nEsperando el resultado del recuento"
        else:
            text += "Pregunta: " + str(voting_q) + "\n"
            for option in post:
                text += "Opción " + str(option.get('number')) + " - " + option.get('option') + " - " + str(option.get('votes')) + " votos \n"
            text += "\nResultados de la Votación: \n"
            for option in post:
                text += option.get('option') + " - " + str(option.get('postproc')) + "\n"
        
        bot_token = '1415070510:AAE49OJPu4viYNo5Tfov4vzkoIyeNf_JBr4'
        bot = telegram.Bot(bot_token)
        id = -1001318632551
        return bot.send_message(id, text)

# Envío de reporte desde un objeto Votación Binaria
def send_telegram_report_binary(v):
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
    bot_token = '1415070510:AAE49OJPu4viYNo5Tfov4vzkoIyeNf_JBr4'
    bot = telegram.Bot(bot_token)
    id = -1001318632551
    return bot.send_message(id,text)

# Envío de reporte desde un objeto Votación Normal
def send_telegram_report_normal(v):
    voting_id = v.id
    voting_title = v.titulo
    voting_desc = v.descripcion
    voting_start = v.fecha_inicio
    voting_end = v.fecha_fin
    voting_questions = v.preguntas.all()
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
    text = "REPORTE DE ESTADO VOTACIÓN NORMAL\n\n"
    text += "Votación: " + str(voting_id) + " - " + voting_title +"\n"
    text += "Estado: " + status + "\n"
    text += "Descripción: " + str(voting_desc) + "\n\n"
    for question in voting_questions:
        text += question.textoPregunta + "\n"
        if Pregunta.Respuesta_Minima(question) == "None":
            text += "No hay respuestas a esta pregunta \n\n"
        else:
            text += "Respuesta más baja: " + str(Pregunta.Respuesta_Minima(question)) + "\n"
            text += "Respuesta más alta: " + str(Pregunta.Respuesta_Maxima(question)) + "\n"
            text += "Calificación Media: " + str(Pregunta.Media_De_Las_Respuestas(question)) + "\n\n"

    bot_token = '1415070510:AAE49OJPu4viYNo5Tfov4vzkoIyeNf_JBr4'
    bot = telegram.Bot(bot_token)
    id = -1001318632551
    return bot.send_message(id,text)

# Envío de reporte desde un objeto Votación Preferencia
def send_telegram_report_preferencia(v):
    voting_id = v.id
    voting_title = v.titulo
    voting_desc = v.descripcion
    voting_start = v.fecha_inicio
    voting_end = v.fecha_fin
    voting_questions = v.preguntasPreferencia.all()
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
    text = "REPORTE DE ESTADO VOTACIÓN PREFERENCIA\n\n"
    text += "Votación: " + str(voting_id) + " - " + voting_title +"\n"
    text += "Estado: " + status + "\n"
    text += "Descripción: " + str(voting_desc) + "\n\n"
    for question in voting_questions:
        text += question.textoPregunta + "\n"
        if PreguntaPreferencia.Numero_De_Opciones(question) == 0 :
            text += "No hay opciones para esta pregunta \n"
        else:
            question_ans = question.opcionesRespuesta.all()
            for ans in question_ans:
                text += "- " + ans.nombre_opcion + ": " + str(OpcionRespuesta.Media_Preferencia(ans))+"\n"
        text += "\n"
        
    bot_token = '1415070510:AAE49OJPu4viYNo5Tfov4vzkoIyeNf_JBr4'
    bot = telegram.Bot(bot_token)
    id = -1001318632551
    return bot.send_message(id,text)

# Envío de reporte desde un objeto Votación Multiple
def send_telegram_report_mult(v):
    voting_id = v.id
    voting_title = v.titulo
    voting_desc = v.descripcion
    voting_start = v.fecha_inicio
    voting_end = v.fecha_fin
    voting_questions = v.preguntasMultiples.all()
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
    text = "REPORTE DE ESTADO VOTACIÓN MÚLTIPLE\n\n"
    text += "Votación: " + str(voting_id) + " - " + voting_title +"\n"
    text += "Estado: " + status + "\n"
    text += "Descripción: " + str(voting_desc) + "\n\n"
    for question in voting_questions:
        text += question.textoPregunta + "\n"
        if PreguntaMultiple.Numero_De_Opciones(question) == 0 :
            text += "No hay opciones para esta pregunta \n"
        else:
            question_ans = question.opcionesMultiples.all()
            for ans in question_ans:
                text += "- " + ans.nombre_opcion + ": " + str(ans.n_votado)+"\n"
        text += "\n"
        
    bot_token = '1415070510:AAE49OJPu4viYNo5Tfov4vzkoIyeNf_JBr4'
    bot = telegram.Bot(bot_token)
    id = -1001318632551
    return bot.send_message(id,text)