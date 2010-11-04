from resources.lib.config import cConfig
import sys

class cPluginHandler:

    def getPluginHandle(self):
        try:
                return int( sys.argv[ 1 ] )
        except:
                return 0

    def getPluginPath(self):
        try:
                return sys.argv[0]
        except:
                return ''

    def getAvailablePlugins(self):
        oConfig = cConfig()
        aPlugins = []

        bPlugin = oConfig.getSetting('plugin_kino_to')        
        if (bPlugin == 'true'):
            aPlugins.append(self.__createAvailablePluginsItem('30201', 'kino_to'))

        bPlugin = oConfig.getSetting('plugin_southpark_de')
        if (bPlugin == 'true'):
            aPlugins.append(self.__createAvailablePluginsItem('30202', 'southpark_de'))

        bPlugin = oConfig.getSetting('plugin_myp2p_eu')
        if (bPlugin == 'true'):
            aPlugins.append(self.__createAvailablePluginsItem('30203', 'myp2p_eu'))

        bPlugin = oConfig.getSetting('plugin_gstream_in')
        if (bPlugin == 'true'):
            aPlugins.append(self.__createAvailablePluginsItem('30204', 'gstream_in'))

        bPlugin = oConfig.getSetting('plugin_nba_de')
        if (bPlugin == 'true'):
            aPlugins.append(self.__createAvailablePluginsItem('30205', 'nba_de'))

        bPlugin = oConfig.getSetting('plugin_bundesliga_de')
        if (bPlugin == 'true'):
            aPlugins.append(self.__createAvailablePluginsItem('30206', 'bundesliga_de'))

        bPlugin = oConfig.getSetting('plugin_mtv_de')
        if (bPlugin == 'true'):
            aPlugins.append(self.__createAvailablePluginsItem('30207', 'mtv_de'))

        bPlugin = oConfig.getSetting('plugin_kino_de')
        if (bPlugin == 'true'):
            aPlugins.append(self.__createAvailablePluginsItem('30208', 'kino_de'))

        bPlugin = oConfig.getSetting('plugin_bild_de')
        if (bPlugin == 'true'):
            aPlugins.append(self.__createAvailablePluginsItem('30209', 'bild_de'))

        bPlugin = oConfig.getSetting('plugin_moviemaze_de')
        if (bPlugin == 'true'):
            aPlugins.append(self.__createAvailablePluginsItem('30210', 'moviemaze_de'))

        bPlugin = oConfig.getSetting('plugin_shoutcast_com')
        if (bPlugin == 'true'):
            aPlugins.append(self.__createAvailablePluginsItem('30211', 'shoutcast_com'))

        bPlugin = oConfig.getSetting('plugin_movie2k_com')
        if (bPlugin == 'true'):
            aPlugins.append(self.__createAvailablePluginsItem('30212', 'movie2k_com'))

        bPlugin = oConfig.getSetting('plugin_simpsons_to')
        if (bPlugin == 'true'):
            aPlugins.append(self.__createAvailablePluginsItem('30213', 'simpsons_to'))

        return aPlugins

    def __createAvailablePluginsItem(self, iPluginStringId, sPluginIdentifier):
        oConfig = cConfig()
        sPluginName = oConfig.getLocalizedString(int(iPluginStringId))

        aPluginEntry = []
        aPluginEntry.append(sPluginName)
        aPluginEntry.append(sPluginIdentifier)
        return aPluginEntry