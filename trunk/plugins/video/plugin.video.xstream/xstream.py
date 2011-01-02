from resources.lib.statistic import cStatistic
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.gui import cGui
from resources.lib.handler.pluginHandler import cPluginHandler
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
import logger


def run():
        logger.info('xtream started ...')

        parseUrl()

def runTestPlugin(oGui):
    oGuiElement = cGuiElement()
    oGuiElement.setTitle('testPlugin')
    oGuiElement.setSiteName('test')
    oGuiElement.setFunction('load')
    oGui.addFolder(oGuiElement)

def parseUrl():
    oInputParameterHandler = cInputParameterHandler()

    if (oInputParameterHandler.exist('function')):
            sFunction = oInputParameterHandler.getValue('function')
    else:
            logger.info('call load methode')
            sFunction = "load"

    if (oInputParameterHandler.exist('site')):
            sSiteName = oInputParameterHandler.getValue('site')
            logger.info('load sitename ' + sSiteName + ' and call function ' + sFunction)

            if (sFunction == 'load'):
                cStatistic().callStartPlugin(sSiteName)

            #try:
            exec "import " + sSiteName + " as plugin"
            exec "plugin."+ sFunction +"()"
            #except:
            #    logger.fatal('could not load site: ' + sSiteName )
    else:
            oGui = cGui()
            oPluginHandler = cPluginHandler()
            aPlugins = oPluginHandler.getAvailablePlugins()
            if (len(aPlugins) == 0):
                oGui.openSettings()
            else:
                for aPlugin in aPlugins:
                    oGuiElement = cGuiElement()
                    oGuiElement.setTitle(aPlugin[0])
                    oGuiElement.setSiteName(aPlugin[1])
                    oGuiElement.setFunction(sFunction)
                    oGui.addFolder(oGuiElement)

            # TEST PLUGIN
            #runTestPlugin(oGui)

            oGui.setEndOfDirectory()