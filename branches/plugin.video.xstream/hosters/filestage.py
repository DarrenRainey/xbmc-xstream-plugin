from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.util import cUtil

class cHoster:
    def getName(self):
        return 'Filestage.to'

    def getPattern(self):
        return 's1.addVariable\("file","([^"]+)"'

    def setUrl(self, sUrl):
        self.__sUrl = sUrl

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        oHosterHandler = cHosterHandler()
        aResult = oHosterHandler.getUrl(self)
        if (aResult[0] == True):
            return True, cUtil().urlDecode(aResult[1])
        return False
