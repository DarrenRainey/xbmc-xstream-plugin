import logger
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.player import cPlayer
from resources.lib.util import cUtil
from resources.lib.gui.contextElement import cContextElement
from resources.lib.download import cDownload

SITE_NAME = 'br_online_de'
URL_MAIN = 'http://www.br-online.de'
URL_CENTAURI = 'http://www.br-online.de/br-alpha/alpha-centauri/alpha-centauri-harald-lesch-videothek-ID1207836664586.xml'

def load():
    logger.info('load br-online.de :)')

    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_CENTAURI)
    __createMenuEntry(oGui, 'showCentauriVideothek', 'Alpha-Centauri', oOutputParameterHandler)
    
    oGui.setEndOfDirectory()

def __createMenuEntry(oGui, sFunction, sLabel, oOutputParameterHandler = ''):
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_NAME)
    oGuiElement.setFunction(sFunction)
    oGuiElement.setTitle(sLabel)
    oGui.addFolder(oGuiElement, oOutputParameterHandler)

def showCentauriVideothek():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    sPattern = '<h3 class="teaserHead">.*?<a href="([^"]+)".*?<img src="([^"]+)".*?<span class="versteckt">(.*?)</span>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_NAME)
            oGuiElement.setFunction('showCentauriMovies')
            oGuiElement.setThumbnail(URL_MAIN + str(aEntry[1]))
            oGuiElement.setTitle(aEntry[2])

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + str(aEntry[0]))
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()
    
def showCentauriMovies():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    
    sPattern = '<h3 class="teaserHead">.*?<a href="([^"]+)".*?<span class="versteckt">(.*?)</span>'
    __showCentauriMovies(oGui, sHtmlContent, sPattern)

    sPattern = '<h3 class="linkPkt">.*?<a href="([^"]+)".*?<span class="versteckt">(.*?)</span>'
    __showCentauriMovies(oGui, sHtmlContent, sPattern)

    oGui.setEndOfDirectory()

def __showCentauriMovies(oGui, sHtmlContent, sPattern):
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_NAME)
            oGuiElement.setFunction('getMovieUrls')
            oGuiElement.setTitle(aEntry[1])

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + str(aEntry[0]))
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

def getMovieUrls():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    sPattern = "player.avaible_url\['microsoftmedia'\]\['1'\] = \"([^\"]+)\""
    __getMovieUrls(oGui, sHtmlContent, sPattern, 'WMV - low Quality')

    sPattern = "player.avaible_url\['microsoftmedia'\]\['2'\] = \"(.*?)\""
    __getMovieUrls(oGui, sHtmlContent, sPattern, 'WMV - high Quality')

    sPattern = "player.avaible_url\['flashmedia'\]\['1'\] = \"(.*?)\""
    __getMovieUrls(oGui, sHtmlContent, sPattern, 'FLASH - low Quality')

    sPattern = "player.avaible_url\['flashmedia'\]\['2'\] = \"(.*?)\""
    __getMovieUrls(oGui, sHtmlContent, sPattern, 'FLASH - high Quality')

    oGui.setEndOfDirectory()

def __getMovieUrls(oGui, sHtmlContent, sPattern, sLabel):
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
  
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_NAME)
            oGuiElement.setFunction('play')
            oGuiElement.setTitle(sLabel)

            oOutputParameterHandler = cOutputParameterHandler()           
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry))

            # download context menu
            oContextElement = cContextElement()
            oContextElement.setTitle('Download')
            oContextElement.setFile(SITE_NAME)
            oContextElement.setFunction('download')
            oOutputParameterHandlerDownload = cOutputParameterHandler()         
            oOutputParameterHandlerDownload.addParameter('siteUrl', str(aEntry))
            oContextElement.setOutputParameterHandler(oOutputParameterHandlerDownload)
            oGuiElement.addContextItem(oContextElement)
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

def play():
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_NAME)
    oGuiElement.setMediaUrl(sUrl)

    oPlayer = cPlayer()
    oPlayer.addItemToPlaylist(oGuiElement)
    oPlayer.startPlayer()
    return

def download():
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    
    cDownload().download(sUrl, 'filename')
    return