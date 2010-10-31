import urllib
import logger
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.player import cPlayer

SITE_NAME = 'kino_to'
URL_MAIN = 'http://kino.to'
URL_CINEMA_PAGE = 'http://kino.to/Cinemas.html'
URL_GENRE_PAGE = 'http://kino.to/Genre.html'
URL_MOVIE_PAGE = 'http://kino.to/Movies.html'
URL_SERIE_PAGE = 'http://kino.to/Series.html'
URL_DOCU_PAGE = 'http://kino.to/Documentation.html'

URL_FAVOURITE_MOVIE_PAGE = 'http://kino.to/FavoredMovies.html'
URL_FAVOURITE_SERIE_PAGE = 'http://kino.to/FavoredSeries.html'
URL_FAVOURITE_DOCU_PAGE = 'http://kino.to/FavoredDocus.html'

URL_SEARCH = 'http://kino.to/Search.html'
URL_MIRROR = 'http://kino.to/aGET/Mirror/'
URL_EPISODE_URL = 'http://kino.to/aGET/MirrorByEpisode/'
URL_AJAX = 'http://kino.to/aGET/List/'
URL_LANGUAGE = 'http://kino.to/aSET/PageLang/1'

def load():
    logger.info('load kinoto :)')
        
    __initSiteLanguage()
   
    oGui = cGui()

    __createMenuEntry(oGui, 'displayCinemaSite', 'Aktuelle KinoFilme')
    __createMenuEntry(oGui, 'displayGenreSite', 'Kategorien')

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MOVIE_PAGE)
    oOutputParameterHandler.addParameter('page', 1)
    oOutputParameterHandler.addParameter('mediaType', 'movie')
    __createMenuEntry(oGui, 'displayCharacterSite', 'Filme', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SERIE_PAGE)
    oOutputParameterHandler.addParameter('page', 1)
    oOutputParameterHandler.addParameter('mediaType', 'series')
    __createMenuEntry(oGui, 'displayCharacterSite', 'Serien', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_DOCU_PAGE)
    oOutputParameterHandler.addParameter('page', 1)
    oOutputParameterHandler.addParameter('mediaType', 'documentation')
    __createMenuEntry(oGui, 'displayCharacterSite', 'Dokumentationen', oOutputParameterHandler)

    __createMenuEntry(oGui, 'displaySearchSite', 'Suche')
    
    oGui.setEndOfDirectory()

def __createMenuEntry(oGui, sFunction, sLabel, oOutputParameterHandler = ''):
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_NAME)
    oGuiElement.setFunction(sFunction)
    oGuiElement.setTitle(sLabel)    
    oGui.addFolder(oGuiElement, oOutputParameterHandler)

def __initSiteLanguage():
    oRequestHandler = cRequestHandler(URL_LANGUAGE)
    oRequestHandler.request()
	

def displaySearchSite():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        oRequestHandler = cRequestHandler(URL_SEARCH)
        oRequestHandler.addParameters('q', sSearchText)
        sRequestUri = oRequestHandler.getRequestUri();
        logger.info(sRequestUri)

        oRequest = cRequestHandler(sRequestUri)
        sHtmlContent = oRequest.request()

        # parse content
        sPattern = '<td class="Icon"><img width="16" height="11" src="http://res.kino.to/gr/sys/lng/([^"]+).png" alt="language"></td>.*?<td class="Title">.*?<a onclick="return false;" href="([^"]+)">([^<]+)</a>'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            for aEntry in aResult[1]:
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_NAME)
                oGuiElement.setFunction('parseMovieEntrySite')
                oGuiElement.setTitle(aEntry[2])

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('movieUrl', URL_MAIN + str(aEntry[1]))
                oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()
    

