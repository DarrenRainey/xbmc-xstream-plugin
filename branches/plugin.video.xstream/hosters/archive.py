from resources.lib.handler.hosterHandler import cHosterHandler

class cHoster:
    def getName(self):
        return 'Archive.to'

    def getPattern(self):
        return '<a href="([^"]+)">Download</a></b>'

    def setUrl(self, sUrl):
        self.__sUrl = sUrl

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        oHosterHandler = cHosterHandler()
        aUrl = oHosterHandler.getUrl(self)
        
        if (aUrl[0] == True):
            return True, str(aUrl[1]).replace(':80', '')

        return aUrl