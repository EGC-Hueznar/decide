import telegram

def send_telegram_report(voting):
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

    text = "REPORTE DE ESTADO \n\n"
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
    bot.send_message(id, text)