def displayCharacterSite():
    logger.info('load displayCharacterSite')
    sPattern = 'class="LetterMode.*?>([^>]+)</a>'
    oGui = cGui()
        
    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('siteUrl') and oInputParameterHandler.exist('page') and oInputParameterHandler.exist('mediaType')):
        siteUrl = oInputParameterHandler.getValue('siteUrl')
        iPage = oInputParameterHandler.getValue('page')
        sMediaType = oInputParameterHandler.getValue('mediaType')
                                
        # request
        oRequest = cRequestHandler(siteUrl)
        sHtmlContent = oRequest.request()

        # parse content
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
              
        if (aResult[0] == True):
            for aEntry in aResult[1]:
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_NAME)
                oGuiElement.setFunction('ajaxCall')
                oGuiElement.setTitle(aEntry[0])

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('character', aEntry[0])
                oOutputParameterHandler.addParameter('page', iPage)
                oOutputParameterHandler.addParameter('mediaType', sMediaType)
                oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def displayGenreSite():
    logger.info('load displayGenreSite')
    sPattern = '<td class="Title"><a href="/Genre/([^Poular]+)">([^"]+)</a>'

    # request
    oRequest = cRequestHandler(URL_GENRE_PAGE)
    sHtmlContent = oRequest.request()

    # parse content
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
        
    oGui = cGui()
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_NAME)
            oGuiElement.setFunction('showCharacters')
            oGuiElement.setTitle(aEntry[1])
 
            iGenreId = aEntry[0]
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('page', 1)            
            oOutputParameterHandler.addParameter('mediaType', 'fGenre')
            oOutputParameterHandler.addParameter('mediaTypePageId', iGenreId)
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def displayCinemaSite():
    logger.info('load displayCinemaSite')
    sPattern = '<div onclick="location.href=\'([^>]+)\';.*?<div class="Opt leftOpt Headlne"><h1>([^>]+)</h1></div>.*?<img src="([^"]+)" class="Thumb".*?"Descriptor">([^"]+)</div>'
        
    # request
    oRequest = cRequestHandler(URL_CINEMA_PAGE)
    sHtmlContent = oRequest.request()

    # parse content
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    oGui = cGui()
    # iterated result and create GuiElements
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_NAME)
            oGuiElement.setFunction('parseMovieEntrySite')
            oGuiElement.setTitle(aEntry[1])
            oGuiElement.setThumbnail(aEntry[2])
            oGuiElement.setDescription(aEntry[3])

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('movieUrl', URL_MAIN + str(aEntry[0]))
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()
        
def parseMovieEntrySite():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('movieUrl')):
        sUrl = oInputParameterHandler.getValue('movieUrl')

        # get movieEntrySite content
        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()

        bIsSerie = __isSerie(sHtmlContent)
        if (bIsSerie):
            aSeriesItems = parseSerieSite(sHtmlContent)
                        
            if (len(aSeriesItems) > 0):
                for aSeriesItem in aSeriesItems:
                    oGuiElement = cGuiElement()
                    oGuiElement.setSiteName(SITE_NAME)
                    oGuiElement.setTitle(aSeriesItem[0])
                    oGuiElement.setFunction('displayHoster')
                    
                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('sUrl', aSeriesItem[1])
                    oGui.addFolder(oGuiElement, oOutputParameterHandler)
        else:
            displayHoster(sHtmlContent)
            

    oGui.setEndOfDirectory()

def displayHoster(sHtmlContent = ''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('sUrl')):
        sUrl = oInputParameterHandler.getValue('sUrl')

        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()


    aHosters = __getMovieHoster(sHtmlContent);
    for aHoster in aHosters:
        if (len(aHoster) > 0):
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_NAME)
            oGuiElement.setTitle(aHoster[0])
            oGuiElement.setFunction('parseHosterSnippet')

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('hosterName', aHoster[0])
            oOutputParameterHandler.addParameter('hosterUrlSite', aHoster[1])
            oOutputParameterHandler.addParameter('hosterParserMethode', aHoster[2])
            oOutputParameterHandler.addParameter('hosterFileName', aHoster[3])
            oGui.addFolder(oGuiElement, oOutputParameterHandler)
    oGui.setEndOfDirectory()


