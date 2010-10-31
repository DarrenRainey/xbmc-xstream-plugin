import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import urllib

try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""


class cGui:
    DEFAULT_FOLDER_ICON = 'DefaultFolder.png'

    def addSimpleFolder(self, sSiteName, sFunctionName, sTitle, aParams = {}):
        
        listitem = xbmcgui.ListItem( sTitle, iconImage = self.DEFAULT_FOLDER_ICON, thumbnailImage='' )
        listitem.setInfo('video', {'Title' : sTitle, 'Plot' : '', 'Studio' : '' })

        sItemUrl = self.__createItemUrl(sSiteName, sFunctionName, sTitle, aParams)
        xbmcplugin.addDirectoryItem(handle = pluginhandle, url = sItemUrl, listitem = listitem, isFolder = True)

        xbmc.output(sItemUrl)

        return True

    def addMovieFolder(self, sSiteName, sFunctionName, oMovieModel):
        listitem = xbmcgui.ListItem(oMovieModel.getTitle(), iconImage = self.DEFAULT_FOLDER_ICON, thumbnailImage='' )
        listitem.setInfo('video', {'Title' : oMovieModel.getTitle(), 'Plot' : '', 'Studio' : '' })

        aParams = {'url' : urllib.unquote_plus(oMovieModel.getUrl())}
        sItemUrl = self.__createItemUrl(sSiteName, sFunctionName, oMovieModel.getTitle(), aParams)
        xbmcplugin.addDirectoryItem(handle = pluginhandle, url = sItemUrl, listitem = listitem, isFolder = True)

        xbmc.output(sItemUrl)

        return True

    def __createItemUrl(self, sSiteName, sFunctionName, sTitle, aParams = {}):
        sParams = 'params=0'
        if len(aParams) > 0:
                sParams = urllib.urlencode(aParams)

        if (len(sFunctionName) == 0):
                sItemUrl = '%s?site=%s&title=%s&%s' % ( sys.argv[ 0 ] , sSiteName , urllib.quote_plus(sTitle), sParams)
        else:
                sItemUrl = '%s?site=%s&function=%s&title=%s&%s' % ( sys.argv[ 0 ] , sSiteName , sFunctionName , urllib.quote_plus(sTitle), sParams)
        return sItemUrl