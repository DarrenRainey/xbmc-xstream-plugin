from resources.lib.config import cConfig
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.pluginHandler import cPluginHandler
import urllib
import xbmcgui
import xbmcplugin
import xbmc

class cGui:

    def addFolder(self, oGuiElement, oOutputParameterHandler = ''):
            sItemUrl = self.__createItemUrl(oGuiElement, oOutputParameterHandler)
            oListItem = self.createListItem(oGuiElement)

            oListItem = self.__createContextMenu(oGuiElement, oListItem)

            sPluginHandle = cPluginHandler().getPluginHandle();
            xbmcplugin.addDirectoryItem(sPluginHandle, sItemUrl, oListItem, True)

    def createListItem(self, oGuiElement):
            oListItem = xbmcgui.ListItem(oGuiElement.getTitle(), oGuiElement.getTitleSecond(), oGuiElement.getIcon(), oGuiElement.getThumbnail())
            oListItem.setInfo(oGuiElement.getType(), oGuiElement.getItemValues())

            aProperties = oGuiElement.getItemProperties()
            for sPropertyKey in aProperties.keys():
                oListItem.setProperty(sPropertyKey, aProperties[sPropertyKey])

            return oListItem

    def __createContextMenu(self, oGuiElement, oListItem):
            if (len(oGuiElement.getContextItems()) > 0):
                for oContextItem in oGuiElement.getContextItems():
                    sPluginPath = cPluginHandler().getPluginPath();
                    oOutputParameterHandler = oContextItem.getOutputParameterHandler()
                    sParams = oOutputParameterHandler.getParameterAsUri()
                    sTest = '%s?site=%s&function=%s&%s' % (sPluginPath, oContextItem.getFile(), oContextItem.getFunction(), sParams)

                    aContextMenus = []
                    aContextMenus+= [ ( oContextItem.getTitle(), "XBMC.RunPlugin(%s)" % (sTest,),)]

                oListItem.addContextMenuItems(aContextMenus, True)
            else:
                aContextMenus = []
                oListItem.addContextMenuItems(aContextMenus, True)

            return oListItem

    def setEndOfDirectory(self):
            iHandler = cPluginHandler().getPluginHandle()
            xbmcplugin.setPluginCategory(iHandler, "" )
            xbmcplugin.addSortMethod(iHandler, xbmcplugin.SORT_METHOD_NONE )
            xbmcplugin.endOfDirectory(iHandler, True )

    def __createItemUrl(self, oGuiElement, oOutputParameterHandler = ''):
            if (oOutputParameterHandler == ''):
                    oOutputParameterHandler = cOutputParameterHandler()
                    
            sParams = oOutputParameterHandler.getParameterAsUri()
            sPluginPath = cPluginHandler().getPluginPath();

            if (len(oGuiElement.getFunction()) == 0):
                     sItemUrl = '%s?site=%s&title=%s&%s' % (sPluginPath, oGuiElement.getSiteName(), urllib.quote_plus(oGuiElement.getTitle()), sParams)
            else:
                     sItemUrl = '%s?site=%s&function=%s&title=%s&%s' % (sPluginPath, oGuiElement.getSiteName(), oGuiElement.getFunction(), urllib.quote_plus(oGuiElement.getTitle()), sParams)

            #logger.logInfo(sItemUrl)
            return sItemUrl

    def showKeyBoard(self, sDefaultText = ''):
            keyboard = xbmc.Keyboard(sDefaultText)
            keyboard.doModal()
            if (keyboard.isConfirmed()):
                sSearchText = keyboard.getText()
                if (len(sSearchText)) > 0:
                    return sSearchText

            return False

    def openSettings(self):
            cConfig().showSettingsWindow()

    def showNofication(self, sTitle, iSeconds = 0):
        if (cConfig().isDharma() == False):
            return

	if (iSeconds == 0):
            iSeconds = 1000
	else:
            iSeconds = iSeconds * 1000
        
        xbmc.executebuiltin("Notification(%s,%s,%s)" % (cConfig().getLocalizedString(30308), (cConfig().getLocalizedString(30309) % str(sTitle)), iSeconds))