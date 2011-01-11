from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler

SITE_IDENTIFIER = 'iload_to'
SITE_NAME = 'ILoad.to'

URL_MAIN = 'http://iload.to'
URL_MOVIE_PAGE = 'http://iload.to/category/1-Filme/'
URL_CHARACTERS = 'http://iload.to/category/1-Filme/letter'
URL_SEARCH = 'http://iload.to/ajax/module/category/1-Filme/search/'

COOKIE_SECURITY_NAME = 'suilid'

def load():
    sCookieValue = __getSecurityCookieValue()

    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_CHARACTERS)
    oOutputParameterHandler.addParameter('security', sCookieValue)
    __createMenuEntry(oGui, 'showCharacters', 'Filme', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN)
    oOutputParameterHandler.addParameter('security', sCookieValue)
    __createMenuEntry(oGui, 'showCinemaMovies', 'aktuelle KinoFilme', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MOVIE_PAGE)
    oOutputParameterHandler.addParameter('security', sCookieValue)
    __createMenuEntry(oGui, 'displayGenre', 'Genre', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH)
    oOutputParameterHandler.addParameter('security', sCookieValue)
    __createMenuEntry(oGui, 'displaySearch', 'Suche', oOutputParameterHandler)
    
    oGui.setEndOfDirectory()

def __getSecurityCookieValue():
    oRequestHandler = cRequestHandler(URL_MAIN)
    oRequestHandler.request();
    aHeader = oRequestHandler.getResponseHeader()
    sReponseCookie = aHeader.getheader("Set-Cookie")

    sPattern = COOKIE_SECURITY_NAME + '=([^;]+);'
    oParser = cParser()
    aResult = oParser.parse(sReponseCookie, sPattern)
    if (aResult[0] == True):        
        return COOKIE_SECURITY_NAME + '=' + str(aResult[1][0])

    return ''

def __createMenuEntry(oGui, sFunction, sLabel, oOutputParameterHandler = ''):
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction(sFunction)
    oGuiElement.setTitle(sLabel)
    oGui.addFolder(oGuiElement, oOutputParameterHandler)

def showCharacters():

    oInputParameterHandler = cInputParameterHandler()
    sSecurity = oInputParameterHandler.getValue('security')

    oGui = cGui()
    __createCharacters(oGui, '#', sSecurity)
    __createCharacters(oGui, 'A', sSecurity)
    __createCharacters(oGui, 'B', sSecurity)
    __createCharacters(oGui, 'C', sSecurity)
    __createCharacters(oGui, 'D', sSecurity)
    __createCharacters(oGui, 'E', sSecurity)
    __createCharacters(oGui, 'F', sSecurity)
    __createCharacters(oGui, 'G', sSecurity)
    __createCharacters(oGui, 'H', sSecurity)
    __createCharacters(oGui, 'I', sSecurity)
    __createCharacters(oGui, 'J', sSecurity)
    __createCharacters(oGui, 'K', sSecurity)
    __createCharacters(oGui, 'L', sSecurity)
    __createCharacters(oGui, 'N', sSecurity)
    __createCharacters(oGui, 'O', sSecurity)
    __createCharacters(oGui, 'Q', sSecurity)
    __createCharacters(oGui, 'R', sSecurity)
    __createCharacters(oGui, 'S', sSecurity)
    __createCharacters(oGui, 'T', sSecurity)
    __createCharacters(oGui, 'U', sSecurity)
    __createCharacters(oGui, 'V', sSecurity)
    __createCharacters(oGui, 'W', sSecurity)
    __createCharacters(oGui, 'X', sSecurity)
    __createCharacters(oGui, 'Y', sSecurity)
    __createCharacters(oGui, 'Z', sSecurity)
    
    oGui.setEndOfDirectory()

def __createCharacters(oGui, sCharacter, sCookieValue):
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction('showMovies')
    oGuiElement.setTitle(sCharacter)

    if (sCharacter == '#'):
        sCharacter = '_'

    sUrl = URL_CHARACTERS + '/' + str(sCharacter) + '/'

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oOutputParameterHandler.addParameter('page', '1')
    oOutputParameterHandler.addParameter('security', sCookieValue)
    oGui.addFolder(oGuiElement, oOutputParameterHandler)

def displaySearch():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sSecurity = oInputParameterHandler.getValue('security')


    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):

        sSearchText = sSearchText.replace(' ', '+')
        sUrl = URL_SEARCH + str(sSearchText) + '/'
        __showMovies(sUrl, 1, sSecurity)
        return

    oGui.setEndOfDirectory()

def displayGenre():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sSecurity = oInputParameterHandler.getValue('security')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Cookie', sSecurity)
    sHtmlContent = oRequestHandler.request();

    sPattern = '<a href="([^"]+)" class="next level3">.*?<div>(.*?)</div>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('showMovies')
            oGuiElement.setTitle(aEntry[1])

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('page', '1')
            oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + str(aEntry[0]))
            oOutputParameterHandler.addParameter('security', sSecurity)
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()



def showMovies():
    oInputParameterHandler = cInputParameterHandler()
    sSiteUrl = oInputParameterHandler.getValue('siteUrl')
    iPage = oInputParameterHandler.getValue('page')
    sSecurity = oInputParameterHandler.getValue('security')

    __showMovies(sSiteUrl, iPage, sSecurity)
    

