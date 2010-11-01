from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.parser import cParser
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.gui import cGui
from resources.lib.player import cPlayer
from resources.lib.gui.contextElement import cContextElement
from resources.lib.download import cDownload
import logger

SITE_NAME = 'movie2k_com'

URL_MAIN = 'http://www.movie2k.com/'
URL_TOP_MOVIES = 'http://www.movie2k.com/movies-top.html'
URL_GENRE = 'http://www.movie2k.com/genres-movies.html'
URL_MOVIES_ALL_WITH_CHARACTER = 'http://www.movie2k.com/movies-all'

URL_SERIES = 'http://www.movie2k.com/tvshows_featured.php'
URL_SERIES_ALL = 'http://www.movie2k.com/tvshows-all.html'
URL_SERIES_TOP = 'http://www.movie2k.com/tvshows-top.html'
URL_SERIES_GENRE = 'http://www.movie2k.com/genres-tvshows.html'

URL_SEARCH = 'http://www.movie2k.com/movies.php?list=searchnew534'

def load():
    logger.info('load movie2k.com :)')

    oGui = cGui()
    __createMainMenuItem(oGui, 'Filme', '', 'showMovieMenu')
    __createMainMenuItem(oGui, 'Serien', '', 'showSeriesMenu')
    __createMainMenuItem(oGui, 'Suche', '', 'showSearch')
    oGui.setEndOfDirectory()

def showMovieMenu():
    oGui = cGui()
    __createMainMenuItem(oGui, 'Kinofilme', URL_MAIN, 'showMoviesAndSeries')
    __createMainMenuItem(oGui, 'Alle Filme', URL_MAIN, 'showCharcacters')
    __createMainMenuItem(oGui, 'Top Filme', URL_TOP_MOVIES, 'parseMovieSimpleList')
    __createMainMenuItem(oGui, 'Genre', URL_GENRE, 'showGenre')
    oGui.setEndOfDirectory()

def showSeriesMenu():
    oGui = cGui()
    __createMainMenuItem(oGui, 'Featured', URL_SERIES, 'showMoviesAndSeries')
    __createMainMenuItem(oGui, 'Alle Serien', URL_SERIES_ALL, 'showAllSeries')
    __createMainMenuItem(oGui, 'Top Serien', URL_SERIES_TOP, 'parseMovieSimpleList')
    __createMainMenuItem(oGui, 'Genre', URL_SERIES_GENRE, 'showGenre')
    oGui.setEndOfDirectory()


def showCharcacters():
    oGui = cGui()
    __createCharacters(oGui, '#')
    __createCharacters(oGui, 'A')
    __createCharacters(oGui, 'B')
    __createCharacters(oGui, 'C')
    __createCharacters(oGui, 'D')
    __createCharacters(oGui, 'E')
    __createCharacters(oGui, 'F')
    __createCharacters(oGui, 'G')
    __createCharacters(oGui, 'H')
    __createCharacters(oGui, 'I')
    __createCharacters(oGui, 'J')
    __createCharacters(oGui, 'K')
    __createCharacters(oGui, 'L')
    __createCharacters(oGui, 'N')
    __createCharacters(oGui, 'O')
    __createCharacters(oGui, 'Q')
    __createCharacters(oGui, 'R')
    __createCharacters(oGui, 'S')
    __createCharacters(oGui, 'T')
    __createCharacters(oGui, 'U')
    __createCharacters(oGui, 'V')
    __createCharacters(oGui, 'W')
    __createCharacters(oGui, 'X')
    __createCharacters(oGui, 'Y')
    __createCharacters(oGui, 'Z')    
    oGui.setEndOfDirectory()

def __createCharacters(oGui, sCharacter):
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_NAME)
    oGuiElement.setFunction('parseMovieSimpleList')
    oGuiElement.setTitle(sCharacter)

    if (sCharacter == '#'):
        sUrl = URL_MOVIES_ALL_WITH_CHARACTER + '-1-1.html'
    else:
        sUrl = URL_MOVIES_ALL_WITH_CHARACTER + '-' + str(sCharacter) + '-1.html'

    oOutputParameterHandler = cOutputParameterHandler()    
    oOutputParameterHandler.addParameter('sUrl', sUrl)
    oGui.addFolder(oGuiElement, oOutputParameterHandler)

