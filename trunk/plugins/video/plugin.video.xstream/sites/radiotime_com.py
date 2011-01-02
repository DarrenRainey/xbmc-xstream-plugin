
from resources.lib.util import cUtil
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.parser import cParser
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.gui import cGui
from resources.lib.player import cPlayer
import logger

SITE_NAME = 'radiotime_com'

URL_MAIN = 'http://radiotime.com'
URL_REGION = 'http://radiotime.com/region/'
URL_MUSIC = 'http://radiotime.com/genre/c_1/Music.aspx'
URL_TALK = 'http://radiotime.com/genre/c_2/Spoken.aspx'
URL_SPORT = 'http://radiotime.com/genre/c_323/Sports.aspx'
URL_LOCATION = 'http://radiotime.com/region/c_0/Browse_Locations.aspx'

URL_SPECIAL_SPORT = 'http://radiotime.com/channel/c_424726/RadioTime_Sports.aspx'

URL_SEARCH = 'http://radiotime.com/Search.aspx?query='
URL_PLAY = 'http://radiotime.com/WebTuner.aspx?StationId='

def load():
    logger.info('load radiotime.com :)')
    oGui = cGui()

    sLokalUrl = __getLocalRadioUrl()
    if (sLokalUrl != False):
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sLokalUrl)
        __createMenuEntry(oGui, 'showMenuEntries', 'Lokal Radio (Radio in deiner Naehe)', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_TALK)
    __createMenuEntry(oGui, 'showMenuEntries', 'nach Sendungen', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MUSIC)
    __createMenuEntry(oGui, 'showMenuEntries', 'nach Musikrichtungen', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SPORT)
    __createMenuEntry(oGui, 'showMenuEntries', 'nach Sportarten', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_LOCATION)
    __createMenuEntry(oGui, 'showMenuEntries', 'nach Orte', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SPECIAL_SPORT)
    __createMenuEntry(oGui, 'showMenuEntries', 'Spezielle Sportsendungen', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN)
    __createMenuEntry(oGui, 'showSearch', 'Suche', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def __createMenuEntry(oGui, sFunction, sLabel, oOutputParameterHandler = ''):
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_NAME)
    oGuiElement.setFunction(sFunction)
    oGuiElement.setTitle(sLabel)
    oGui.addFolder(oGuiElement, oOutputParameterHandler)

def __getLocalRadioUrl():
    oRequestHandler = cRequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request();

    sPattern = '<li class="yuimenubaritem"><a class="yuimenubaritemlabel" href="/region/([^"]+)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return URL_REGION + str(aResult[1][0])

    return False

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):

        sSearchText = sSearchText.replace(' ', '+')
        sUrl = URL_SEARCH + str(sSearchText)
        __showMenuEntries(sUrl)
        return

    oGui.setEndOfDirectory()


def showMenuEntries():
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    __showMenuEntries(sUrl)

def __showMenuEntries(sUrl):
    oGui = cGui()
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    if (__isSearchRefinePage(sHtmlContent) == True):
        __showSearchRefinePage(oGui, sHtmlContent)

    __showStations(oGui, sHtmlContent)
    __showStationsMore(oGui, sHtmlContent)

    oGui.setEndOfDirectory()

def __showSearchRefinePage(oGui, sHtmlContent):
    oGui = cGui()

    sPattern = '<a title="([^"]+)" href="([^"]+)"><strong>([^"]+)</strong></a><br />'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            if (str(aEntry[0]) != 'Mehr dazu im... Radio'):
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_NAME)
                oGuiElement.setFunction('showMenuEntries')
                oGuiElement.setTitle(str(aEntry[2]))

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + str(aEntry[1]))
                oGui.addFolder(oGuiElement, oOutputParameterHandler)
   

def __isSearchRefinePage(sHtmlContent):
    sPattern = '<div id="searchRefineWrap">(.*?)<td class="label browse">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        return True

    return False

def __showStations(oGui, sHtmlContent):
    sPattern = '<tr valign="top" class="result station">.*?<img src="([^"]+)".*?<div class="actions">.*?<a href="javascript:play\(([^,]+).*?<td class="description">.*?<a href=.*?>(.*?)<.*?<div class="location">(.*?)</div>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_NAME)
            oGuiElement.setFunction('showStreams')
            oGuiElement.setTitle('[R] ' + str(aEntry[2]) + ' (' + cUtil().removeHtmlTags(str(aEntry[3])).replace('\t', '') + ')' )
            oGuiElement.setThumbnail(str(aEntry[0]))

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', URL_PLAY + str(aEntry[1]))
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

def __showStationsMore(oGui, sHtmlContent):    
    sPattern = '<a href="javascript:play\(([^,]+).*?class="td-freq">(.*?)<.*?<td class="td-station"><a href=".*?">(.*?)<.*?<td class="td-city">(.*?)<'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_NAME)
            oGuiElement.setFunction('showStreams')
            oGuiElement.setTitle('[R] ' + str(aEntry[1]) + ' - ' + str(aEntry[2]) + ' (' + str(aEntry[3]) + ')')
           
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', URL_PLAY + str(aEntry[0]))
            oGui.addFolder(oGuiElement, oOutputParameterHandler)



def showStreams():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    sPattern = '"StreamId":.*?"Url":"([^"]+)".*?"Bandwidth":([^,]+).*?"MediaType":"([^"]+)"'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
        
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_NAME)
            oGuiElement.setFunction('play')
            oGuiElement.setTitle('Format: ' + str(aEntry[2]) + ' - Quality: ' + str(aEntry[1]))
            oGuiElement.setThumbnail(str(aEntry[0]))

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',  str(aEntry[0]))
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()
  

def play():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_NAME)
    oGuiElement.setMediaUrl(sUrl)

    oPlayer = cPlayer()
    oPlayer.addItemToPlaylist(oGuiElement)
    oPlayer.startPlayer()
    return

