from hosters.hoster import iHoster
from resources.lib.handler.hosterHandler import cHosterHandler

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Stream File'

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName

    def getPluginIdentifier(self):
        return 'asx'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return 'mms://(.*?)"'

    def setUrl(self, sUrl):
        self.__sUrl = sUrl

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):        
        oHosterHandler = cHosterHandler()
        aResult = oHosterHandler.getUrl(self)
        print aResult
        if (aResult[0] == True):
            return True, 'mms://' + aResult[1]
        return False, ''