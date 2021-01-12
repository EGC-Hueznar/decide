const Discord = require('discord.js')

module.exports = {
    name: '!help',
    description: 'Help from decide bot',
    execute(msg, args) {

        const exampleEmbed = new Discord.RichEmbed()
        .setColor('#94F9F9')
        .setTitle('Comandos disponibles')
        .setAuthor(msg.author.username, msg.author.avatarURL)
        .setDescription('Estos son los comandos disponibles de decidebot:')
        .setThumbnail('https://avatars3.githubusercontent.com/u/34768613?s=200&v=4')
        .addField(":white_check_mark: | !login", "Inicio de sesión en decide")
        .addField(":wave: | !logout", "Cierre de sesión en decide")
        .addField(":thinking: | !help", "Muestra los comandos de decide")
        .addField(":pencil: | !voting", "Muestra todas las votaciones")
        .addField(":pencil: | !voting [id]", "Muestra las opciones de la votación")
        .addField(":pencil: | !voting [id] [opción]", "Votar la opción seleccionada")
        .setTimestamp()

        msg.reply(exampleEmbed)

    }
}