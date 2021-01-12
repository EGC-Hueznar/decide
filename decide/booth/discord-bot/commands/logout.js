const utils = require('../utils/utils.js')
const urls = require('../utils/urls.json')

module.exports = {
    name: '!logout',
    description: 'Logout from decide',
    execute(msg, args) {

        var token = ""

        try {
            msg.author.send('Cargando... :hourglass_flowing_sand:')
            if(utils.getDataFromUser(msg.author.id)){
                if(JSON.stringify(utils.getDataFromUser(msg.author.id)) === JSON.stringify({})){
                    msg.author.send(':grimacing: Prueba a logearte antes')
                }else{
                    token = utils.getDataFromUser(msg.author.id).token
                    logout_url = urls.BASE_URL + urls.LOGOUT_URL
                    utils.axiosPost(logout_url, {token:token}, token).then( response => {
                        utils.cleanData(msg.author.id)
                        msg.author.send('Sesión cerrada con éxito :wave:')
                    }).catch(error => {
                        msg.author.send(':grimacing: Error en la conexión')
                    })
                }
            }else{
                msg.author.send(':grimacing: Prueba a logearte antes')
            }
        }catch {
            msg.author.send('Error al cerrar sesión')
        }
    }
}