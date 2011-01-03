import logger
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.player import cPlayer
from resources.lib.util import cUtil

SITE_NAME = 'anime_stream24_com'
URL_MAIN = 'http://www.anime-stream24.com'

def load():
    logger.info('load anime-stream24.com :)')

    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN)
    __createMenuEntry(oGui, 'showAnimesAlphabetic', 'Animes von A - Z', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN)
    __createMenuEntry(oGui, 'showCurrentMovies', 'Aktuelle Anime Folgen', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def __createMenuEntry(oGui, sFunction, sLabel, oOutputParameterHandler = ''):
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_NAME)
    oGuiElement.setFunction(sFunction)
    oGuiElement.setTitle(sLabel)
    oGui.addFolder(oGuiElement, oOutputParameterHandler)

def showCurrentMovies():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    sPattern = '<h2>Aktuelle Anime Folgen</h2>(.*?)</ul>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        sHtmlContent = aResult[1][0]

        sPattern = "<a href='([^']+)'>(.*?)<"
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            for aEntry in aResult[1]:
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_NAME)
                oGuiElement.setFunction('showHosters')
                oGuiElement.setTitle(str(aEntry[1]))

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
                oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showAnimesAlphabetic():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    sPattern = '<h2>Animes von A - Z</h2>(.*?)</select>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        sHtmlContent = aResult[1][0]

        sPattern = "<option value='([^']+)'>(.*?)<"
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            for aEntry in aResult[1]:
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_NAME)
                oGuiElement.setFunction('showMovieTitles')
                oGuiElement.setTitle(str(aEntry[1]))

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
                oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovieTitles():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
        
    sUrl = sUrl.replace(' ', '%20').replace(':', '%3A').replace('+', '%2B')
    sUrl = sUrl.replace('http%3A//', 'http://')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    sPattern = "<h3 class='title-only'><a href='([^']+)'>(.*?)</a></h3>"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_NAME)
            oGuiElement.setFunction('showHosters')
            oGuiElement.setTitle(str(aEntry[1]))

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

    sNextPage = __checkForNextPage(sHtmlContent)
    if (sNextPage != False):       
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_NAME)
        oGuiElement.setFunction('showMovieTitles')
        oGuiElement.setTitle('next ..')

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sNextPage)
        oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = "<a class='blog-pager-older-link' href='([^']+)'"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    sPattern = "<h3 class='post-title entry-title'>(.*?)<div style='clear: both;'></div>"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        sHtmlContent = aResult[1][0]
        sHtmlContent = str(sHtmlContent).lower()

        sPattern = "src=([^ ]+) "
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            for aEntry in aResult[1]:
                sHosterUrl = str(aEntry).replace("'", '').replace('"', '')
                aHoster = __checkHoster(sHosterUrl)

                sHosterName = aHoster[0]
                sHosterPluginName = aHoster[1]

                if (sHosterName != False):
                    oGuiElement = cGuiElement()
                    oGuiElement.setSiteName(SITE_NAME)
                    oGuiElement.setFunction('play')
                    oGuiElement.setTitle(sHosterName)

                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('siteUrl', sHosterUrl)
                    oOutputParameterHandler.addParameter('sHosterFileName', sHosterPluginName)

                    oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def __checkHoster(sHosterUrl):    
    if (sHosterUrl.startswith('http://embed.novamov.com/')):
        return 'novamov', 'novamov'

    if (sHosterUrl.startswith('http://embed.divxstage.net/')):
        return 'divxstage', 'divxstage'

    if (sHosterUrl.startswith('http://www.filestage.to/')):
        return 'filestage', 'filestage'

    if (sHosterUrl.startswith('http://www.vidxden.com/')):
        return 'vidxden', 'vidxden'

    if (sHosterUrl.startswith('http://www.vidbux.com/')):
        return 'vidbux', 'vidbux'

    if (sHosterUrl.startswith('http://www.megavideo.com/')):
        return 'megavideo', 'megavideo'

    if (sHosterUrl.startswith('http://www.dankfile.com/')):
        return 'dankfile', 'dankfile'

    return False, False

def play():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sHosterFileName = oInputParameterHandler.getValue('sHosterFileName')

    #try:
    exec "from " + sHosterFileName + " import cHoster"
    oHoster = cHoster()
    oHoster.setUrl(sUrl)
    aLink = oHoster.getMediaLink()
    if (aLink[0] == True):
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_NAME)
        oGuiElement.setMediaUrl(aLink[1])

        oPlayer = cPlayer()
        oPlayer.addItemToPlaylist(oGuiElement)
        oPlayer.startPlayer()
        return

    #except:
    #    logger.fatal('could not load plugin: ' + sHosterFileName)

    oGui.setEndOfDirectory()
    