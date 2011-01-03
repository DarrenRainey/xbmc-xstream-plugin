from resources.lib.player import cPlayer
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.config import cConfig
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.parser import cParser
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.gui import cGui
import logger

SITE_NAME = 'myp2p_eu'

URL_MAIN = 'http://www.myp2p.eu/'
URL_COUNTRY_SITE = 'http://www.myp2p.eu/channel.php?&part=channel&sel_country=yes'

def load():
    logger.info('load myp2peu :)')

    oConfig = cConfig()
    oGui = cGui()

    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_NAME)
    oGuiElement.setFunction('showCountrySite')
    oGuiElement.setTitle(oConfig.getLocalizedString(30402))
    oGui.addFolder(oGuiElement)

    oGui.setEndOfDirectory()

def showCountrySite():
    oGui = cGui()

    sPattern = '<td onclick="window.location.href=\'([^;]+)\'; return false;" style="cursor: pointer; padding-top: 1px; padding-bottom: 1px;"><div style="width: 25px; margin-right: 15px; float: left;"><img src="([^"]+)" border="1" /></div>([^<]+)</td>'
   
    # request
    oRequest = cRequestHandler(URL_COUNTRY_SITE)
    sHtmlContent = oRequest.request()
  
    # parse content
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

     
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_NAME)
            oGuiElement.setFunction('showSubChannels')
            oGuiElement.setTitle(aEntry[2])
            oGuiElement.setThumbnail(aEntry[1])

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('channelUrl', URL_MAIN + str(aEntry[0]))
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSubChannels():
    oConfig = cConfig()
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('channelUrl')):
        sChanellUrl = oInputParameterHandler.getValue('channelUrl')

        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_NAME)
        oGuiElement.setFunction('parseSubChannels')
        oGuiElement.setTitle('nicht zugeordnet')
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('channelUrl', sChanellUrl)
        oOutputParameterHandler.addParameter('channelType', 0)
        oGui.addFolder(oGuiElement, oOutputParameterHandler)

        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_NAME)
        oGuiElement.setFunction('parseSubChannels')
        oGuiElement.setTitle('Unterhaltung')
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('channelUrl', sChanellUrl)
        oOutputParameterHandler.addParameter('channelType', 1)
        oGui.addFolder(oGuiElement, oOutputParameterHandler)

        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_NAME)
        oGuiElement.setFunction('parseSubChannels')
        oGuiElement.setTitle('Kinder')
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('channelUrl', sChanellUrl)
        oOutputParameterHandler.addParameter('channelType', 2)
        oGui.addFolder(oGuiElement, oOutputParameterHandler)

        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_NAME)
        oGuiElement.setFunction('parseSubChannels')
        oGuiElement.setTitle('Musik')
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('channelUrl', sChanellUrl)
        oOutputParameterHandler.addParameter('channelType', 3)
        oGui.addFolder(oGuiElement, oOutputParameterHandler)

        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_NAME)
        oGuiElement.setFunction('parseSubChannels')
        oGuiElement.setTitle('Nachrichten')
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('channelUrl', sChanellUrl)
        oOutputParameterHandler.addParameter('channelType', 4)
        oGui.addFolder(oGuiElement, oOutputParameterHandler)

        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_NAME)
        oGuiElement.setFunction('parseSubChannels')
        oGuiElement.setTitle('Sport')
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('channelUrl', sChanellUrl)
        oOutputParameterHandler.addParameter('channelType', 5)
        oGui.addFolder(oGuiElement, oOutputParameterHandler)

        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_NAME)
        oGuiElement.setFunction('parseSubChannels')
        oGuiElement.setTitle('Alle anzeigen')
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('channelUrl', sChanellUrl)
        oOutputParameterHandler.addParameter('channelType', 6)
        oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def parseSubChannels():
    oConfig = cConfig()
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('channelUrl') and oInputParameterHandler.exist('channelType')):
        sChanellUrl = oInputParameterHandler.getValue('channelUrl')

        iChannelType = oInputParameterHandler.getValue('channelType')

        sCategoryName = 'No category'

        if (iChannelType == '0'):
            sCategoryName = 'No category'

        if (iChannelType == '1'):
            sCategoryName = 'Entertainment'

        if (iChannelType == '2'):
            sCategoryName = 'Kids'

        if (iChannelType == '3'):
            sCategoryName = 'Music'

        if (iChannelType == '4'):
            sCategoryName = 'News'

        if (iChannelType == '5'):
            sCategoryName = 'Sports'

        if (iChannelType == '5'):
            sCategoryName = '.+?'

        sPattern ='<tr><td class="competition"[^>]+>' + str(sCategoryName) + '</td></tr><tr><td></td><td><table[^>]+>(.+?)</table>'

        # request
        oRequest = cRequestHandler(sChanellUrl)
        sHtmlContent = oRequest.request()

        # parse content
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        

        if (aResult[0] == True):
            for aEntry in aResult[1]:
                sHtmlContent = aEntry                
                sPattern = '<td onclick="window.open\(\\\'([^\']+)\\\'\); return false;" style="cursor: pointer; padding-top: 1px; padding-bottom: 1px;">([^"]+)</td>'

                oParser = cParser()
                aResult = oParser.parse(sHtmlContent, sPattern)
                
                if (aResult[0] == True):
                    for aEntry in aResult[1]:
                        #if (aEntry[0][0:3] == 'mms') or (aEntry[0][0:4] == 'rtsp'):
                        oGuiElement = cGuiElement()
                        oGuiElement.setSiteName(SITE_NAME)
                        oGuiElement.setFunction('playStream')
                        oGuiElement.setTitle(aEntry[1])
                        oOutputParameterHandler = cOutputParameterHandler()
                        oOutputParameterHandler.addParameter('playUrl', aEntry[0])
                        oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def playStream():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('playUrl')):
        playUrl = oInputParameterHandler.getValue('playUrl')

        oPlayer = cPlayer()
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_NAME)
        oGuiElement.setMediaUrl(playUrl)
        oPlayer.addItemToPlaylist(oGuiElement)
        oPlayer.startPlayer()
        return
        
    oGui.setEndOfDirectory()