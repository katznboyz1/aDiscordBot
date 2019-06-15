import discord, json, os, PIL.Image, PIL.ImageDraw, PIL.ImageFont, random, time
import ___utils___ as localUtilsLib

localUtilsLib.stdout.log('bot.py has started running with PID {}.'.format(str(os.getpid())))

class program:
    bot = discord.Client()
    colors = {
        'success-green':0x00ff22,
        'failure-red':0xe60004,
        'neutral-blue':0x0059ff,
    }

@program.bot.event
async def on_message(message) -> None:
    if (message.author != program.bot.user):
        if (message.content.startswith('<@{}>'.format(program.bot.user.id))):
            localUtilsLib.stdout.log('A user with the ID {} sent me a message.'.format(message.author.id))
            messageHandled = False
            try:
                if (message.content.strip() == '<@{}>'.format(program.bot.user.id) and messageHandled == False): #1
                    embed = discord.Embed(title = 'Hello there!', description = '<@{}>, I see that you @ mentioned me. If you would like to see my help menu, then type `@aDiscordBot help` for a website that lists all my commands.'.format(message.author.id), color = program.colors['neutral-blue'])
                    embed.set_author(name = '{}'.format(program.bot.user.name), icon_url = 'https://raw.githubusercontent.com/katznboyz1/aDiscordBot/master/bot-profile-picture.png')
                    await program.bot.send_message(message.channel, embed = embed)
            except Exception as error:
                localUtilsLib.stdout.log('Exception occured in (1) while handling <@{}>\'s message: {}'.format(message.author.id), error)
            try: #2
                if (message.content.strip().lower() == '<@{}> taskkill'.format(program.bot.user.id) and messageHandled == False): #(2)
                    if (int(message.author.id) in localUtilsLib.presets.getManifestData()['authorized-bot-admins']):
                        embed = discord.Embed(title = 'Success', description = '<@{}>, the bot was killed.'.format(message.author.id), color = program.colors['success-green'])
                        embed.set_author(name = '{}'.format(program.bot.user.name), icon_url = 'https://raw.githubusercontent.com/katznboyz1/aDiscordBot/master/bot-profile-picture.png')
                        await program.bot.send_message(message.channel, embed = embed)
                        localUtilsLib.stdout.log('Bot was shut off by a user with the ID {}.'.format(message.author.id))
                        os.kill(os.getpid(), os.getppid())
                    else:
                        embed = discord.Embed(title = 'Invalid Command', description = '<@{}>, you dont have the permission to preform that command.'.format(message.author.id), color = program.colors['failure-red'])
                        embed.set_author(name = '{}'.format(program.bot.user.name), icon_url = 'https://raw.githubusercontent.com/katznboyz1/aDiscordBot/master/bot-profile-picture.png')
                        await program.bot.send_message(message.channel, embed = embed)
                    messageHandled = True
            except Exception as error:
                localUtilsLib.stdout.log('Exception occured in (2) while handling <@{}>\'s message: {}'.format(message.author.id), error)
            try: #3
                if (message.content.strip().lower() == '<@{}> help'.format(program.bot.user.id) and messageHandled == False):
                    embed = discord.Embed(title = 'Click here to go to my help page', color = program.colors['neutral-blue'], url = 'https://katznboyz1.github.io/aDiscordBot/commands.html')
                    embed.set_author(name = '{}'.format(program.bot.user.name), icon_url = 'https://raw.githubusercontent.com/katznboyz1/aDiscordBot/master/bot-profile-picture.png')
                    await program.bot.send_message(message.channel, embed = embed)
                    messageHandled = True
            except Exception as error:
                localUtilsLib.stdout.log('Exception occured in (3) while handling <@{}>\'s message: {}'.format(message.author.id), error)
            try: #4
                if (message.content.strip().lower().split(' ')[0:2] == ['<@{}>'.format(program.bot.user.id), 'say'] and messageHandled == False):
                    newMessage = message.content.split(' ')[2:]
                    newNewMessage = ''
                    for each in newMessage:
                        newNewMessage += str(each) + ' '
                    await program.bot.send_message(message.channel, newNewMessage)
                    await program.bot.delete_message(message)
                    messageHandled = True
            except Exception as error:
                localUtilsLib.stdout.log('Exception occured in (4) while handling <@{}>\'s message: {}'.format(message.author.id), error)
            try: #5
                if (message.content.strip().lower().split(' ')[0:2] == ['<@{}>'.format(program.bot.user.id), 'prune'] and messageHandled == False):
                    pruneAmount = message.content.split(' ')[2]
                    integerConversionSuccess = False
                    integerConversionError = 'No error provided.'
                    try:
                        pruneAmount = int(pruneAmount)
                        integerConversionSuccess = True
                        if (pruneAmount > 0 and pruneAmount < 91):
                            pass
                        else:
                            integerConversionSuccess = False
                            integerConversionError = 'The amount of messages you wanted me to delete was too large. You said to delete {} messages but I can only delete 90 at a time.'.format(pruneAmount)
                        if (message.author.permissions_in(message.channel).administrator):
                            pass
                        else:
                            integerConversionSuccess = False
                            integerConversionError = 'You must be a server administrator to use this command.'
                    except ValueError:
                        integerConversionError = 'The amount of messages you wanted me to delete was not a valid number.'
                    if (integerConversionSuccess == False):
                        embed = discord.Embed(title = 'Error', description = integerConversionError, color = program.colors['failure-red'])
                        embed.set_author(name = '{}'.format(program.bot.user.name), icon_url = 'https://raw.githubusercontent.com/katznboyz1/aDiscordBot/master/bot-profile-picture.png')
                        await program.bot.send_message(message.channel, embed = embed)
                    else:
                        async for messages in program.bot.logs_from(message.channel, limit = (pruneAmount + 1)):
                            await program.bot.delete_message(messages)
                    messageHandled = True
            except Exception as error:
                localUtilsLib.stdout.log('Exception occured in (5) while handling <@{}>\'s message: {}'.format(message.author.id), error)

@program.bot.event
async def on_ready() -> None:
    localUtilsLib.stdout.log('The bot is online.')

program.bot.run(localUtilsLib.presets.getManifestData()['discord-bot-key'])