import discord, json, os, random, time
import ___utils___ as localUtilsLib

localUtilsLib.stdout.log('bot.py has started running with PID {}.'.format(str(os.getpid())))

class program:
    bot = discord.Client()
    colors = {
        'success-green':0x00ff22,
        'failure-red':0xe60004,
        'neutral-blue':0x0059ff,
        'surprise-yellow':0xfff700,
    }
    xpValues = {
        'xpPerMessage':15,
        'xpMinAndMaxChanceForLootbox':[50, 1500],
        'dailyCollectAmount':500,
    }

@program.bot.event
async def on_message(message) -> None:
    if (message.author != program.bot.user):
        dataFileContents = {}
        if (str(message.author.id) + '.user.json' in os.listdir('data')):
            try:
                dataFileContents = json.loads(str(open('./data/{}.user.json'.format(str(message.author.id))).read()))
            except Exception as error:
                localUtilsLib.stdout.log('Could not access the user log for {}. Error: ({})'.format(str(message.author.id), str(error)))
        requiredKeys = [
            ['score_global', '0'],
            ['last_daily_collect_timestamp_days_since_unix_epoch', '0'],
        ]
        for key in requiredKeys:
            if (str(key[0]) not in dataFileContents):
                dataFileContents[str(key[0])] = str(key[1])
        dataFileContents['score_global'] = str(int(dataFileContents['score_global']) + int(program.xpValues['xpPerMessage']))


        serverData = {}
        if (str(message.server.id) + '.server.json' in os.listdir('data')):
            try:
                serverData = json.loads(str(open('./data/{}.server.json'.format(str(message.server.id))).read()))
            except Exception as error:
                localUtilsLib.stdout.log('Could not access the server log for {}. Error: ({})'.format(str(message.server.id), str(error)))
        requiredKeys = [
            ['allow_randomlootboxes', '1'],
            ['server_prefix', '<@{}>'.format(program.bot.user.id)],
            ['lingering_lootboxes', '0'],
        ]
        for key in requiredKeys:
            if (str(key[0]) not in serverData):
                serverData[str(key[0])] = str(key[1])
        prefix = str(serverData['server_prefix'])


        randomLootboxInteger = random.randint(0, 200)


        if (message.content.startswith(prefix) or message.content.startswith('<@{}>'.format(program.bot.user.id))):
            localUtilsLib.stdout.log('A user with the ID {} sent me a message.'.format(message.author.id))
            messageHandled = False


            try: #1
                if (message.content.strip() == '<@{}>'.format(program.bot.user.id) and messageHandled == False): #1
                    embed = discord.Embed(title = 'Hello there!', description = '<@{}>, I see that you @ mentioned me. If you would like to see my help menu, then type `@aDiscordBot help` for a website that lists all my commands. If you would like to change my prefix from {} to something else, use my `setprefix` command!'.format(message.author.id, prefix), color = program.colors['neutral-blue'])
                    embed.set_author(name = '{}'.format(program.bot.user.name), icon_url = 'https://raw.githubusercontent.com/katznboyz1/aDiscordBot/master/bot-profile-picture.png')
                    await program.bot.send_message(message.channel, embed = embed)
                    messageHandled = True
            except Exception as error:
                localUtilsLib.stdout.log('Exception occured in (1) while handling <@{}>\'s message: {}'.format(message.author.id, error))


            try: #2
                if (message.content.strip().lower().split(' ')[0:2] == [prefix, 'taskkill'] and messageHandled == False): #(2)
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
                localUtilsLib.stdout.log('Exception occured in (2) while handling <@{}>\'s message: {}'.format(message.author.id, error))


            try: #3
                if (message.content.strip().lower().split(' ')[0:2] == [prefix, 'help'] and messageHandled == False):
                    embed = discord.Embed(title = 'Click here to go to my help page', color = program.colors['neutral-blue'], url = 'https://katznboyz1.github.io/aDiscordBot/commands.html')
                    embed.set_author(name = '{}'.format(program.bot.user.name), icon_url = 'https://raw.githubusercontent.com/katznboyz1/aDiscordBot/master/bot-profile-picture.png')
                    await program.bot.send_message(message.channel, embed = embed)
                    messageHandled = True
            except Exception as error:
                localUtilsLib.stdout.log('Exception occured in (3) while handling <@{}>\'s message: {}'.format(message.author.id, error))


            try: #4
                if (message.content.strip().lower().split(' ')[0:2] == [prefix, 'say'] and messageHandled == False):
                    newMessage = message.content.split(' ')[2:]
                    newNewMessage = ''
                    for each in newMessage:
                        newNewMessage += str(each) + ' '
                    await program.bot.send_message(message.channel, newNewMessage)
                    await program.bot.delete_message(message)
                    messageHandled = True
            except Exception as error:
                localUtilsLib.stdout.log('Exception occured in (4) while handling <@{}>\'s message: {}'.format(message.author.id, error))


            try: #5
                if (message.content.strip().lower().split(' ')[0:2] == [prefix, 'prune'] and messageHandled == False):
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
                localUtilsLib.stdout.log('Exception occured in (5) while handling <@{}>\'s message: {}'.format(message.author.id, error))


            try: #6
                if (message.content.strip().lower().split(' ')[0:2] == [prefix, 'cursedimage'] and messageHandled == False):
                    randomImage = './media/serveTheCycleImages/' + str(random.choice(os.listdir('./media/serveTheCycleImages')))
                    await program.bot.send_file(message.channel, randomImage)
                    messageHandled = True
            except Exception as error:
                localUtilsLib.stdout.log('Exception occured in (6) while handling <@{}>\'s message: {}'.format(message.author.id), error)


            try: #7
                if (message.content.strip().lower().split(' ')[0:2] == [prefix, 'commandhelp'] and messageHandled == False):
                    commandsJsonData = {}
                    commandsJsonData = json.loads(str(open('./commands.json').read()))['commands']
                    commandExists = False
                    commandData = {}
                    for each in commandsJsonData:
                        if (commandsJsonData[each]['commandName'] == message.content.strip().split(' ')[2]):
                            commandExists = True
                            commandData = commandsJsonData[each]
                    if (commandExists):
                        embed = discord.Embed(title = 'Help page for "{}"'.format(message.content.strip().split(' ')[2]), description = 'Command name: {}\nCommand description: {}\nCommand usage: `{}`'.format(commandData['commandName'], commandData['description'], commandData['usage']), color = program.colors['success-green']) 
                        embed.set_author(name = '{}'.format(program.bot.user.name), icon_url = 'https://raw.githubusercontent.com/katznboyz1/aDiscordBot/master/bot-profile-picture.png')
                        await program.bot.send_message(message.channel, embed = embed)
                    else:
                        embed = discord.Embed(title = 'Error', description = 'I was not able to find that command, try using `@aDiscordBot help` to look over the list of commands.', color = program.colors['failure-red'])
                        embed.set_author(name = '{}'.format(program.bot.user.name), icon_url = 'https://raw.githubusercontent.com/katznboyz1/aDiscordBot/master/bot-profile-picture.png')
                        await program.bot.send_message(message.channel, embed = embed)
                    messageHandled = True
            except Exception as error:
                localUtilsLib.stdout.log('Exception occured in (7) while handling <@{}>\'s message: {}'.format(message.author.id, error))


            try: #8
                if (message.content.strip().lower().split(' ')[0:2] == [prefix, 'sheriff'] and messageHandled == False):
                    sheriffTemplate = '''
**Howdy**
.........:cowboy:
.?..?.?
?....?....?
:point_down:.??..:point_down:
......?..?
......?...?
.......:boot:...:boot:
'''.replace('?', message.content.strip().lower().split(' ')[2]).replace('.', ' ')
                    await program.bot.send_message(message.channel, sheriffTemplate)
                    messageHandled = True
            except Exception as error:
                localUtilsLib.stdout.log('Exception occured in (8) while handling <@{}>\'s message: {}'.format(message.author.id), error)


            try: #9
                if (message.content.strip().lower().split(' ')[0:2] == [prefix, 'profile'] and messageHandled == False):
                    wantedProfileId = str(message.author.id)
                    done = False
                    if ('{}.user.json'.format(wantedProfileId) in os.listdir('data')):
                        pass
                    else:
                        embed = discord.Embed(title = 'Error', description = 'You dont seem to be in my record, try sending that message again, it should be fixed by then.', color = program.colors['failure-red'])
                        embed.set_author(name = '{}'.format(program.bot.user.name), icon_url = 'https://raw.githubusercontent.com/katznboyz1/aDiscordBot/master/bot-profile-picture.png')
                        await program.bot.send_message(message.channel, embed = embed)
                        done = True
                    if (not done):
                        embed = discord.Embed(title = 'Here is your profile, {}'.format(message.author.name), description = 'XP: {}'.format(dataFileContents['score_global']), color = program.colors['neutral-blue'])
                        embed.set_author(name = '{}'.format(program.bot.user.name), icon_url = 'https://raw.githubusercontent.com/katznboyz1/aDiscordBot/master/bot-profile-picture.png')
                        await program.bot.send_message(message.channel, embed = embed)
                    messageHandled = True
            except Exception as error:
                localUtilsLib.stdout.log('Exception occured in (9) while handling <@{}>\'s message: {}'.format(message.author.id, error))
            

            try: #10
                if (message.content.strip().lower().split(' ')[0:2] == [prefix, 'setprefix'] and messageHandled == False):
                    finalMessage = {'error':False, 'header':'ooga booga', 'content':'you shouldnt see this text', 'barcolor':'success-green'}
                    if (message.author.permissions_in(message.channel).administrator):
                        pass
                    else:
                        finalMessage['error'] = True
                        finalMessage['header'] = 'Error'
                        finalMessage['content'] = 'You dont have the permissions to use this command. To use this command, you must be a server administrator.'
                        finalMessage['barcolor'] = 'failure-red'
                    newPrefix = str(message.content.strip().lower().split(' ')[2])
                    if (len(newPrefix) <= 25):
                        pass
                    else:
                        finalMessage['error'] = True
                        finalMessage['header'] = 'Error'
                        finalMessage['content'] = 'The prefix must be less than 25 letters long.'
                        finalMessage['barcolor'] = 'failure-red'
                    if (finalMessage['error'] == False):
                        finalMessage['header'] = 'Success!'
                        finalMessage['content'] = 'The prefix for {} has been set to {}.'.format(message.server.name, newPrefix)
                        finalMessage['barcolor'] = 'success-green'
                        serverData['server_prefix'] = str(newPrefix)
                    embed = discord.Embed(title = finalMessage['header'], description = finalMessage['content'], color = program.colors[finalMessage['barcolor']]) 
                    embed.set_author(name = '{}'.format(program.bot.user.name), icon_url = 'https://raw.githubusercontent.com/katznboyz1/aDiscordBot/master/bot-profile-picture.png')
                    await program.bot.send_message(message.channel, embed = embed)
                    messageHandled = True
            except Exception as error:
                localUtilsLib.stdout.log('Exception occured in (10) while handling <@{}>\'s message: {}'.format(message.author.id, error))


            try: #11
                if (message.content.strip().lower().split(' ')[0:2] == [prefix, 'toggledrops'] and messageHandled == False):
                    finalMessage = {'error':False, 'header':'ooga booga', 'content':'you shouldnt see this text', 'barcolor':'success-green'}
                    if (message.author.permissions_in(message.channel).administrator):
                        pass
                    else:
                        finalMessage['error'] = True
                        finalMessage['header'] = 'Error'
                        finalMessage['content'] = 'You dont have the permissions to use this command. To use this command, you must be a server administrator.'
                        finalMessage['barcolor'] = 'failure-red'
                    if (finalMessage['error'] == False):
                        oldState = bool(int(serverData['allow_randomlootboxes']))
                        serverData['allow_randomlootboxes'] = str(int(not oldState))
                        finalMessage['header'] = 'Success!'
                        if (oldState):
                            finalMessage['content'] = 'Lootboxes and other random drops are now disabled on this server.'
                        else:
                            finalMessage['content'] = 'Lootboxes and other random drops are now enabled on this server.'
                        finalMessage['barcolor'] = 'success-green'
                    embed = discord.Embed(title = finalMessage['header'], description = finalMessage['content'], color = program.colors[finalMessage['barcolor']]) 
                    embed.set_author(name = '{}'.format(program.bot.user.name), icon_url = 'https://raw.githubusercontent.com/katznboyz1/aDiscordBot/master/bot-profile-picture.png')
                    await program.bot.send_message(message.channel, embed = embed)
                    messageHandled = True
            except Exception as error:
                localUtilsLib.stdout.log('Exception occured in (11) while handling <@{}>\'s message: {}'.format(message.author.id, error))

            
            try: #12
                if (message.content.strip().lower().split(' ')[0:2] == [prefix, 'dailyxp'] and messageHandled == False):
                    lastDaily = int(dataFileContents['last_daily_collect_timestamp_days_since_unix_epoch'])
                    currentDate = localUtilsLib._time.getDaysSinceUnixEpoch()
                    if (currentDate > lastDaily):
                        embed = discord.Embed(title = 'Daily XP collected', description = 'You have recived {} XP, <@{}>.'.format(program.xpValues['dailyCollectAmount'], message.author.id), color = program.colors['success-green']) 
                        embed.set_author(name = '{}'.format(program.bot.user.name), icon_url = 'https://raw.githubusercontent.com/katznboyz1/aDiscordBot/master/bot-profile-picture.png')
                        await program.bot.send_message(message.channel, embed = embed)
                        dataFileContents['score_global'] = str(int(dataFileContents['score_global']) + program.xpValues['dailyCollectAmount'])
                        dataFileContents['last_daily_collect_timestamp_days_since_unix_epoch'] = str(currentDate)
                    else:
                        embed = discord.Embed(title = 'Failed to collect daily XP', description = 'It hasnt been a day since you last collected your XP, <@{}>!'.format(message.author.id), color = program.colors['failure-red']) 
                        embed.set_author(name = '{}'.format(program.bot.user.name), icon_url = 'https://raw.githubusercontent.com/katznboyz1/aDiscordBot/master/bot-profile-picture.png')
                        await program.bot.send_message(message.channel, embed = embed)
                    messageHandled = True
            except Exception as error:
                localUtilsLib.stdout.log('Exception occured in (12) while handling <@{}>\'s message: {}'.format(message.author.id, error))


            try: #final-1
                if (messageHandled == False):
                    embed = discord.Embed(title = 'Error', description = 'I wasnt able to find that command, <@{}>! Try typing `@aDiscordBot help` for my list of commands.'.format(message.author.id), color = program.colors['failure-red']) 
                    embed.set_author(name = '{}'.format(program.bot.user.name), icon_url = 'https://raw.githubusercontent.com/katznboyz1/aDiscordBot/master/bot-profile-picture.png')
                    await program.bot.send_message(message.channel, embed = embed)
                    messageHandled = True
            except Exception as error:
                localUtilsLib.stdout.log('Exception occured in (final-1) while handling <@{}>\'s message: {}'.format(message.author.id), error)


        if (str(serverData['allow_randomlootboxes']) == '1' and randomLootboxInteger == 1):
            serverData['lingering_lootboxes'] = str(int(serverData['lingering_lootboxes']) + 1)
            embed = discord.Embed(title = 'Woah!', description = 'A lootbox just spawned, type `pickup` to take it. Better be fast before somebody else gets it. Did you know that its only a 1/200 chance that these things spawn!', color = program.colors['surprise-yellow']) 
            embed.set_author(name = '{}'.format(program.bot.user.name), icon_url = 'https://raw.githubusercontent.com/katznboyz1/aDiscordBot/master/bot-profile-picture.png')
            await program.bot.send_message(message.channel, embed = embed)
        if (message.content.strip().lower() == 'pickup' and int(serverData['lingering_lootboxes']) > 0):
            serverData['lingering_lootboxes'] = str(int(serverData['lingering_lootboxes']) - 1)
            amountWon = random.randint(*program.xpValues['xpMinAndMaxChanceForLootbox'])
            embed = discord.Embed(title = '{} was the fastest this time!'.format(message.author.name), description = '<@{}>, you picked up the lootbox first! You picked up {} coins from the box.'.format(message.author.id, amountWon), color = program.colors['surprise-yellow']) 
            embed.set_author(name = '{}'.format(program.bot.user.name), icon_url = 'https://raw.githubusercontent.com/katznboyz1/aDiscordBot/master/bot-profile-picture.png')
            await program.bot.send_message(message.channel, embed = embed)
            dataFileContents['score_global'] = str(int(dataFileContents['score_global']) + amountWon)


        try:
            dataFile = open('./data/{}.user.json'.format(str(message.author.id)), 'w')
            dataFile.write(json.dumps(dataFileContents))
            dataFile.close()
        except Exception as error:
            localUtilsLib.stdout.log('Failed saving user data to file for {}. Error: ({})'.format(message.author.id, error))
        try:
            dataFile = open('./data/{}.server.json'.format(str(message.server.id)), 'w')
            dataFile.write(json.dumps(serverData))
            dataFile.close()
        except Exception as error:
            localUtilsLib.stdout.log('Failed saving server data to file for {}. Error: ({})'.format(message.server.id, error))

@program.bot.event
async def on_ready() -> None:
    localUtilsLib.stdout.log('The bot is online.')
    await program.bot.change_presence(game = discord.Game(name = 'Mmmm. Testing in production I am. Unwise that is.'))

program.bot.run(localUtilsLib.presets.getManifestData()['discord-bot-key'])