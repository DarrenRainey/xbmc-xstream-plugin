from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.parser import cParser
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.gui import cGui
from resources.lib.player import cPlayer
from resources.lib.util import cUtil
import logger

SITE_NAME = 'mtv_de'

URL_MAIN = 'http://www.mtv.de'
URL_VIDEOS = 'http://www.mtv.de/videos'
URL_SHOWS = 'http://www.mtv.de/videos/mtv-shows'
URL_CHARTS = 'http://www.mtv.de/charts/germany'
URL_VIDEOCHARTS = 'http://www.mtv.de/charts/videocharts'
URL_XML = 'http://de.esperanto.mtvi.com/www/xml/flv/flvgen.jhtml'
URL_SEARCH = 'http://www.mtv.de/videos/search'

ENTRIES_PER_PAGE = 30

def load():
    logger.info('load mtv :)')
    
    oGui = cGui()
    __createMainMenuItem(oGui, 'Neuste Videos', 'latest')
    __createMainMenuItem(oGui, 'Meist gesehende Videos' , 'views')
    __createMainMenuItem(oGui, 'Beste Bewertungs Videos', 'rating')

    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_NAME)
    oGuiElement.setFunction('showShows')
    oGuiElement.setTitle('Shows')
    oGui.addFolder(oGuiElement)

    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_NAME)
    oGuiElement.setFunction('showCharts')
    oGuiElement.setTitle('Charts')
    oGui.addFolder(oGuiElement)

    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_NAME)
    oGuiElement.setFunction('showVideoCharts')
    oGuiElement.setTitle('VideoCharts')
    oGui.addFolder(oGuiElement)

    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_NAME)
    oGuiElement.setFunction('showSearch')
    oGuiElement.setTitle('Suche')
    oGui.addFolder(oGuiElement)
    oGui.setEndOfDirectory()

def __createMainMenuItem(oGui, sTitle, sOrderBy):
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_NAME)
    oGuiElement.setFunction('listVideos')
    oGuiElement.setTitle(sTitle)
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('orderBy', sOrderBy)
    oGui.addFolder(oGuiElement, oOutputParameterHandler)

def listVideos():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('orderBy')):
        sOrderBy = oInputParameterHandler.getValue('orderBy')

        iPage = 1
        if (oInputParameterHandler.exist('page')):
            iPage = oInputParameterHandler.getValue('page')      

        oRequest = cRequestHandler(URL_VIDEOS)
        oRequest.addParameters('page', iPage)
        oRequest.addParameters('order', sOrderBy)
        sHtmlContent = oRequest.request()

        sPattern = '<li class="fourth">    <p><a title="([^"]+)" href="([^"]+)">.*?<img class="smallImgTeaser" src="([^"]+)".*?/>'
        
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        if (aResult[0] == True):
            for aEntry in aResult[1]:
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_NAME)
                oGuiElement.setFunction('play')
                oGuiElement.setTitle(aEntry[0])
                sThumbnail = str(aEntry[2])
                oGuiElement.setThumbnail(sThumbnail)

                sUrl = URL_MAIN + str(aEntry[1])
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('sUrl', sUrl)
                oGui.addFolder(oGuiElement, oOutputParameterHandler)

            __createNextButtonForVideos(iPage, sOrderBy, oGui)
                
    oGui.setEndOfDirectory()

def listShow():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('showUrl')):
        sShowUrl = oInputParameterHandler.getValue('showUrl')

        sPattern = '<li class="fourth">    <p><a title="([^"]+)" href="([^"]+)">.*?<img class="smallImgTeaser" src="([^"]+)".*?/>'

        oRequest = cRequestHandler(sShowUrl)
        sHtmlContent = oRequest.request()
     
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
            for aEntry in aResult[1]:
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_NAME)
                oGuiElement.setFunction('play')
                oGuiElement.setTitle(aEntry[0])
                sThumbnail = str(aEntry[2])
                oGuiElement.setThumbnail(sThumbnail)

                sUrl = URL_MAIN + str(aEntry[1])
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('sUrl', sUrl)
                oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def __createNextButtonForVideos(iPage, sOrderBy, oGui):
    if (iPage == 1):       
        iNextPage = 2  
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_NAME)
        oGuiElement.setFunction('listVideos')
        oGuiElement.setTitle('mehr ..')
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('orderBy', sOrderBy)
        oOutputParameterHandler.addParameter('page', iNextPage)
        oGui.addFolder(oGuiElement, oOutputParameterHandler)

    return

def showVideoCharts():
    __parseCharts(URL_VIDEOCHARTS)
    
def showCharts():
    __parseCharts(URL_CHARTS)