def parseSerieSite(sHtmlContent):
    aSeriesItems = []

    sPattern = 'id="SeasonSelection" rel="([^"]+)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        aSeriesUrls = aResult[1][0].split("&amp;")
        sSeriesUrl = '&' + str(aSeriesUrls[1]) + '&' + str(aSeriesUrls[2])

        sPattern = '<option.*?rel="([^"]+)".*?>Staffel ([^<]+)</option'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            for aEntry in aResult[1]:
                aSeriesIds = aEntry[0].split(",")
                for iSeriesIds in aSeriesIds:
                    aSeries = []
                    iSeriesId = iSeriesIds
                    iSeasonId = aEntry[1]

                    sTitel = 'Staffel '+ str(iSeasonId) + ' - ' + str(iSeriesId)
                    sUrl = URL_EPISODE_URL + sSeriesUrl + '&Season=' + str(iSeasonId) + '&Episode=' + str(iSeriesId)

                    aSeries.append(sTitel)
                    aSeries.append(sUrl)
                    aSeriesItems.append(aSeries)
    return aSeriesItems        

def __isSerie(sHtmlContent):
    sPattern = 'id="SeasonSelection" rel="([^"]+)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
            return True
    else:
            return False
                

def parseHosterSnippet():
    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('hosterName')
        and oInputParameterHandler.exist('hosterUrlSite')
        and oInputParameterHandler.exist('hosterParserMethode')
        and oInputParameterHandler.exist('hosterFileName')):
        sHosterName = oInputParameterHandler.getValue('hosterName')
        sHosterUrlSite = oInputParameterHandler.getValue('hosterUrlSite')
        sHosterParserMethode = oInputParameterHandler.getValue('hosterParserMethode')
        sHosterFileName = oInputParameterHandler.getValue('hosterFileName')
        if (sHosterParserMethode == 'parseHosterDefault'):
            __parseHosterDefault(sHosterUrlSite, sHosterName, sHosterFileName, False)
        if (sHosterParserMethode == 'parseMegaVideoCom'):
            sPattern = 'value=\\\\"http:\\\\/\\\\/www.megavideo.com\\\\/v\\\\/([^"]+)\\\\'
            __parseHosterDefault(sHosterUrlSite, sHosterName, sHosterFileName, sPattern)


def playMovieFromHoster():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('sHosterFileName') and oInputParameterHandler.exist('linkToHosterMediaFile')):
        sHosterFileName = oInputParameterHandler.getValue('sHosterFileName')
        linkToHosterMediaFile = oInputParameterHandler.getValue('linkToHosterMediaFile')

        #try:
        exec "from " + sHosterFileName + " import cHoster"
        oHoster = cHoster()
        oHoster.setUrl(linkToHosterMediaFile)
        aLink = oHoster.getMediaLink()
        if (aLink[0] == True):
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_NAME)
            oGuiElement.setMediaUrl(aLink[1])

            oPlayer = cPlayer()
            oPlayer.addItemToPlaylist(oGuiElement)
            oPlayer.startPlayer()
            return
                        
        #except:
        #    logger.fatal('could not load plugin: ' + sHosterFileName)

    oGui.setEndOfDirectory()