def showAllSeries():
    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('sUrl')):
        sUrl = oInputParameterHandler.getValue('sUrl')

        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()
        __parseMovieSimpleList(sHtmlContent, 1)

def showSearch():
    logger.info('show keyboard')
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        __callSearch(sSearchText)

    oGui.setEndOfDirectory()

def __callSearch(sSearchText):
    oRequest = cRequestHandler(URL_SEARCH)
    oRequest.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
    oRequest.addParameters('search', sSearchText)
    sHtmlContent = oRequest.request()

    __parseMovieSimpleList(sHtmlContent, 1)
    

def __checkForNextPage(sHtmlContent, iCurrentPage):
    iNextPage = int(iCurrentPage) + 1
    iNextPage = str(iNextPage) + ' '
    
    sPattern = '<a href="([^"]+)">' + iNextPage + '</a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]
    return False

def showGenre():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('sUrl')):
        sUrl = oInputParameterHandler.getValue('sUrl')

        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()

        sPattern = '<TR>.*?<a href="([^"]+)">(.*?)</a>.*?<TD id="tdmovies" width="50">(.*?)</TD>'

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
            for aEntry in aResult[1]:
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_NAME)
                oGuiElement.setFunction('parseMovieSimpleList')

                sTitle = aEntry[1] + ' (' + aEntry[2] + ')'

                oGuiElement.setTitle(sTitle)

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('sUrl', URL_MAIN + aEntry[0])
                oGui.addFolder(oGuiElement, oOutputParameterHandler)

        oGui.setEndOfDirectory()

def parseMovieSimpleList():
    oInputParameterHandler = cInputParameterHandler()

    if (oInputParameterHandler.exist('iPage')):
        iPage = oInputParameterHandler.getValue('iPage')
    else:
        iPage = 1

    if (oInputParameterHandler.exist('sUrl')):
        sUrl = oInputParameterHandler.getValue('sUrl')

        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()

        __parseMovieSimpleList(sHtmlContent, iPage)

def __parseMovieSimpleList(sHtmlContent, iPage):
    oGui = cGui()
    sPattern = '<TR>.*?<a href="([^"]+)">(.*?)</a>.*?<img border=0 src="http://www.movie2k.com/img/(.*?).png'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_NAME)
            oGuiElement.setFunction('showHoster')

            sTitle = aEntry[1].strip().replace('\t', '') +  __getLanmguage(aEntry[2])
            oGuiElement.setTitle(sTitle)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('sUrl', aEntry[0])
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

    sNextUrl = __checkForNextPage(sHtmlContent, iPage)    
    if (sNextUrl != False):
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_NAME)
        oGuiElement.setFunction('parseMovieSimpleList')
        oGuiElement.setTitle('next ..')

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sUrl', sNextUrl)
        oOutputParameterHandler.addParameter('iPage', int(iPage) + 1)
        oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMoviesAndSeries():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('sUrl')):
        sUrl = oInputParameterHandler.getValue('sUrl')


        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()

        sPattern = '<div style="float:left"><a href="([^"]+)".{0,1}><img src="([^"]+)".*?alt="([^"]+)".*?<img src="http://www.movie2k.com/img/(.*?).png"'

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
            for aEntry in aResult[1]:
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_NAME)
                oGuiElement.setFunction('showHoster')

                sThumbnail = URL_MAIN + aEntry[1]
                oGuiElement.setThumbnail(sThumbnail)

                sTitle = aEntry[2].strip().replace('kostenlos', '') +  __getLanmguage(aEntry[3])
                oGuiElement.setTitle(sTitle)

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('sUrl', aEntry[0])
                oGui.addFolder(oGuiElement, oOutputParameterHandler)

        oGui.setEndOfDirectory()

