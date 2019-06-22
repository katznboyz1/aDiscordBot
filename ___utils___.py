import time, json, datetime
class stdout:
    def generateLogLine(string) -> str:
        newstring = _time.formatTimeString('%month%/%day%/%year% - %hour24%:%minute%:%second% | ')
        newstring += str(string)
        return newstring
    def log(string, printLine = True, logLine = True) -> None:
        line = stdout.generateLogLine(string)
        try:
            if (printLine):
                print (line)
        except Exception as error:
            print ('Error while printing log text: {}'.format(error))
        try:
            if (logLine):
                try:
                    previousContents = str(open(str(_time.formatTimeString('./utils/logs/%month%-%day%-%year%.txt'))).read())
                except:
                    previousContents = ''
                file = open(str(_time.formatTimeString('./utils/logs/%month%-%day%-%year%.txt')), 'w')
                file.write('{}\n{}'.format(previousContents, line))
                file.close()
        except Exception as error:
            print ('Error while writing to log file: {}'.format(error))
        return None
class _time:
    def localtime() -> dict:
        ENDTIMEDICT = {}
        LOCALTIME = time.localtime()
        for partition in range(len(LOCALTIME)):
            if (partition == 0):
                ENDTIMEDICT['year'] = LOCALTIME[partition]
            elif (partition == 1):
                ENDTIMEDICT['month'] = LOCALTIME[partition]
            elif (partition == 2):
                ENDTIMEDICT['day'] = LOCALTIME[partition]
            elif (partition == 3):
                ENDTIMEDICT['hour_24HR'] = LOCALTIME[partition]
                ENDTIMEDICT['hour_12HR'] = int(LOCALTIME[partition])
                if (int(ENDTIMEDICT['hour_24HR'] > 12)):
                    ENDTIMEDICT['hour_12HR'] = int(LOCALTIME[partition]) - 12
                    ENDTIMEDICT['pm/am'] = 'pm'
                else:
                    ENDTIMEDICT['pm/am'] = 'am'
            elif (partition == 4):
                ENDTIMEDICT['minute'] = LOCALTIME[partition]
            elif (partition == 5):
                ENDTIMEDICT['second'] = LOCALTIME[partition]
            elif (partition == 6):
                ENDTIMEDICT['weekday'] = LOCALTIME[partition]
            elif (partition == 7):
                ENDTIMEDICT['yearday'] = LOCALTIME[partition]
            elif (partition == 8):
                ENDTIMEDICT['daylightsavingtime'] = bool(int(LOCALTIME[partition]))
        return ENDTIMEDICT
    def formatTimeString(string) -> str:
        timeNow = _time.localtime()
        if (len(str(timeNow['second'])) == 1):
            timeNow['second'] = '0' + str(timeNow['second'])
        if (len(str(timeNow['minute'])) == 1):
            timeNow['minute'] = '0' + str(timeNow['minute'])
        replaceWith = [
            ['%year%', timeNow['year']],
            ['%month%', timeNow['month']],
            ['%day%', timeNow['day']],
            ['%hour%', timeNow['hour_12HR']],
            ['%hour24%', timeNow['hour_24HR']],
            ['%pm/am%', timeNow['pm/am']],
            ['%minute%', timeNow['minute']],
            ['%second%', timeNow['second']],
            ['%weekday%', timeNow['weekday']],
            ['%yearday%', timeNow['yearday']],
            ['%dst%', timeNow['daylightsavingtime']],
        ]
        for each in range(len(replaceWith)):
            string = string.replace(str(replaceWith[each][0]), str(replaceWith[each][1]))
        return string
    def getDaysSinceUnixEpoch() -> int:
        epoch = datetime.datetime.utcfromtimestamp(0)
        today = datetime.datetime.today()
        distance = today - epoch
        return int(distance.days)
class presets:
    def getManifestData(path = './manifest.json') -> dict:
        return json.loads(str(open(path).read()))