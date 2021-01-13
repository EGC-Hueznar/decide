const { MessageCollector, DMChannel } = require("discord.js")
const Discord = require('discord.js')
const utils = require('../utils/utils.js')
const urls = require('../utils/urls.json')
const JSONbig = require("json-bigint") 
const {BigInt} = require("../crypto/BigInt.js")
const {ElGamal} = require("../crypto/ElGamal.js")

module.exports = {

    name: '!voting',
    description: 'Vote in decide',
    async execute(msg, args) {

        var cleanedOptions = []


        async function loadVotings (usuarioDecideId) {
            var votings = {} 
            await utils.axiosGet(`${urls.BASE_URL}${urls.CENSUS_VOTINGS_URL}${usuarioDecideId}/`).then(async response => {
                votings = response.data.votings
                await utils.axiosGet(urls.BASE_URL + urls.VOTING_URL).then(async response => {
                    votings={votings: response.data.filter(v => votings.includes(v.id) 
                        && v.start_date 
                        && Date.parse(v.start_date) < Date.now() 
                        && !v.end_date)};
                }).catch( error => {
                    msg.reply('Error al cargar votaciones')
                })
            }).catch( error => {
                msg.reply('Error al cargar votaciones')
            })
            return votings
        }

        async function loadOptions (voting) {
            cleanedOptions = voting.question.options.map(opt => ({
            label: opt.option,
            value: opt.number
        }))
            return cleanedOptions
        }

        async function handleSubmit (selected, voting, user, token) {
            try{
                const vote = encrypt(voting, selected);
                const data = {
                    vote: {a: vote.alpha.toString(), b: vote.beta.toString()},
                    voting: voting.id,
                    voter: user.id,
                    token: token
                };
                send(data);
                msg.reply('Ha votado correctamente')
            }catch(error) {
                msg.reply(':x: Error en la votación')
            }
        }
        

        async function send (data) {
            utils.axiosPost(urls.BASE_URL+urls.STORE_URL, data, data.token)
                .then(response => {
                    
                })
                .catch(error => {
                    msg.reply(':x: Error en la votación')
                });
        }

        encrypt = (voting, selected) =>  {
            var bigpk = {
                p: BigInt.fromJSONObject(voting.pub_key.p.toString()),
                g: BigInt.fromJSONObject(voting.pub_key.g.toString()),
                y: BigInt.fromJSONObject(voting.pub_key.y.toString()),
            }
            const bigmsg = BigInt.fromJSONObject(selected.toString());
            const cipher = ElGamal.encrypt(bigpk, bigmsg);
            return cipher;
        }

        if (utils.getDataFromUser(msg.author.id)){

            if (!(JSON.stringify(utils.getDataFromUser(msg.author.id)) === JSON.stringify({}))){
                
                var len = args.length
                
                var usuarioDecide = utils.getDataFromUser(msg.author.id).decideUser
                var token = utils.getDataFromUser(msg.author.id).token
                var lv = await loadVotings(usuarioDecide.id)
                var votingSelected = {}

                if(len === 0) {
                    //Si se escribe !voting muestra las votaciones disponibles

                    const votingEmbed = new Discord.RichEmbed()
                        .setColor('#94F9F9')
                        .setTitle(':pencil: Votaciones disponibles')
                        .setAuthor(msg.author.username, msg.author.avatarURL)
                        .setDescription('**Utiliza !voting [id] para seleccionar votación!** \nEstas son las votaciones en las que estas censado:')
                        .setThumbnail('https://avatars3.githubusercontent.com/u/34768613?s=200&v=4')

                    for (var i = 0; i<lv.votings.length; i++) {
                        if(lv.votings[i].desc != ''){
                            votingEmbed.addField(':arrow_right:⠀' + lv.votings[i].id + ' - Nombre: ' + lv.votings[i].name, lv.votings[i].desc)
                        }else{
                            votingEmbed.addField(':arrow_right:⠀' + lv.votings[i].id + ' - Nombre: ' + lv.votings[i].name, 'No hay descripción')
                        }
                    } 
                    
                    votingEmbed.setTimestamp()
                    
                    msg.author.send(votingEmbed)


                }else if (len === 1) {
                    //Si !voting [número] muestra las opciones de la pregunta
                    idVoting = args[0]
                    select = false
                    for (var j = 0; j<lv.votings.length; j++){
                        if(JSON.stringify(lv.votings[j].id) === idVoting){
                            select = true
                            votingSelected = lv.votings[j]
                            var opciones = await loadOptions(votingSelected)
                            const optionEmbed = new Discord.RichEmbed()
                                .setColor('#94F9F9')
                                .setTitle(':pencil: Opciones de la votación '+votingSelected.name)
                                .setAuthor(msg.author.username, msg.author.avatarURL)
                                .setDescription('**Utiliza !voting ['+JSON.stringify(votingSelected.id)+'] [id opción deseada]' +' para seleccionar opción!** \nEstas son las opciones que puedes seleccionar:')
                                .setThumbnail('https://avatars3.githubusercontent.com/u/34768613?s=200&v=4')
                            for (var z = 0; z<opciones.length; z++) {
                                    optionEmbed.addField(':arrow_right:⠀' + opciones[z].value + ' - ' + opciones[z].label, '⠀')
                            } 
                            optionEmbed.setTimestamp()
                            
                            msg.author.send(optionEmbed)
                            break
                        }
                    }
                    if(select != true){
                        msg.reply(':x: La id introducida no pertenece a ninguna votación')
                    }

                }else if (len === 2) {
                    //Si !voting [número] [número] vota
                    idVoting = args[0]
                    idSelected = args[1]
                    select = false
                    for (var j = 0; j<lv.votings.length; j++){
                        if(JSON.stringify(lv.votings[j].id) === idVoting){
                            select = true
                            votingSelected = lv.votings[j]
                            var opciones = await loadOptions(votingSelected)
                            selectOpt = false
                            for (var z = 0; z<opciones.length; z++){
                                if(JSON.stringify(opciones[z].value) === idSelected){
                                    selectOpt = true
                                    selected = opciones[z].value
                                    handleSubmit(selected, votingSelected, usuarioDecide, token)
                                    break
                                }
                            }
                            if(selectOpt != true){
                                msg.reply(':x: No existe esa opción')
                            } 
                            break
                        }
                }if(select != true){
                        msg.reply(':x: La id introducida no pertenece a ninguna votación')
                    }

                } else {
                    msg.reply(':x: Mensaje no reconocido')
                }
                
            } else {
                msg.reply(':grimacing: Prueba a logearte antes')
            }
        } else {
            msg.reply(':grimacing: Prueba a logearte antes')
        }

    }
}

