import urllib
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

SITE_NAME = 'iload_to'
URL_MAIN = 'http://iload.to'
URL_MOVIE_PAGE = 'http://iload.to/category/1-Filme/'
URL_CHARACTERS = 'http://iload.to/category/1-Filme/letter'
URL_SEARCH = 'http://iload.to/ajax/module/category/1-Filme/search/'

def load():
    logger.info('load iloadto :)')

    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_CHARACTERS)
    __createMenuEntry(oGui, 'showCharacters', 'Filme', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN)
    __createMenuEntry(oGui, 'showCinemaMovies', 'aktuelle KinoFilme', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MOVIE_PAGE)    
    __createMenuEntry(oGui, 'displayGenre', 'Genre', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH)    
    __createMenuEntry(oGui, 'displaySearch', 'Suche', oOutputParameterHandler)
    
    oGui.setEndOfDirectory()

def __createMenuEntry(oGui, sFunction, sLabel, oOutputParameterHandler = ''):
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_NAME)
    oGuiElement.setFunction(sFunction)
    oGuiElement.setTitle(sLabel)
    oGui.addFolder(oGuiElement, oOutputParameterHandler)

def showCharacters():
    oGui = cGui()
    __createCharacters(oGui, '#')
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
    
    oGui.setEndOfDirectory()

def __createCharacters(oGui, sCharacter):
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_NAME)
    oGuiElement.setFunction('showMovies')
    oGuiElement.setTitle(sCharacter)

    if (sCharacter == '#'):
        sCharacter = '_'

    sUrl = URL_CHARACTERS + '/' + str(sCharacter) + '/'

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oOutputParameterHandler.addParameter('page', '1')
    oGui.addFolder(oGuiElement, oOutputParameterHandler)

def displaySearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):

        sSearchText = sSearchText.replace(' ', '+')
        sUrl = URL_SEARCH + str(sSearchText) + '/'
        __showMovies(sUrl, 1)
        return

    oGui.setEndOfDirectory()

def displayGenre():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    sPattern = '<a href="([^"]+)" class="next level3">.*?<div>(.*?)</div>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_NAME)
            oGuiElement.setFunction('showMovies')
            oGuiElement.setTitle(aEntry[1])

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('page', '1')
            oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + str(aEntry[0]))            
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()



def showMovies():
    oInputParameterHandler = cInputParameterHandler()
    sSiteUrl = oInputParameterHandler.getValue('siteUrl')
    iPage = oInputParameterHandler.getValue('page')
    __showMovies(sSiteUrl, iPage)
    

def __showMovies(sSiteUrl, iPage):
    oGui = cGui()

    sUrl = str(sSiteUrl) + str('page/') + str(iPage)
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = str(sHtmlContent).replace('\\', '')

    sPattern = '<table class="row">.*?class="list-cover".*?<img src="([^"]+)">.*?class="list-name".*?<a href="([^"]+)".*?>(.*?)</a>.*?class="description".*?>(.*?)</td>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_NAME)
            oGuiElement.setFunction('showRelease')
            oGuiElement.setTitle(cUtil().removeHtmlTags(aEntry[2]))
            oGuiElement.setThumbnail(aEntry[0])
            oGuiElement.setDescription(aEntry[3])

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('movieUrl', URL_MAIN + str(aEntry[1]))
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

    sNextUrl = __checkForNextPage(sHtmlContent, iPage)
    if (sNextUrl != False):
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_NAME)
        oGuiElement.setFunction('showMovies')
        oGuiElement.setTitle('next ..')

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sSiteUrl)
        oOutputParameterHandler.addParameter('page', int(iPage) + 1)
        oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent, iCurrentPage):
    iNextPage = int(iCurrentPage) + 1
    iNextPage = str(iNextPage)

    sPattern = '<a href=".*?/page/' + iNextPage + '/">(.*?)</a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return True
    return False


