from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.config import cConfig
from xstream import logger
from resources.lib.gui.gui import cGui
import xbmc

class cPlayer:
    def __init__(self):
        self.clearPlayList()

    def clearPlayList(self):
        oPlaylist = self.__getPlayList()
	oPlaylist.clear()

    def __getPlayList(self):
        return xbmc.PlayList(xbmc.PLAYLIST_VIDEO)

    def addItemToPlaylist(self, oGuiElement):
        logger.info('add item to playlist')

        oGui = cGui()
        oListItem =  oGui.createListItem(oGuiElement)
        self.__addItemToPlaylist(oGuiElement, oListItem)    

    def __addItemToPlaylist(self, oGuiElement, oListItem):
        logger.info('addItemToPlaylist')
    
	oPlaylist = self.__getPlayList()	
	oPlaylist.add(oGuiElement.getMediaUrl(), oListItem )

    def startPlayer(self):
        logger.info('start player')
        sPlayerType = self.__getPlayerType()
        xbmcPlayer = xbmc.Player(sPlayerType)
        oPlayList = self.__getPlayList()
	xbmcPlayer.play(oPlayList)


        # dirty, but is works 
        if (cConfig().isDharma() == False):
            oInputParameterHandler = cInputParameterHandler()
            aParams = oInputParameterHandler.getAllParameter()

            oGui = cGui()
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(aParams['site'])
            oGuiElement.setFunction(aParams['function'])
            oGui.addFolder(oGuiElement)
            oGui.setEndOfDirectory()


    def __getPlayerType(self):
        oConfig = cConfig()
        sPlayerType = oConfig.getSetting('playerType')
        logger.info('playertype from config: ' + sPlayerType)

        if (sPlayerType == '0'):
            return xbmc.PLAYER_CORE_AUTO

        if (sPlayerType == '1'):
            return xbmc.PLAYER_CORE_MPLAYER

        if (sPlayerType == '2'):
            return xbmc.PLAYER_CORE_DVDPLAYER
