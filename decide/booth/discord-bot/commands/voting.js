const { MessageCollector, DMChannel } = require("discord.js")
const Discord = require('discord.js')
const utils = require('../utils/utils.js')
const urls = require('../utils/urls.json')
const JSONbig = require("json-bigint") 

module.exports = {

    name: '!voting',
    description: 'Vote in decide',
    async execute(msg, args) {
         
        async function loadVotings (usuarioDecideId) {
            var votings = {} 
            await utils.axiosGet(`${urls.BASE_URL}${urls.CENSUS_VOTINGS_URL}${usuarioDecideId}/`).then(async response => {
                votings = response.data.votings
                await utils.axiosGet(urls.BASE_URL + urls.VOTING_URL, {
                transformResponse: res => JSONbig.parse(res)
                }).then(async response => {
                    votings={votings: response.data.filter(v => votings.includes(v.id) 
                        && v.start_date 
                        && Date.parse(v.start_date) < Date.now() 
                        && !v.end_date)};
                }).catch( error => {
                    console.log(error)
                })
            }).catch( error => {
                console.log(error)
            })
            return votings
        }


        if (utils.getDataFromUser(msg.author.id)){

            if (!(JSON.stringify(utils.getDataFromUser(msg.author.id)) === JSON.stringify({}))){
                
                var len = args.length
                
                var usuarioDecide = utils.getDataFromUser(msg.author.id).decideUser
                var token = utils.getDataFromUser(msg.author.id).token

                if(len === 0) {
                    //Todas las votaciones
                    var lv = await loadVotings(usuarioDecide.id)
                    console.log(lv)

                    const votingEmbed = new Discord.RichEmbed()
                        .setColor('#94F9F9')
                        .setTitle(':pencil: Votaciones disponibles')
                        .setAuthor(msg.author.username, msg.author.avatarURL)
                        .setDescription('**Utiliza !voting [id] para seleccionar votación!** \nEstas son las votaciones en las que estas censado:')
                        .setThumbnail('https://avatars3.githubusercontent.com/u/34768613?s=200&v=4')

                    for (var i = 0; i<lv.votings.length; i++) {
                        votingEmbed.addField(':arrow_right:⠀' + lv.votings[i].id + ' - Nombre: ' + lv.votings[i].name, lv.votings[i].desc)
                    } 
                    
                    votingEmbed.setTimestamp()
                    
                    msg.author.send(votingEmbed)


                }else if (len === 1) {
                    //Votación selecionada
                }else if (len === 2) {
                    //Votar en la vvotacion seleccionada con la opción selecionada
                } else {

                }
                
            } else {
                msg.reply(':grimacing: Prueba a logearte antes')
            }
        } else {
            msg.reply(':grimacing: Prueba a logearte antes')
        }

    }
}