def ajaxCall():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
        
    if (oInputParameterHandler.exist('page') and oInputParameterHandler.exist('mediaType')):
        iPage = oInputParameterHandler.getValue('page')
        sMediaType = oInputParameterHandler.getValue('mediaType')

        iMediaTypePageId = False
        if (oInputParameterHandler.exist('mediaTypePageId')):
            iMediaTypePageId = oInputParameterHandler.getValue('mediaTypePageId')

        sCharacter = 'A'
        if (oInputParameterHandler.exist('character')):
            sCharacter = oInputParameterHandler.getValue('character')


        logger.info('MediaType: ' + sMediaType + ' , Page: ' + str(iPage) + ' , iMediaTypePageId: ' + str(iMediaTypePageId) + ' , sCharacter: ' + str(sCharacter))

        sAjaxUrl = __createAjaxUrl(sMediaType, iPage, iMediaTypePageId, sCharacter)
        logger.info(sAjaxUrl)
                
        oRequest = cRequestHandler(sAjaxUrl)
        sHtmlContent = oRequest.request()

        # parse content
        sPattern = '\["([^"]+)".*?<a href=\\\\"\\\\([^"]+)\\\\".*?onclick=\\\\"return false;\\\\">([^<]+)<\\\\/a>'        
        oParser = cParser()

        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):            

            for aEntry in aResult[1]:
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_NAME)
                oGuiElement.setFunction('parseMovieEntrySite')

                sLanguageId = aEntry[0]
                sTitle = aEntry[2]
                if (sLanguageId == '1'):
                    sTitle = sTitle + ' (de)'
                if (sLanguageId == '2'):
                    sTitle = sTitle + ' (en)'

                oGuiElement.setTitle(sTitle)
                

                sUrl = URL_MAIN + str(aEntry[1])
                sUrl = oParser.replace('\\\\/', '/', sUrl)

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('movieUrl', sUrl)
                oGui.addFolder(oGuiElement, oOutputParameterHandler)


        # check for next site
        sPattern = '"iTotalDisplayRecords":"([^"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            for aEntry in aResult[1]:
                iTotalCount = aEntry[0]
                iNextPage = int(iPage) + 1
                iCurrentDisplayStart = __createDisplayStart(iNextPage)
                if (iCurrentDisplayStart < iTotalCount):
                    oGuiElement = cGuiElement()
                    oGuiElement.setSiteName(SITE_NAME)
                    oGuiElement.setFunction('ajaxCall')
                    oGuiElement.setTitle('next ..')

                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('page', iNextPage)
                    oOutputParameterHandler.addParameter('character', sCharacter)
                    oOutputParameterHandler.addParameter('mediaType', sMediaType)
                    if (iMediaTypePageId != False):
                        oOutputParameterHandler.addParameter('mediaTypePageId', iMediaTypePageId)
                    oGui.addFolder(oGuiElement, oOutputParameterHandler)
                    

    oGui.setEndOfDirectory()
   
def showCharacters():
    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('mediaType')):    
        sMediaType = oInputParameterHandler.getValue('mediaType')
        
    iMediaTypePageId = False
    if (oInputParameterHandler.exist('mediaTypePageId')):
        iMediaTypePageId = oInputParameterHandler.getValue('mediaTypePageId')

    oGui = cGui()
    __createCharacters(oGui, 'A', sMediaType, iMediaTypePageId)
    __createCharacters(oGui, 'B', sMediaType, iMediaTypePageId)
    __createCharacters(oGui, 'C', sMediaType, iMediaTypePageId)
    __createCharacters(oGui, 'D', sMediaType, iMediaTypePageId)
    __createCharacters(oGui, 'E', sMediaType, iMediaTypePageId)
    __createCharacters(oGui, 'F', sMediaType, iMediaTypePageId)
    __createCharacters(oGui, 'G', sMediaType, iMediaTypePageId)
    __createCharacters(oGui, 'H', sMediaType, iMediaTypePageId)
    __createCharacters(oGui, 'I', sMediaType, iMediaTypePageId)
    __createCharacters(oGui, 'J', sMediaType, iMediaTypePageId)
    __createCharacters(oGui, 'K', sMediaType, iMediaTypePageId)
    __createCharacters(oGui, 'L', sMediaType, iMediaTypePageId)
    __createCharacters(oGui, 'M', sMediaType, iMediaTypePageId)
    __createCharacters(oGui, 'N', sMediaType, iMediaTypePageId)
    __createCharacters(oGui, 'O', sMediaType, iMediaTypePageId)
    __createCharacters(oGui, 'P', sMediaType, iMediaTypePageId)
    __createCharacters(oGui, 'Q', sMediaType, iMediaTypePageId)
    __createCharacters(oGui, 'R', sMediaType, iMediaTypePageId)
    __createCharacters(oGui, 'S', sMediaType, iMediaTypePageId)
    __createCharacters(oGui, 'T', sMediaType, iMediaTypePageId)
    __createCharacters(oGui, 'U', sMediaType, iMediaTypePageId)
    __createCharacters(oGui, 'V', sMediaType, iMediaTypePageId)
    __createCharacters(oGui, 'W', sMediaType, iMediaTypePageId)
    __createCharacters(oGui, 'X', sMediaType, iMediaTypePageId)
    __createCharacters(oGui, 'Y', sMediaType, iMediaTypePageId)
    __createCharacters(oGui, 'Z', sMediaType, iMediaTypePageId)
    __createCharacters(oGui, '0', sMediaType, iMediaTypePageId)
    oGui.setEndOfDirectory()

