
class cHoster:
    def getName(self):
        return 'Loaded.it'

    def getPattern(self):
        return ""

    def setUrl(self, sUrl):
        self.__sUrl = sUrl

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        sUrl = self.__sUrl.replace('/show/', '/get/')

        aResult = []
        aResult.append(True)
        aResult.append(sUrl)
        return aResult