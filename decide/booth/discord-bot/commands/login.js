const { MessageCollector, DMChannel } = require("discord.js");


module.exports = {
    name: '!login',
    description: 'Login into decide',
    execute(msg, args) {
        
        var user = ""
        var pass = ""

        //Usuario
        try {
            msg.author.send('Introduzca su usuario')
            msg.author.createDM().then(dmchannel => {
                const collectorUser = new MessageCollector(dmchannel, m => m.author.id === msg.author.id, {time:25000})    

                var i = 0

                collectorUser.on('collect', msgUser => {
                    
                    if(msgUser.content) {
                        user = msgUser.content
                        i+=1
                    }
                    
                    console.log(user)

                    if (i === 1) {
                        msg.author.send('Usuario recibido')
                    }
                    collectorUser.stop()

                    //Contraseña
                    msg.author.send('Introduzca su contraseña');
                    
                    const collectorPass = new MessageCollector(dmchannel, m => m.author.id === msg.author.id, {time:25000})    
        
                    collectorPass.on('collect', msgPass => {
                        
                        if(msgPass.content) {
                            pass = msgPass.content
                            i+=1
                        }
                        
                        console.log(pass)
        
                        if (i === 2) {
                            msg.author.send('Contraseña recibida')
                            i+=1
                        }        
                        collectorPass.stop()

                        if(i === 3) {
                            msg.author.send('Datos introducidos correctamente')
                        }
                    })
                    collectorPass.on('end', () => {
                        msg.author.send('Tiempo expirado. Conexión cerrada')
                    })
                })
                collectorUser.on('end', () => {
                    msg.author.send('Tiempo expirado. Conexión cerrada')
                })
            })

        } catch {
            channel.send('Prueba a logearte de nuevo')
        }
    },
};
  