def __createCharacters(oGui, sCharacter, sMediaType, iMediaTypePageId):
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_NAME)
    oGuiElement.setFunction('ajaxCall')
    oGuiElement.setTitle(sCharacter)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('page', 1)
    oOutputParameterHandler.addParameter('character', sCharacter)
    oOutputParameterHandler.addParameter('mediaType', sMediaType)
    oOutputParameterHandler.addParameter('mediaTypePageId', iMediaTypePageId)
    oGui.addFolder(oGuiElement, oOutputParameterHandler)

def __createDisplayStart(iPage):
    return (25 * int(iPage)) - 25
                
def __createAjaxUrl(sMediaType, iPage, iMediaTypePageId, sCharacter='A'):
    iDisplayStart = __createDisplayStart(iPage)

    oRequestHandler = cRequestHandler(URL_AJAX)
    if (iMediaTypePageId == False):
        #{"fType":"movie","fLetter":"A"}
        oRequestHandler.addParameters('additional', '{"fType":"' + str(sMediaType) + '","fLetter":"' + str(sCharacter) + '"}')
    else:
        #{"foo":"bar","fGenre":"2","fType":"","fLetter":"A"}
        oRequestHandler.addParameters('additional', '{"foo":"bar","' + str(sMediaType) + '":"' + iMediaTypePageId + '","fType":"","fLetter":"' + str(sCharacter) + '"}')
            
    oRequestHandler.addParameters('bSortable_0', 'true')
    oRequestHandler.addParameters('bSortable_1', 'true')
    oRequestHandler.addParameters('bSortable_2', 'true')
    oRequestHandler.addParameters('bSortable_3', 'false')
    oRequestHandler.addParameters('bSortable_4', 'false')
    oRequestHandler.addParameters('bSortable_5', 'false')
    oRequestHandler.addParameters('bSortable_6', 'true')
    oRequestHandler.addParameters('iColumns', '7')
    oRequestHandler.addParameters('iDisplayLength', '25')
    oRequestHandler.addParameters('iDisplayStart', iDisplayStart)
    oRequestHandler.addParameters('iSortCol_0', '2')
    oRequestHandler.addParameters('iSortingCols', '1')
    oRequestHandler.addParameters('sColumns', '')
    oRequestHandler.addParameters('sEcho', iPage)
    oRequestHandler.addParameters('sSortDir_0', 'asc')
    return oRequestHandler.getRequestUri()

