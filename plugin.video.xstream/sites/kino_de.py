from resources.lib.gui.contextElement import cContextElement
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.parser import cParser
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.gui import cGui
from resources.lib.player import cPlayer
from resources.lib.util import cUtil
from resources.lib.download import cDownload
import logger

SITE_NAME = 'kino_de'

URL_MAIN = 'http://www.kino.de'
URL_TRAILERS = 'http://www.kino.de/showroom/trailer/film'
#URL_TRAILERS = 'http://www.kino.de/showroom/trailer/games'



ENTRIES_PER_PAGE = 30

def load():
    logger.info('load kino.de :)')

    oGui = cGui()
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_NAME)
    oGuiElement.setFunction('showTrailers')
    oGuiElement.setTitle('neuste / beste Trailers')
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('sUrl', URL_TRAILERS)
    oGui.addFolder(oGuiElement, oOutputParameterHandler)
       
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_NAME)
    oGuiElement.setFunction('showCharacters')
    oGuiElement.setTitle('Trailers A bis Z')
    oGui.addFolder(oGuiElement)
    oGui.setEndOfDirectory()

def showCharacters():
    oGui = cGui()
    __createCharacters(oGui, 'A')
    __createCharacters(oGui, 'B')
    __createCharacters(oGui, 'C')
    __createCharacters(oGui, 'D')
    __createCharacters(oGui, 'E')
    __createCharacters(oGui, 'F')
    __createCharacters(oGui, 'G')
    __createCharacters(oGui, 'H')
    __createCharacters(oGui, 'I')
    __createCharacters(oGui, 'J')
    __createCharacters(oGui, 'K')
    __createCharacters(oGui, 'L')
    __createCharacters(oGui, 'N')
    __createCharacters(oGui, 'O')
    __createCharacters(oGui, 'Q')
    __createCharacters(oGui, 'R')
    __createCharacters(oGui, 'S')
    __createCharacters(oGui, 'T')
    __createCharacters(oGui, 'U')
    __createCharacters(oGui, 'V')
    __createCharacters(oGui, 'W')
    __createCharacters(oGui, 'X')
    __createCharacters(oGui, 'Y')
    __createCharacters(oGui, 'Z')
    __createCharacters(oGui, '0-9')
    oGui.setEndOfDirectory()

def __createCharacters(oGui, sCharacter):
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_NAME)
    oGuiElement.setFunction('showTrailers')
    oGuiElement.setTitle(sCharacter)

    sUrl = URL_TRAILERS + '/' + str(sCharacter)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('sUrl', sUrl)
    oOutputParameterHandler.addParameter('page', '1')
    oGui.addFolder(oGuiElement, oOutputParameterHandler)

def showTrailers():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('sUrl')):
        sUrl = oInputParameterHandler.getValue('sUrl')
        
        iPage = 0
        if (oInputParameterHandler.exist('page')):
            iPage = oInputParameterHandler.getValue('page')

        sTrailerUrl = sUrl
        if (iPage > 0):
            sTrailerUrl = sTrailerUrl + '/' + str(iPage)

        oRequest = cRequestHandler(sTrailerUrl)
        sHtmlContent = oRequest.request()

        sPattern = '<li class="showroomListItem" title="([^"]+)".+?>.*?<a href="([^"]+)"><img src=\'([^\']+)\'.*?>'

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
             for aEntry in aResult[1]:
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_NAME)
                oGuiElement.setFunction('showTrailerDetails')
                oGuiElement.setTitle(aEntry[0])
                oGuiElement.setThumbnail(aEntry[2])

                sTrailerDetailUrl = URL_MAIN + str(aEntry[1])
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('sUrl', sTrailerDetailUrl)
                oGui.addFolder(oGuiElement, oOutputParameterHandler)

        if (iPage > 0):
            bShowNextButton = __checkForNextPage(iPage, sHtmlContent)
            if (bShowNextButton == True):
                iNextPage = int(iPage) + 1

                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_NAME)
                oGuiElement.setFunction('showTrailers')
                oGuiElement.setTitle('mehr ..')                
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('sUrl', sUrl)
                oOutputParameterHandler.addParameter('page', iNextPage)
                oGui.addFolder(oGuiElement, oOutputParameterHandler)

        oGui.setEndOfDirectory()

def __checkForNextPage(iPage, sHtmlContent):
    sPattern = '<a href=\'.*?\'>(.{1,2})</a></span>    <span class="nextLink">'   

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        iLastPage = aResult[1][0]
        if (int(iPage) < int(iLastPage)):
            return True

    return False
    #<a href='/showroom/trailer/film/A/14'>14</a></span>    <span class="nextLink">

def showTrailerDetails():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('sUrl')):
        sUrl = oInputParameterHandler.getValue('sUrl')

        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()

        sPattern = '<div class="srTrailerListItem .*?">.*?<a href="([^"]+)">.*?<img src="([^"]+)".+?/>.*?<a.+?>(.*?)<br class'

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        if (aResult[0] == True):
            for aEntry in aResult[1]:
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_NAME)
                oGuiElement.setFunction('play')
                sTitle = cUtil().removeHtmlTags(aEntry[2], '')

                sTitle = oParser.replace('[ ]{2,}', ' ', sTitle)                
                oGuiElement.setTitle(sTitle)
                oGuiElement.setThumbnail(aEntry[1])
                
               
                oContextElement = cContextElement()
                oContextElement.setTitle('Download')
                oContextElement.setFile(SITE_NAME)
                oContextElement.setFunction('downloadStreamFile')
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('sUrl', sUrl)
                oOutputParameterHandler.addParameter('sTitle', sTitle)
                oContextElement.setOutputParameterHandler(oOutputParameterHandler)
                oGuiElement.addContextItem(oContextElement)

                sUrl = URL_MAIN + str(aEntry[0])
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('sUrl', sUrl)
                oGui.addFolder(oGuiElement, oOutputParameterHandler)
                

                

    oGui.setEndOfDirectory()

def __getStreamFile(sUrl):
    oRequest = cRequestHandler(sUrl)
    sHtmlContent = oRequest.request()

    sPattern = 'flashvars.initItemXML = "([^"]+)";'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        sXmlFile = aResult[1][0]

        oRequest = cRequestHandler(sXmlFile)
        sHtmlContent = oRequest.request()

        sPattern = '<url>(.*?)</url>'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
            sStreamUrl = aResult[1][0]
            logger.info(sStreamUrl)
            return sStreamUrl

    return False

def downloadStreamFile():
    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('sUrl') and oInputParameterHandler.exist('sTitle')):
        sUrl = oInputParameterHandler.getValue('sUrl')
        sTitle = oInputParameterHandler.getValue('sTitle')

        sStreamUrl = __getStreamFile(sUrl)
        if (sStreamUrl != False):
            cDownload().download(sStreamUrl, sTitle)

def play():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('sUrl')):
        sUrl = oInputParameterHandler.getValue('sUrl')

        sStreamUrl = __getStreamFile(sUrl)
        if (sStreamUrl != False):
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_NAME)
            oGuiElement.setMediaUrl(sStreamUrl)

            oPlayer = cPlayer()
            oPlayer.addItemToPlaylist(oGuiElement)
            oPlayer.startPlayer()
            return
                           
    oGui.setEndOfDirectory()