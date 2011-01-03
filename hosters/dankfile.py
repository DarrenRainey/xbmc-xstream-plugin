from resources.lib.jsunpacker import cJsUnpacker
from resources.lib.parser import cParser
from resources.lib.handler.requestHandler import cRequestHandler

class cHoster:
    def getName(self):
        return 'dankfile.com'

    def getPattern(self):
        return ""

    def setUrl(self, sUrl):
        self.__sUrl = sUrl

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()

        return self.__getUrlFromJavascriptCode(sHtmlContent)

    def __getUrlFromJavascriptCode(self, sHtmlContent):
        sPattern = "<script type='text/javascript'>eval.*?return p}\((.*?)</script>"
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
            sJavascript = aResult[1][0]

            sUnpacked = cJsUnpacker().unpackByString(sJavascript)
            sPattern = ".addVariable\('file','([^']+)'"
            oParser = cParser()
            aResultLink = oParser.parse(sUnpacked, sPattern)
            
            if (aResultLink[0] == True):
                aResult = []
                aResult.append(True)
                aResult.append(aResultLink[1][0])
                return aResult

        return False

