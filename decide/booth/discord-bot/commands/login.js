const { MessageCollector, DMChannel, MessageEmbed } = require("discord.js");
const utils = require('../utils/utils.js')
const urls = require('../utils/urls.json')

module.exports = {
    name: '!login',
    description: 'Login into decide',
    execute(msg, args) {
        
        var user = ""
        var pass = ""
        var token = ""

        //Usuario
        try {

            //TODO: Comprobar que el usuario ya esta registrado. 
            //TODO: Cancelar conexión con bot.
            //TODO: Si escribes un comando en mitad del proceso de login, cortar conexión o salga mensaje

            msg.author.send('**Introduzca su usuario:**')
            msg.author.createDM().then(dmchannel => {
                const collectorUser = new MessageCollector(dmchannel, m => m.author.id === msg.author.id, {time:25000})    

                var i = 0

                collectorUser.on('collect', msgUser => {

                    if(msgUser.content) {
                        user = msgUser.content
                        i+=1
                    }

                    if (i === 1) {
                        msg.author.send('Usuario recibido :white_check_mark:')
                    }
                    collectorUser.stop()

                    //Contraseña
                    msg.author.send('**Introduzca su contraseña:**');
                    
                    const collectorPass = new MessageCollector(dmchannel, m => m.author.id === msg.author.id, {time:25000})    
        
                    collectorPass.on('collect', msgPass => {
                        
                        if(msgPass.content) {
                            pass = msgPass.content
                            i+=1
                        }
        
                        if (i === 2) {
                            msg.author.send('Contraseña recibida :white_check_mark:')
                            i+=1
                        }        
                        collectorPass.stop()

                        if(i === 3) {
                            msg.author.send('Comprobando... :hourglass_flowing_sand:')
                        }
                    })

                    collectorPass.on('end', () => {

                        utils.axiosPost(urls.BASE_URL + urls.LOGIN_URL, {username:user, password:pass}).then( response => {
                            
                            token = response.data.token
                            console.log('Token -> ' + token)

                            utils.storeData(msg.author.id, {token:token})
                        
                            utils.axiosPost(urls.BASE_URL + urls.GETUSER_URL, {token:token}, token).then( response => {
                                
                                const userData = utils.getDataFromUser(msg.author.id)
                                utils.storeData(msg.author.id, {...userData, decideUser:response.data})

                                msg.author.send('Enhorabuena! Se ha registrado correctamente :sunglasses:')

                            }).catch(error => msg.author.send('Error al intentar encontrar al usuario :pleading_face:'))

                        }).catch(error => msg.author.send('Error en las credenciales :pleading_face:'))
                    })

                })
            })
            
        } catch(error) {
            
            console.log(error)
            
            msg.author.send('Prueba a logearte de nuevo')
        }
    },
};
  