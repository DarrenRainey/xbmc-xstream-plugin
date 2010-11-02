from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.parser import cParser
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.gui import cGui
from resources.lib.player import cPlayer
from resources.lib.util import cUtil
import logger


SITE_NAME = 'simpsons_to'

URL_MAIN = 'http://www.simpsons.to/'
URL_LOAD_PAGE = 'http://www.simpsons.to/load_page.php'
URL_PLAYER = 'http://stream.simpsons.to/streamlink/?'

def load():
    logger.info('load simpsons :)')

    oGui = cGui()

    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_NAME)
    oGuiElement.setFunction('displaySeasions')
    oGuiElement.setTitle('Staffeln')
    oGui.addFolder(oGuiElement)

    oGui.setEndOfDirectory()

def __loadPageContent():
    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('sPage')):
        sPage = oInputParameterHandler.getValue('sPage')

        oRequest = cRequestHandler(URL_LOAD_PAGE)
        oRequest.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
        oRequest.addParameters('page', sPage)
        sHtmlContent = oRequest.request()
        return sHtmlContent

    return False
    
def displaySeasions():
    oGui = cGui()
    sPattern = '<div id="staffeln">(.*?)<div id='

    oRequest = cRequestHandler(URL_MAIN)
    sHtmlContent = oRequest.request()    

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
  
    if (aResult[0] == True):
        sHtmlContent = aResult[1][0]
        
        sPattern = '<a href="([^"]+)">([^<]+)</a>'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        for aEntry in aResult[1]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_NAME)
            oGuiElement.setFunction('showEpisodes')
            oGuiElement.setTitle(aEntry[1])
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('sPage', aEntry[0])
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showEpisodes():
    oGui = cGui()

    sHtmlContent = __loadPageContent()
    if (sHtmlContent != False):
        # mit sprache, jedoch bekomme ich dann nicht den letzten eintrag
        #sPattern = '<h1 style="color:#000000;" title="([^"]+)">.*?<img src="([^"]+)" class="episoden_vorschau".*?<a href="([^"]+)" class="optionen_alle".*?<img src="images/language/(.*?).gif"'

        sPattern = '<h1 style="color:#000000;" title="([^"]+)">.*?<img src="([^"]+)" class="episoden_vorschau".*?<a href="([^"]+)" class="optionen_alle"'

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
       
        if (aResult[0] == True):
            for aEntry in aResult[1]:
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_NAME)
                oGuiElement.setFunction('showHoster')
                #oGuiElement.setTitle(__createTitle(aEntry[0], aEntry[3]))
                oGuiElement.setTitle(__createTitle(aEntry[0], ''))
                oGuiElement.setThumbnail(URL_MAIN + str(aEntry[1]))

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('sPage', aEntry[2])
                oGui.addFolder(oGuiElement, oOutputParameterHandler)
        

    oGui.setEndOfDirectory()

def __createTitle(sTitle, sLanguage):
    if (sLanguage == 'gb'):
        return sTitle + ' (ENG)'

    if (sLanguage == 'de'):
        return sTitle + ' (DE)'

    return sTitle

def showHoster():
    oGui = cGui()

    sHtmlContent = __loadPageContent()
    if (sHtmlContent != False):

        oParser = cParser()
        sPattern = "<b>Hoster:</b>(.*?)</div>.*?<a href='([^']+)' class='optionen_mirror'"
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
            for aEntry in aResult[1]:
                sTitle = cUtil().removeHtmlTags(aEntry[0], '').replace(' ', '')

                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_NAME)
                oGuiElement.setFunction('parseHoster')
                oGuiElement.setTitle(sTitle)

                sPlayerId = __getPlayerId(aEntry[1])

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('sPlayerId', sPlayerId)
                oOutputParameterHandler.addParameter('sHosterName', sTitle)
                oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def __getPlayerId(sUrl):
    sUrl = str(sUrl)    
    aUrlParts = sUrl.split('-')  
    return aUrlParts[1]

def parseHoster():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('sPlayerId') and oInputParameterHandler.exist('sHosterName')):
        sPlayerId = oInputParameterHandler.getValue('sPlayerId')
        sHosterName = oInputParameterHandler.getValue('sHosterName')

        print sPlayerId
        print sHosterName
       
        __playStreamUrl(sPlayerId, sHosterName)
        return
    
    oGui.setEndOfDirectory()

def __playStreamUrl(sPlayerId, sHosterName):
    oGui = cGui()

    sHosterName = sHosterName.lower()

    sUrl = URL_PLAYER + str(sPlayerId)
    oRequest = cRequestHandler(sUrl)
    oRequest.request()
    sStreamUrl = oRequest.getRealUrl()
    print sStreamUrl
    
    if (sHosterName == 'mystream.to'):
        __play('mystream', sStreamUrl, '', False)
        return

    if (sHosterName == 'megavideo.com'):
        __play('megavideo', sStreamUrl, '', False)
        return

    if (sHosterName == 'duckload.com'):
        __play('duckload', sStreamUrl, '', False)
        return

    if (sHosterName == 'zshare.net'):
        __play('zshare', sStreamUrl, '', False)
        return

    if (sHosterName == 'videoweed.com'):
        __play('videoweed', sStreamUrl, '', False)
        return

    if (sHosterName == 'tubeload.to'):
        __play('tubeload', sStreamUrl, '', False)
        return


    oGui.setEndOfDirectory()


def __playDirect(sUrl):   
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_NAME)
    oGuiElement.setMediaUrl(sUrl)

    oPlayer = cPlayer()
    oPlayer.addItemToPlaylist(oGuiElement)
    oPlayer.startPlayer()
    return

def __play(sHosterFileName, sLinkToHosterMediaFile, sTitle, bDownload):
    oGui = cGui()

    exec "from " + sHosterFileName + " import cHoster"
    print 'load hoster ' + sHosterFileName
    oHoster = cHoster()
    oHoster.setUrl(sLinkToHosterMediaFile)
    aLink = oHoster.getMediaLink()
       
    if (aLink[0] == True):
        if (bDownload == True):
            cDownload().download(aLink[1], sTitle)
        else:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_NAME)
            oGuiElement.setMediaUrl(aLink[1])

            oPlayer = cPlayer()
            oPlayer.addItemToPlaylist(oGuiElement)
            oPlayer.startPlayer()
        return

    oGui.setEndOfDirectory()
            