def showCinemaMovies():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    sPattern = '<div class="toptitle-slider-content"(.*?)</div>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntryHtml in aResult[1]:
            sPattern = '<a href="([^"]+)"><img src="([^"]+)".*?data-tooltip="([^"]+)"'
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)

            if (aResult[0] == True):
                for aEntry in aResult[1]:
                    oGuiElement = cGuiElement()
                    oGuiElement.setSiteName(SITE_NAME)
                    oGuiElement.setFunction('showRelease')
                    oGuiElement.setTitle(cUtil().removeHtmlTags(aEntry[2]))
                    oGuiElement.setThumbnail(aEntry[1])
                  
                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('movieUrl', URL_MAIN + str(aEntry[0]))
                    oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showRelease():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('movieUrl')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    sPattern = '<table class="release-list">(.*?)</table>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntryHtml in aResult[1]:
            sPattern = '<tr class="row">.*?<a href="([^"]+)">(.*?)</a>.*?class="countryflag".*?alt="([^"]+)".*?class="release-types">(.*?)</td>'
            oParser = cParser()
            aResult = oParser.parse(aEntryHtml, sPattern)

            if (aResult[0] == True):
                for aEntry in aResult[1]:

                    oGuiElement = cGuiElement()
                    oGuiElement.setSiteName(SITE_NAME)
                    oGuiElement.setFunction('showStreams')
                    oGuiElement.setTitle(__createTitleWithLanguage(aEntry[2], aEntry[1]))

                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('movieUrl', URL_MAIN + str(aEntry[0]))
                    oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showStreams():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('movieUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    sPattern = '<div class="SEP"><div><div></div><h3>DivX Streams</h3><div></div></div></div>(.*?)</table>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntryHtml in aResult[1]:
            __parseHosters('Divx', oGui, aEntryHtml)

    sPattern = '<div class="SEP"><div><div></div><h3>Flash Streams</h3><div></div></div></div>(.*?)</table>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntryHtml in aResult[1]:
            __parseHosters('Flash', oGui, aEntryHtml)    

    oGui.setEndOfDirectory()
    return

def __parseHosters(sFormat, oGui, sHtmlContent):
    sPattern = "onclick=\"return se_ddd.*?,'(.*?)','(.*?)','(.*?)'"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sHostername = __checkHoster(str(aEntry[0]))
            if (sHostername != False):
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_NAME)
                oGuiElement.setFunction('playMovieFromHoster')
                oGuiElement.setTitle(str(sFormat) + ' - ' + str(aEntry[0]) + ' - ' + str(aEntry[1]))

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('sHosterFileName', sHostername)
                oOutputParameterHandler.addParameter('linkToHosterMediaFile', str(aEntry[2]))
                
                 # download context menu
                oContextElement = cContextElement()
                oContextElement.setTitle('Download')
                oContextElement.setFile(SITE_NAME)
                oContextElement.setFunction('downloadStreamFile')
                oOutputParameterHandlerDownload = cOutputParameterHandler()
                oOutputParameterHandlerDownload.addParameter('sHosterFileName', sHostername)
                oOutputParameterHandlerDownload.addParameter('linkToHosterMediaFile', str(aEntry[2]))
                oContextElement.setOutputParameterHandler(oOutputParameterHandlerDownload)
                oGuiElement.addContextItem(oContextElement)
                oGui.addFolder(oGuiElement, oOutputParameterHandler)


def __checkHoster(sHosterName):
    if (sHosterName == 'filestage.to'):
        return 'filestage'

    if (sHosterName == 'megavideo.com'):
        return 'megavideo'

    if (sHosterName == 'mystream.to'):
        return 'mystream'
    
    if (sHosterName == 'duckload.com'):
        return 'duckload'

    if (sHosterName == 'tubeload.to'):
        return 'tubeload'
    
    if (sHosterName == 'videoweed.com'):
        return 'videoweed'

    if (sHosterName == 'zshare.net'):
        return 'zshare'
    

    return False

def playMovieFromHoster():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('sHosterFileName') and oInputParameterHandler.exist('linkToHosterMediaFile')):
        sHosterFileName = oInputParameterHandler.getValue('sHosterFileName')
        linkToHosterMediaFile = oInputParameterHandler.getValue('linkToHosterMediaFile')

        #try:
        exec "from " + sHosterFileName + " import cHoster"
        oHoster = cHoster()
        oHoster.setUrl(linkToHosterMediaFile)
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

def downloadStreamFile():
    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('sHosterFileName') and oInputParameterHandler.exist('linkToHosterMediaFile')):
        sHosterFileName = oInputParameterHandler.getValue('sHosterFileName')
        linkToHosterMediaFile = oInputParameterHandler.getValue('linkToHosterMediaFile')

         #try:
        exec "from " + sHosterFileName + " import cHoster"
        oHoster = cHoster()
        oHoster.setUrl(linkToHosterMediaFile)
        aLink = oHoster.getMediaLink()
        if (aLink[0] == True):
            cDownload().download(aLink[1], 'filename')
            return

        #except:
        #    logger.fatal('could not load plugin: ' + sHosterFileName)


def __createTitleWithLanguage(sLanguage, sTitle):
    sTitle = cUtil().removeHtmlTags(sTitle, '')
    sTitle = str(sTitle).replace('\t', '').replace('&amp;', '&')

    if (sLanguage == 'GER'):
        return sTitle + ' (de)'
    if (sLanguage == 'ENG'):
	return sTitle + ' (en)'

    return sTitle