from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.parser import cParser
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.gui import cGui
from resources.lib.player import cPlayer
from resources.lib.util import cUtil
import logger


SITE_NAME = 'bundesliga_de'

URL_MAIN = 'http://www.bundesliga.de'
URL_TV = 'http://www.bundesliga.de/de/bundesliga-tv/'
URL_GET_STREAM = 'http://www.bundesliga.de/flash/vp/'

def load():
    logger.info('load bundesliga :)')

    oGui = cGui()
    __createMainMenuItem(oGui, 'Aktuell', 'aktuell')
    __createMainMenuItem(oGui, 'Vorschau' , 'vorschau')
    __createMainMenuItem(oGui, 'Spieltag', 'spieltag')
    __createMainMenuItem(oGui, 'Highlights', 'highlights')
    __createMainMenuItem(oGui, 'Interview', 'interview')
    __createMainMenuItem(oGui, 'Dfl', 'dfl')
    __createMainMenuItem(oGui, 'Hintergrund', 'hintergrund')
    oGui.setEndOfDirectory()

def __createMainMenuItem(oGui, sTitle, sPlaylistId):
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_NAME)
    oGuiElement.setFunction('listVideos')
    oGuiElement.setTitle(sTitle)
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('playlistId', sPlaylistId)
    oGui.addFolder(oGuiElement, oOutputParameterHandler)

def listVideos():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('playlistId')):
        sPlaylistId = oInputParameterHandler.getValue('playlistId')

        sUrl = URL_TV + str(sPlaylistId) + '/index.php'
        sPattern = '<param name="flashVars" value="xmlfilepath=([^"]+)" />'
      
        oRequest = cRequestHandler(sUrl)
        oRequest.addParameters('f', '')
        sHtmlContent = oRequest.request()
       
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
            sXmlUrl = URL_MAIN + aResult[1][0]
            logger.info(sXmlUrl)
            __parseXmlFile(oGui, sXmlUrl)

    oGui.setEndOfDirectory()

def __parseXmlFile(oGui, sUrl):
    oRequest = cRequestHandler(sUrl)
    sHtmlContent = oRequest.request()

    sPattern = '<TEASER><!\[CDATA\[([^>]+)>\\]]></TEASER>  <MEDIA_URL>([^>]+)</MEDIA_URL>  <LINK><!\[CDATA\[javascript:showVideoSnippet\(\'([^;]+)\'\); void\(0\);\]\]></LINK>'
   
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
         for aEntry in aResult[1]:
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_NAME)
                oGuiElement.setFunction('play')
                oGuiElement.setTitle(aEntry[0])
                sThumbnail = URL_MAIN + str(aEntry[1])
                oGuiElement.setThumbnail(sThumbnail)

                sUrl = URL_MAIN + str(aEntry[2])
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('sUrl', sUrl)
                oGui.addFolder(oGuiElement, oOutputParameterHandler)

def play():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('sUrl')):
        sUrl = oInputParameterHandler.getValue('sUrl')
               
        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()

        sPattern = '<param name="flashvars" value="meta=%2Fflash%2Fvp%2F([^"]+)"'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
            sUrlParams = cUtil().urlDecode(aResult[1][0])           
            sStreamUrl = URL_GET_STREAM + sUrlParams

            oRequest = cRequestHandler(sStreamUrl)
            sHtmlContent = oRequest.request()

            sPattern = '<videofile src="([^"]+)" />'
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
                
    oGui = cGui()
    oGui.setEndOfDirectory()
