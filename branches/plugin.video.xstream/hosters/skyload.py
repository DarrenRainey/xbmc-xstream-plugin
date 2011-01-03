from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser

class cHoster:
    def getName(self):
        return 'SklyLoad.net'

    def getPattern(self):
        return "<param name='src' value='(.*?)'";

    def setUrl(self, sUrl):
        self.__sUrl = sUrl

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()
        sPattern = 'var targetURL="([^"]+)"'

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        print(aResult)
        if (aResult[0] == True):
            self.__sUrl = aResult[1][0]
            print(self.__sUrl)
           
            oHosterHandler = cHosterHandler()
            return oHosterHandler.getUrl(self)

        return False, aResult



