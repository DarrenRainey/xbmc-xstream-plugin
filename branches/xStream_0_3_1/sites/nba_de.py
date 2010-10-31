from resources.lib.util import cUtil
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.parser import cParser
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.gui import cGui
from resources.lib.player import cPlayer
import logger

SITE_NAME = 'nba_de'

URL_PLAYLIST = 'http://www.nba.de/video/index.php/action/get-playlist-videos/playlist-id/'
URL_POST_FOR_MOVIE = 'http://akmi.kaltura.com//api_v3/index.php?service=multirequest&action=null'
URL_HIGHLIGHTS = 'http://www.nba.de/video/index.php/action/get-videos/category/'

def load():
    logger.info('load nba :)')
        
    oGui = cGui()

    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_NAME)
    oGuiElement.setFunction('listVideos')
    oGuiElement.setTitle('Neuste Videos')
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('playlistId', '0_65ltkg6t')
    oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_NAME)
    oGuiElement.setFunction('listVideos')
    oGuiElement.setTitle('Meist gesehende')
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('playlistId', '0_mmdxlq9n')
    oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_NAME)
    oGuiElement.setFunction('listHighlights')
    oGuiElement.setTitle('Highlights - alle')
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('urlPart', '1_Highlights>Alle')
    oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_NAME)
    oGuiElement.setFunction('listHighlights')
    oGuiElement.setTitle('Highlights - Daily Zap')
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('urlPart', '1_Highlights>Daily Zap')
    oGui.addFolder(oGuiElement, oOutputParameterHandler)    

    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_NAME)
    oGuiElement.setFunction('listHighlights')
    oGuiElement.setTitle('Highlights - Mavericks')
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('urlPart', '1_Highlights>Mavericks')
    oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def listHighlights():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('urlPart')):
        sUrlPart = oInputParameterHandler.getValue('urlPart')

        sUrl = URL_HIGHLIGHTS + sUrlPart
        
        sPattern = '{"mediaType":1,.*?"dataUrl":"([^"]+)".*?"duration":([^,]+),.*?"name":"([^"]+)".*?"thumbnailUrl":"([^"]+)".*?'
        
        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()
        sHtmlContent = sHtmlContent.replace('\/', '/')
        sHtmlContent = sHtmlContent.replace('\\"', '"')
        
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        if (aResult[0] == True):
            for aEntry in aResult[1]:
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_NAME)
                oGuiElement.setFunction('playVideo')
                
                sDurationFormatted = cUtil().formatTime(aEntry[1])
                sTitle = aEntry[2] + ' (' + sDurationFormatted + ')'
                oGuiElement.setTitle(sTitle)
                oGuiElement.setThumbnail(aEntry[3])
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('videoUrl', aEntry[0])
                oGui.addFolder(oGuiElement, oOutputParameterHandler)
                
    oGui.setEndOfDirectory()

def listVideos():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('playlistId')):
        sPlaylistId = oInputParameterHandler.getValue('playlistId')

        sUrl = URL_PLAYLIST + str(sPlaylistId)
       
        sPattern = '<li><a href="#([^"]+)".*?><img src="([^"]+)".*?></div><div>([^"]+)</div></a></li>'

        # request
        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()
        sHtmlContent = sHtmlContent.replace('\/', '/')
        sHtmlContent = sHtmlContent.replace('\\"', '"')
       
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
            for aEntry in aResult[1]:
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_NAME)
                oGuiElement.setFunction('playVideo')

                sTitle = cUtil().removeHtmlTags(aEntry[2], ' ')
                oGuiElement.setTitle(sTitle)
                oGuiElement.setThumbnail(aEntry[1])

                sVideoUrl = __createVideoUrl(aEntry[1], aEntry[0])                
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('videoUrl', sVideoUrl)                
                oGui.addFolder(oGuiElement, oOutputParameterHandler)
    
    oGui.setEndOfDirectory()

def __createVideoUrl(sThumbnailUrl, sVideoId):
    aUrlParts = sThumbnailUrl.split('thumbnail');
    return str(aUrlParts[0]) + 'flvclipper/entry_id/' + str(sVideoId) + '/version/0'
    
def playVideo():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('videoUrl')):
        videoUrl = oInputParameterHandler.getValue('videoUrl')

        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_NAME)
        oGuiElement.setMediaUrl(videoUrl)

        oPlayer = cPlayer()
        oPlayer.addItemToPlaylist(oGuiElement)
        oPlayer.startPlayer()
        return

    oGui.setEndOfDirectory()