import logger
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.player import cPlayer
from resources.lib.gui.contextElement import cContextElement
from resources.lib.download import cDownload


SITE_NAME = 'gstream_in'
URL_MAIN = 'http://g-stream.in'
URL_SHOW_MOVIE = 'http://g-stream.in/showthread.php?t='
URL_CATEGORIES = 'http://g-stream.in/forumdisplay.php?f='
URL_HOSTER = 'http://g-stream.in/secure/'
URL_SEARCH = 'http://g-stream.in/search.php'

def load():
    logger.info('load g-stream.in :)')

    oGui = cGui()
    __createMainMenuEntry(oGui, 'Aktuelle KinoFilme', 542)
    __createMainMenuEntry(oGui, 'Action', 591)
    __createMainMenuEntry(oGui, 'Horror', 593)
    __createMainMenuEntry(oGui, 'Komoedie', 592)
    __createMainMenuEntry(oGui, 'Thriller', 595)
    __createMainMenuEntry(oGui, 'Drama', 594)
    __createMainMenuEntry(oGui, 'Fantasy', 655)
    __createMainMenuEntry(oGui, 'Abenteuer', 596)
    __createMainMenuEntry(oGui, 'Animation', 677)
    __createMainMenuEntry(oGui, 'Dokumentation', 751)

    oGui.setEndOfDirectory()

def __createMainMenuEntry(oGui, sMenuName, iCategoryId):
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_NAME)
    oGuiElement.setTitle(sMenuName)
    oGuiElement.setFunction('parseMovieResultSite')
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('normalySiteUrl', URL_CATEGORIES + str(iCategoryId) + '&order=desc&page=')
    oOutputParameterHandler.addParameter('siteUrl', URL_CATEGORIES + str(iCategoryId) + '&order=desc&page=1')
    oOutputParameterHandler.addParameter('iPage', 1)
    oGui.addFolder(oGuiElement, oOutputParameterHandler)

def parseMovieResultSite():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('siteUrl')):
        siteUrl = oInputParameterHandler.getValue('siteUrl')
        normalySiteUrl = oInputParameterHandler.getValue('normalySiteUrl')
        iPage = oInputParameterHandler.getValue('iPage')
       
        sPattern = '<a href="([^"]+)" id="([^"]+)">([^<]+)<'
        
        # request
        oRequest = cRequestHandler(siteUrl)
        sHtmlContent = oRequest.request()

        # parse content
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            for aEntry in aResult[1]:
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_NAME)
                oGuiElement.setFunction('parseMovie')
                oGuiElement.setTitle(aEntry[2])
                sUrl = str(aEntry[1]).replace('thread_title_', '')               
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('movieUrl', URL_SHOW_MOVIE + str(sUrl))
                oGui.addFolder(oGuiElement, oOutputParameterHandler)


        # check for next site
        sPattern = '<td class="thead">Zeige Themen .*?von ([^<]+)</td>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            for aEntry in aResult[1]:
                iTotalCount = aEntry[0]
                iNextPage = int(iPage) + 1
                iCurrentDisplayStart = __createDisplayStart(iNextPage)
                if (iCurrentDisplayStart < iTotalCount):
                    oGuiElement = cGuiElement()
                    oGuiElement.setSiteName(SITE_NAME)
                    oGuiElement.setFunction('parseMovieResultSite')
                    oGuiElement.setTitle('next ..')

                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('iPage', iNextPage)
                    oOutputParameterHandler.addParameter('normalySiteUrl', normalySiteUrl)
                    normalySiteUrl = normalySiteUrl + str(iNextPage)
                    oOutputParameterHandler.addParameter('siteUrl', normalySiteUrl)
                    oGui.addFolder(oGuiElement, oOutputParameterHandler)


    oGui.setEndOfDirectory()

def __createDisplayStart(iPage):
    return (20 * int(iPage)) - 20

