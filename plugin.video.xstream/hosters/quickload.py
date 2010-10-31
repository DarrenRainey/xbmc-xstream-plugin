from resources.lib.handler.hosterHandler import cHosterHandler

class cHoster:
    def getName(self):
        return 'QuickLoad.to'

    def getPattern(self):
        return '<embed.*?src="([^"]+)"'

    def setUrl(self, sUrl):
        self.__sUrl = sUrl

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        oHosterHandler = cHosterHandler()
        return oHosterHandler.getUrl(self)