def __parseHosterDefault(sUrl, sHosterName, sHosterFileName, sPattern):
    if (sPattern == False):
        sPattern = 'div><a href=\\\\"([^"]+)\\\\'
    
    sUrl = sUrl.replace('&amp;', '&')

    oRequest = cRequestHandler(sUrl)
    sHtmlContent = oRequest.request()
        
    oParser = cParser()
    aMovieParts = oParser.parse(sHtmlContent, sPattern)
        
    iCounter = 0
    oGui = cGui()
    if (aMovieParts[0] == True):
        
        for sPartUrl in aMovieParts[1]:
            sPartUrl = sPartUrl.replace('\\/', '/')
            iCounter = iCounter + 1

            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_NAME)
            oGuiElement.setTitle(sHosterName)
            oGuiElement.setFunction('playMovieFromHoster')
                        
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('sHosterFileName', sHosterFileName)
            oOutputParameterHandler.addParameter('linkToHosterMediaFile', sPartUrl)

            oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

                
def __getMovieHoster(sHtmlContent):
    aHosters = []
       
    aHosters.append(__parseHosterSiteFromSite(sHtmlContent, 'megavideo.com', 'Hoster_2', 'parseMegaVideoCom', 'megavideo'))
    aHosters.append(__parseHosterSiteFromSite(sHtmlContent, 'duckload.com', 'Hoster_6', 'parseHosterDefault', 'duckload'))
    aHosters.append(__parseHosterSiteFromSite(sHtmlContent, 'loaded.it', 'Hoster_19', 'parseHosterDefault', 'loadedit'))
    aHosters.append(__parseHosterSiteFromSite(sHtmlContent, 'sharehoster.com', 'Hoster_3', 'parseHosterDefault', 'sharehoster'))
    aHosters.append(__parseHosterSiteFromSite(sHtmlContent, 'dataup.to', 'Hoster_8', 'parseHosterDefault', 'dataup'))
    aHosters.append(__parseHosterSiteFromSite(sHtmlContent, 'quickload.to', 'Hoster_9', 'parseHosterDefault', 'quickload'))
    aHosters.append(__parseHosterSiteFromSite(sHtmlContent, 'mystream.to', 'Hoster_22', 'parseHosterDefault', 'mystream'))
    aHosters.append(__parseHosterSiteFromSite(sHtmlContent, 'mystream.to', 'Hoster_10', 'parseHosterDefault', 'mystream'))
    aHosters.append(__parseHosterSiteFromSite(sHtmlContent, 'skyload.net', 'Hoster_20', 'parseHosterDefault', 'skyload'))
    aHosters.append(__parseHosterSiteFromSite(sHtmlContent, 'tubeload.to', 'Hoster_18', 'parseHosterDefault', 'tubeload'))
        
    return aHosters


def __parseHosterSiteFromSite(sHtmlContent, sHosterName, sHosterId, sHosterMethodeName, sHosterFilename):
    aHoster = []
    sRegex = '<li id="' + sHosterId + '".*?rel="([^"]+)"'
        
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sRegex, 1)
    if (aResult[0] == True):
        sUrl = URL_MIRROR + urllib.unquote_plus(aResult[1][0])
        aHoster.append(sHosterName)
        aHoster.append(sUrl)
        aHoster.append(sHosterMethodeName)
        aHoster.append(sHosterFilename)
                
    return aHoster

#def __getDescription(sHtmlContent):
    #sRegex = '<div class="Descriptore">([^<]+)<'
    #oParser = cParser()
    #aResult = oParser.parse(sHtmlContent, sRegex, 1)
    #if (aResult[0] == True):
    #        print aResult[1]
    #return ''

#def __getThumbnail(sHtmlContent):
    #sRegex = '<div class="Grahpics">.*? src="([^"]+)"'
    #oParser = cParser()
    #aResult = oParser.parse(sHtmlContent, sRegex, 1)
    #if (aResult[0] == True):
    #        print aResult[1]
    #return ''

#def __isSerie(sHtmlContent):
    #sRegex = 'id="SeasonSelection" rel="([^"]+)"'
    #oParser = cParser()
    #aResult = oParser.parse(sHtmlContent, sRegex, 1)
    #return aResult[0]