def parseMovie():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('movieUrl')):
        sSiteUrl = oInputParameterHandler.getValue('movieUrl')
        
        oRequest = cRequestHandler(sSiteUrl)
        sHtmlContent = oRequest.request()

        aHosters = []
        aHosters.append(__parseHosterSiteFromSite(sHtmlContent, 'duckload.com', 'www.duckload.com', 'parseHosterDefault', 'duckload'))
        aHosters.append(__parseHosterSiteFromSite(sHtmlContent, 'mystream.to', 'www.mystream.to', 'parseHosterDefault', 'mystream'))
        aHosters.append(__parseHosterSiteFromSite(sHtmlContent, 'loaded.it', 'loaded.it', 'parseHosterLoadedIt', 'loadedit'))
        aHosters.append(__parseHosterSiteFromSite(sHtmlContent, 'tubeload.to', 'www.tubeload.to', 'parseHosterDefault', 'tubeload'))
        
        for aHoster in aHosters:
            if (len(aHoster) > 0):
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_NAME)
                oGuiElement.setTitle(aHoster[0])
                oGuiElement.setFunction('playMovieFromHoster')

                oContextElement = cContextElement()
                oContextElement.setTitle('Download')
                oContextElement.setFile(SITE_NAME)
                oContextElement.setFunction('playMovieFromHoster')
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('hosterName', aHoster[0])
                oOutputParameterHandler.addParameter('linkToHosterMediaFile', aHoster[1])
                oOutputParameterHandler.addParameter('hosterParserMethode', aHoster[2])
                oOutputParameterHandler.addParameter('sHosterFileName', aHoster[3])
                oOutputParameterHandler.addParameter('bDownload', 'True')                
                oContextElement.setOutputParameterHandler(oOutputParameterHandler)
                oGuiElement.addContextItem(oContextElement)

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('hosterName', aHoster[0])
                oOutputParameterHandler.addParameter('linkToHosterMediaFile', aHoster[1])
                oOutputParameterHandler.addParameter('hosterParserMethode', aHoster[2])
                oOutputParameterHandler.addParameter('sHosterFileName', aHoster[3])
                oGui.addFolder(oGuiElement, oOutputParameterHandler)
        
    oGui.setEndOfDirectory()

def playMovieFromHoster():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('sHosterFileName') and oInputParameterHandler.exist('linkToHosterMediaFile')):
        sHosterFileName = oInputParameterHandler.getValue('sHosterFileName')
        linkToHosterMediaFile = oInputParameterHandler.getValue('linkToHosterMediaFile').replace(' ', '+')
        sFilename = oInputParameterHandler.getValue('hosterName')
        bDownload = False
        

        # get real url        
        oRequest = cRequestHandler(linkToHosterMediaFile)
        oRequest.request()
        linkToHosterMediaFile = oRequest.getRealUrl()
        logger.info('real Url: ' + str(linkToHosterMediaFile))

        #try:
        exec "from " + sHosterFileName + " import cHoster"
        oHoster = cHoster()
        oHoster.setUrl(linkToHosterMediaFile)
        aLink = oHoster.getMediaLink()
        if (aLink[0] == True):
            if (bDownload == True):
                cDownload().download(aLink[1], sFilename)
            else:
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_NAME)
                oGuiElement.setMediaUrl(aLink[1])

                oPlayer = cPlayer()
                oPlayer.addItemToPlaylist(oGuiElement)
                oPlayer.startPlayer()
            return
            
        #except:
        #logger.fatal('could not load plugin: ' + sHosterFileName)

    oGui.setEndOfDirectory()


def __parseHosterSiteFromSite(sHtmlContent, sHosterName, sHosterId, sHosterMethodeName, sHosterFilename):
    aHoster = []
    sRegex = '<a href="' + URL_HOSTER + sHosterId + '([^ ]+)" target="_blank" rel="nofollow" >'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sRegex, 1)
    if (aResult[0] == True):
        sUrl = URL_HOSTER + sHosterId + aResult[1][0]

        aHoster.append(sHosterName)
        aHoster.append(sUrl)
        aHoster.append(sHosterMethodeName)
        aHoster.append(sHosterFilename)

    return aHoster