def showHoster():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('sUrl')):
        sUrl = oInputParameterHandler.getValue('sUrl')
        
        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()
        
        sPattern = '<tr id="tablemoviesindex2">.*?<a href="([^"]+)">([^<]+)<.*?width="16">(.*?)</a>.*?alt="([^"]+)"'
        #sPattern = '<tr id="tablemoviesindex2">.*?<a href="([^"]+)">.*?width="16">(.*?)</a>.*?alt="([^"]+)"'

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        if (aResult[0] == True):
            for aEntry in aResult[1]:
                sHoster = aEntry[2].strip()
                if (__checkHoster(sHoster) == True):

                    oGuiElement = cGuiElement()
                    oGuiElement.setSiteName(SITE_NAME)
                    oGuiElement.setFunction('play')

                    sTitle = aEntry[1] + ' - ' + aEntry[2] + ' - ' + aEntry[3]
                    oGuiElement.setTitle(sTitle)

                    sUrl = URL_MAIN + aEntry[0]

                    oContextElement = cContextElement()
                    oContextElement.setTitle('Download')
                    oContextElement.setFile(SITE_NAME)
                    oContextElement.setFunction('play')
                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('sUrl', sUrl)
                    oOutputParameterHandler.addParameter('sTitle', sTitle)
                    oOutputParameterHandler.addParameter('bDownload', 'True')
                    oOutputParameterHandler.addParameter('sHoster', sHoster)
                    oContextElement.setOutputParameterHandler(oOutputParameterHandler)
                    oGuiElement.addContextItem(oContextElement)
                    
                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('sUrl', sUrl)
                    oOutputParameterHandler.addParameter('sTitle', sTitle)
                    oOutputParameterHandler.addParameter('sHoster', sHoster)
                    oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def __checkHoster(sHoster):
    if (sHoster == 'Mystream'):
        return True

    if (sHoster == 'loaded.it'):
        return True

    if (sHoster == 'Novamov'):
        return True

    if (sHoster == 'Stream2k'):
        return True

    #if (sHoster == 'UploadC'):
    #    return True

    #if (sHoster == 'Loombo'):
    #    return True

    if (sHoster == 'VideoWeed'):
        return True

    if (sHoster == 'Streamesel'):
        return True

    if (sHoster == 'MegaVideo'):
        return True

    if (sHoster == 'Duckload'):
        return True

    if (sHoster == 'Movshare'):
        return True

    if (sHoster == 'FileStage'):
        return True

    if (sHoster == 'Tubeload'):
        return True

    if (sHoster == 'Screen4u'):
        return True

    if (sHoster == 'CheckThisV'):
        return True

    return False