def __parseCharts(sUrl):
    oGui = cGui()

    sPattern = '<td class="ch_place">.*?"/>(.*?)</td>.*?<td class="ch_last">(.*?)</td>.*?<td class="ch_artist">(.*?)</td>.*?<td class="ch_track">(.*?)</td>.*?<td class="ch_buy">(.*?)</td>'

    oRequest = cRequestHandler(sUrl)
    sHtmlContent = oRequest.request()

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_NAME)
            oGuiElement.setFunction('play')

            sInterpretName = cUtil().removeHtmlTags(str(aEntry[2]), '')

            sTitle = str(aEntry[0]) + ' (' + str(aEntry[1]) + ') : ' + sInterpretName + ' - ' + str(aEntry[3])

            oOutputParameterHandler = cOutputParameterHandler()

            sPattern = '.*?<a href="([^"]+)".*?<img.*?<img.*?src="([^"]+)"'
            sCode = aEntry[4]
            oParser = cParser()
            aResultMeta = oParser.parse(sCode, sPattern)
            if (aResultMeta[0] == True):
                oGuiElement.setTitle(sTitle)

                sLink = aResultMeta[1][0][0]
                sThumbnail = aResultMeta[1][0][1]

                oGuiElement.setThumbnail(sThumbnail)

                sUrl = URL_MAIN + str(sLink)
                oOutputParameterHandler.addParameter('sUrl', sUrl)

            else:
                sTitle = sTitle + ' (NO VIDEO)'
                oGuiElement.setTitle(sTitle)

            oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showShows():
    oGui = cGui()

    sPattern = '<div class="bigImageTeaser">.*?<img src="([^"]+)".*?title="([^"]+)".*?<a href="/tv([^"]+)">'

    oRequest = cRequestHandler(URL_SHOWS)
    sHtmlContent = oRequest.request()
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
   
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_NAME)
            oGuiElement.setFunction('listShow')

            sTitle = aEntry[1].replace('Foto', '')
            oGuiElement.setTitle(sTitle)
            sThumbnail = str(aEntry[0])
            oGuiElement.setThumbnail(sThumbnail)

            sUrl = URL_MAIN + '/tv/' + str(aEntry[2])
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('showUrl', sUrl)
            oGui.addFolder(oGuiElement, oOutputParameterHandler)
            
    oGui.setEndOfDirectory()



def showSearch():
    logger.info('show keyboard')
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        __callSearch(sSearchText, 0)
                            
    oGui.setEndOfDirectory()

def search():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    
    if (oInputParameterHandler.exist('searchText') and oInputParameterHandler.exist('start')):
        sSearchText = oInputParameterHandler.getValue('searchText')
        iStart = oInputParameterHandler.getValue('start')
        __callSearch(sSearchText, iStart)
        return
    
    oGui.setEndOfDirectory()

def __callSearch(sSearchText, iStart):
    logger.info('search : ' + str(sSearchText) + ' start : ' + str(iStart))

    oGui = cGui()

    oRequest = cRequestHandler(URL_SEARCH)
    oRequest.addParameters('q', sSearchText)
    oRequest.addParameters('x', 0)
    oRequest.addParameters('y', 0)
    oRequest.addParameters('n', ENTRIES_PER_PAGE)
    oRequest.addParameters('s', iStart)
    sHtmlContent = oRequest.request()

    sPattern = '<div class="smallVideoTeaser"><a href="([^"]+)" title="([^"]+)"><img .+?><img src="([^"]+)".*?/>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_NAME)
            oGuiElement.setFunction('play')
            oGuiElement.setTitle(aEntry[1])
            sThumbnail = str(aEntry[2])
            oGuiElement.setThumbnail(sThumbnail)

            sUrl = URL_MAIN + str(aEntry[0])
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('sUrl', sUrl)
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

        __createNextButtonForSearch(oGui, iStart, sSearchText, sHtmlContent)
            
    oGui.setEndOfDirectory()

def __createNextButtonForSearch(oGui, iCurrentStart, sSearchText, sHtmlContent):    
    sPattern = '<p class="textPadding">    <strong>([^ ]+) '
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        iCount = aResult[1][0]
        logger.info(iCount)

        iNextStart = __calculateNextPage(iCount, iCurrentStart)
        if (iNextStart > 0):
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_NAME)
            oGuiElement.setFunction('search')
            oGuiElement.setTitle('mehr ..')
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('searchText', sSearchText)
            oOutputParameterHandler.addParameter('start', iNextStart)
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

        
def __calculateNextPage(iCount, iCurrentStart):
    iNextStart = int(iCurrentStart) + ENTRIES_PER_PAGE  
    if (iNextStart < int(iCount)):        
        return iNextStart
    
    return 0


def play():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('sUrl')):
        sUrl = oInputParameterHandler.getValue('sUrl')
        
        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()
       
        sPattern = 'vid=([^;]+);'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
       
        if (aResult[0] == True):
            videoId = aResult[1][0]
            logger.info(videoId)
            
            oRequest = cRequestHandler(URL_XML)
            oRequest.addParameters('vid', videoId)
            oRequest.addParameters('hiLoPref', 'lo')
            sHtmlContent = oRequest.request()
         
            sPattern = '<src>([^<]+)</src>'
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)

            if (aResult[0] == True):
                sStreamUrl = aResult[1][0]
                logger.info(sStreamUrl)
               
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_NAME)
                oGuiElement.setMediaUrl(sStreamUrl)
                oPlayer = cPlayer()
                oPlayer.addItemToPlaylist(oGuiElement)
                oPlayer.startPlayer()
                return
                            
    oGui.setEndOfDirectory()