def __showMovies(sSiteUrl, iPage, sSecurity):
    oGui = cGui()

    sUrl = str(sSiteUrl) + str('page/') + str(iPage)

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Cookie', sSecurity)
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = str(sHtmlContent).replace('\\', '')
    
    sPattern = '<table class="row">.*?class="list-cover".*?<img src="([^"]+)">.*?class="list-name".*?<a href="([^"]+)".*?>(.*?)</a>.*?class="description".*?>(.*?)</td>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('showRelease')
            oGuiElement.setTitle(cUtil().removeHtmlTags(aEntry[2]))
            oGuiElement.setThumbnail(aEntry[0])
            oGuiElement.setDescription(aEntry[3])

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('movieUrl', URL_MAIN + str(aEntry[1]))
            oOutputParameterHandler.addParameter('security', sSecurity)
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

    sNextUrl = __checkForNextPage(sHtmlContent, iPage)
    if (sNextUrl != False):
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_IDENTIFIER)
        oGuiElement.setFunction('showMovies')
        oGuiElement.setTitle('next ..')

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sSiteUrl)
        oOutputParameterHandler.addParameter('page', int(iPage) + 1)
        oOutputParameterHandler.addParameter('security', sSecurity)
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
    sSecurity = oInputParameterHandler.getValue('security')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Cookie', sSecurity)
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
                    oGuiElement.setSiteName(SITE_IDENTIFIER)
                    oGuiElement.setFunction('showRelease')
                    oGuiElement.setTitle(cUtil().removeHtmlTags(aEntry[2]))
                    oGuiElement.setThumbnail(aEntry[1])
                  
                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('movieUrl', URL_MAIN + str(aEntry[0]))
                    oOutputParameterHandler.addParameter('security', sSecurity)
                    oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def __createInfo(oGui, sHtmlContent):
    sPattern = '<table class="description">.*?<td class="cover"><a href="([^"]+)".*?<td class="text">(.*?)</td>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setTitle('info (press Info Button)')
            oGuiElement.setThumbnail(str(aEntry[0]))
            oGuiElement.setFunction('dummyFolder')
            oGuiElement.setDescription(cUtil().removeHtmlTags(str(aEntry[1])))
            oGui.addFolder(oGuiElement)

def dummyFolder():
    oGui = cGui()
    oGui.setEndOfDirectory()

def showRelease():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sSecurity = oInputParameterHandler.getValue('security')
    sUrl = oInputParameterHandler.getValue('movieUrl')
    
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Cookie', sSecurity)
    sHtmlContent = oRequestHandler.request();

    __createInfo(oGui, sHtmlContent)

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
                    oGuiElement.setSiteName(SITE_IDENTIFIER)
                    oGuiElement.setFunction('showStreams')
                    oGuiElement.setTitle(__createTitleWithLanguage(aEntry[2], aEntry[1]))

                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('movieUrl', URL_MAIN + str(aEntry[0]))
                    oOutputParameterHandler.addParameter('security', sSecurity)
                    oGui.addFolder(oGuiElement, oOutputParameterHandler)
    else:
        sPattern = '<a href="([^"]+)" target="_self" data-tab="ReleaseTab" data-tab-name="Downloads">Downloads</a>'

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
            for aEntry in aResult[1]:
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_IDENTIFIER)
                oGuiElement.setFunction('showStreams')

                sPattern = '<a href="/release/(.*?)">([^"]+)</a>'
                oParser = cParser()
                aResultTitle = oParser.parse(sHtmlContent, sPattern)

                if (aResultTitle[0] == True):
                    sTitle = aResultTitle[1][0][1]                    
                    oGuiElement.setTitle(sTitle)
                else:
                    oGuiElement.setTitle('no title')

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('movieUrl', sUrl)
                oOutputParameterHandler.addParameter('security', sSecurity)
                oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showStreams():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('movieUrl')
    sSecurity = oInputParameterHandler.getValue('security')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Cookie', sSecurity)
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

            oHoster = __getHoster(str(aEntry[0]))
            if (oHoster != False):
                sTitle = str(sFormat) + ' - ' + str(aEntry[0]) + ' - ' + str(aEntry[1])
                oHoster.setDisplayName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, str(aEntry[2]))                


def __getHoster(sHosterName):
    if (sHosterName == 'filestage.to'):
        return cHosterHandler().getHoster('filestage')

    if (sHosterName == 'megavideo.com'):
        return cHosterHandler().getHoster('megavideo')

    if (sHosterName == 'mystream.to'):
        return cHosterHandler().getHoster('mystream')
    
    if (sHosterName == 'duckload.com'):
        return cHosterHandler().getHoster('duckload')

    if (sHosterName == 'tubeload.to'):
        return cHosterHandler().getHoster('tubeload')
    
    if (sHosterName == 'videoweed.com'):
        return cHosterHandler().getHoster('videoweed')

    if (sHosterName == 'zshare.net'):
        return cHosterHandler().getHoster('zshare')    

    return False

def __createTitleWithLanguage(sLanguage, sTitle):
    sTitle = cUtil().removeHtmlTags(sTitle, '')
    sTitle = str(sTitle).replace('\t', '').replace('&amp;', '&')

    if (sLanguage == 'GER'):
        return sTitle + ' (de)'
    if (sLanguage == 'ENG'):
	return sTitle + ' (en)'

    return sTitle