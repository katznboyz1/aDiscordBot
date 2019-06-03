import discord, goslate, json, os, PIL.Image, PIL.ImageDraw, PIL.ImageFont, random, time
import ___utils___ as localUtilsLib

localUtilsLib.stdout.log('bot.py has started running.')

class program:
    bot = discord.Client()
    colors = {
        'success-green':0x00ff22,
        'failure-red':0xe60004,
        'neutral-blue':0x0059ff,
    }
    gs = goslate.Goslate()

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
                if (message.content.strip().lower() in ['<@{}> help'.format(program.bot.user.id), '<@{}> help'.format(program.bot.user.id)] and messageHandled == False):
            except Exception as error:
                localUtilsLib.stdout.log('Exception occured in (3) while handling <@{}>\'s message: {}'.format(message.author.id), error)
            '''try: #4
                if (message.content.strip().lower() == '<@{}> senselang'.format(program.bot.user.id) and messageHandled == False):
                    embed = discord.Embed(title = 'Next step for the command:', description = 'Please send the text that you want me to translate here. You have 30 seconds to do so.', color = program.colors['neutral-blue'])
                    embed.set_author(name = '{}'.format(program.bot.user.name), icon_url = 'https://raw.githubusercontent.com/katznboyz1/aDiscordBot/master/bot-profile-picture.png')
                    await program.bot.send_message(message.channel, embed = embed)
                    msg = await program.bot.wait_for_message(timeout = 30, author = message.author)
                    if (msg):
                        embed = discord.Embed(title = 'This may take a little bit', description = 'Due to the amount of users using this feature, this command may take a little bit. Give it about 15 seconds [max].', color = program.colors['neutral-blue'])
                        embed.set_author(name = '{}'.format(program.bot.user.name), icon_url = 'https://raw.githubusercontent.com/katznboyz1/aDiscordBot/master/bot-profile-picture.png')
                        await program.bot.send_message(message.channel, embed = embed)
                        language = program.gs.detect(msg.content)
                        try:
                            success = False
                            for tries in range(3):
                                try:
                                    language = program.gs.get_languages()[language]
                                    success = True
                                    break
                                except:
                                    await time.sleep(5)
                            if (success == False):
                                language = 'error'
                        except:
                            language = 'unknown'
                        embed = discord.Embed(title = 'Success!', description = 'The language used in that message is: {}.'.format(language.lower().capitalize()), color = program.colors['success-green'])
                        embed.set_author(name = '{}'.format(program.bot.user.name), icon_url = 'https://raw.githubusercontent.com/katznboyz1/aDiscordBot/master/bot-profile-picture.png')
                        await program.bot.send_message(message.channel, embed = embed)
                    else:
                        embed = discord.Embed(title = 'Command failed', description = 'The 30 seconds are up <@{}>.'.format(message.author.id), color = program.colors['failure-red'])
                        embed.set_author(name = '{}'.format(program.bot.user.name), icon_url = 'https://raw.githubusercontent.com/katznboyz1/aDiscordBot/master/bot-profile-picture.png')
                        await program.bot.send_message(message.channel, embed = embed)
            except Exception as error:
                localUtilsLib.stdout.log('Exception occured in (4) while handling <@{}>\'s message: {}'.format(message.author.id), error)'''
            

@program.bot.event
async def on_ready() -> None:
    localUtilsLib.stdout.log('The bot is online.')

program.bot.run(localUtilsLib.presets.getManifestData()['discord-bot-key'])