def play():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('sUrl') and oInputParameterHandler.exist('sHoster')):
        sUrl = oInputParameterHandler.getValue('sUrl')
        sHoster = oInputParameterHandler.getValue('sHoster')
        sTitle = oInputParameterHandler.getValue('sTitle')

        bDownload = False
        if (oInputParameterHandler.exist('bDownload')):
            bDownload = True
        
        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()

        # mystream.to
        if (sHoster == 'Mystream'):            
            sPattern = '<a href="http://www.mystream.to/([^"]+)"'
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                sStreamUrl = 'http://www.mystream.to/' + aResult[1][0]
                __play('mystream', sStreamUrl, sTitle, bDownload)
                return

        # loaded.it
        if (sHoster == 'loaded.it'):
            sPattern = '<a href="http://loaded.it/([^"]+)"'
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                sStreamUrl = 'http://loaded.it/' + aResult[1][0]
                __play('loadedit', sStreamUrl, sTitle, bDownload)
                return

        # novamov.com
        if (sHoster == 'Novamov'):
            sPattern = "src='http://www.novamov.com/([^']+)'"
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                sStreamUrl = 'http://www.novamov.com/' + aResult[1][0]
                __play('novamov', sStreamUrl, sTitle, bDownload)
                return

        # Stream2k.com
        if (sHoster == 'Stream2k'):
            sPattern = '<param name="flashvars" value="config=.*?stream2k.com/([^"]+)"'
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                sStreamUrl = 'http://www.stream2k.com/' + aResult[1][0]
                __play('stream2k', sStreamUrl, sTitle, bDownload)
                return
            
        # Videoweed.com
        if (sHoster == 'VideoWeed'):
            sPattern = 'src="http://www.videoweed.com/([^"]+)"'
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                sStreamUrl = 'http://www.videoweed.com/' + aResult[1][0]
                __play('videoweed', sStreamUrl, sTitle, bDownload)
                return
            
        # Uploadc.com MUSS >NOCH
        if (sHoster == 'UploadC'):
            sPattern = '<a href="http://uploadc.com/([^"]+)"'
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                sStreamUrl = 'http://uploadc.com/' + aResult[1][0]
                __play('uploadc', sStreamUrl, sTitle, bDownload)
                return

        # Loombo.com MUSS NOCH
        if (sHoster == 'Loombo'):
            sPattern = '<a href="http://loombo.com/([^"]+)"'
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                sStreamUrl = 'http://loombo.com/' + aResult[1][0]
                __play('loombo', sStreamUrl, sTitle, bDownload)
                return

        # streamesel.com
        if (sHoster == 'Streamesel'):
            sPattern = '<a href="http://www.streamesel.com/([^"]+)"'
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                sStreamUrl = 'http://www.streamesel.com/' + aResult[1][0]
                __play('streamesel', sStreamUrl, sTitle, bDownload)
                return
            
        
        # MegaVideo.com
        if (sHoster == 'MegaVideo'):           
            sPattern = 'value="http://www.megavideo.com/v/([^"]+)"'
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                sStreamUrl = aResult[1][0]
                __play('megavideo', sStreamUrl,sTitle, bDownload)
                return
        
         # Duckload.com
        if (sHoster == 'Duckload'):
            sPattern = '<a href="http://duckload.com/([^"]+)"'
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)          
            if (aResult[0] == True):
                sStreamUrl = 'http://www.duckload.com/' + aResult[1][0]
                __play('duckload', sStreamUrl,sTitle, bDownload)
                return

            sPattern = '<a href="http://www.duckload.com/([^"]+)"'
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)           
            if (aResult[0] == True):
                sStreamUrl = 'http://www.duckload.com/' + aResult[1][0]
                __play('duckload', sStreamUrl,sTitle, bDownload)
                return

        if (sHoster == 'Movshare'):          
            sPattern = 'src="http://www.movshare.net/([^"]+)"'
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                sStreamUrl = 'http://www.movshare.net/' + aResult[1][0]
                __play('movshare', sStreamUrl,sTitle, bDownload)
                return            
        
            sPattern = "src='http://www.movshare.net/([^']+)'"
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                sStreamUrl = 'http://www.movshare.net/' + aResult[1][0]
                __play('movshare', sStreamUrl,sTitle, bDownload)
                return

        if (sHoster == 'FileStage'):
            sPattern = '<a href="http://www.filestage.to/([^"]+)"'
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                sStreamUrl = 'http://www.filestage.to/' + aResult[1][0]
                __play('filestage', sStreamUrl,sTitle, bDownload)
                return

        if (sHoster == 'Tubeload'):
            sPattern = '<a href="http://www.tubeload.to/([^"]+)"'
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                sStreamUrl = 'http://www.tubeload.to/' + aResult[1][0]
                __play('tubeload', sStreamUrl,sTitle, bDownload)
                return

        if (sHoster == 'Screen4u'):
            sPattern = '<a href="http://www.screen4u.net/([^"]+)"'
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                sStreamUrl = 'http://www.screen4u.net/' + aResult[1][0]
                __play('screen4u', sStreamUrl,sTitle, bDownload)
                return

        if (sHoster == 'CheckThisV'):
            sPattern = '<a href="http://www.checkthisvid.com/([^"]+)"'
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                sStreamUrl = 'http://www.checkthisvid.com/' + aResult[1][0]
                __play('checkthisvid', sStreamUrl,sTitle, bDownload)
                return

    oGui.setEndOfDirectory()


def __play(sHosterFileName, linkToHosterMediaFile, sTitle, bDownload):
    oGui = cGui()

    exec "from " + sHosterFileName + " import cHoster"
    print 'load hoster ' + sHosterFileName
    oHoster = cHoster()
    oHoster.setUrl(linkToHosterMediaFile)
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

def __getLanmguage(sString):
    if (sString == 'us_ger_small'):
        return ' (DE)'
    return ' (EN)'

def __createMainMenuItem(oGui, sTitle, sUrl, sFunction):
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_NAME)
    oGuiElement.setFunction(sFunction)
    oGuiElement.setTitle(sTitle)
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('sUrl', sUrl)    
    oGui.addFolder(oGuiElement, oOutputParameterHandler)


