import xbmc

LOG_LEVEL_INFO = 0;
LOG_LEVEL_WARNING = 1;
LOG_LEVEL_FATAL = 2;

logLevel = LOG_LEVEL_INFO# (config.getSetting("debug")=="true")

def info(sInfo):
    if (logLevel <= LOG_LEVEL_INFO):
        __writeLog('[INFO] ' + sInfo);

def warning(sWarning):
    if (logLevel <= LOG_LEVEL_WARNING):
        __writeLog('[WARNING]' + sWarning);

def fatal(sFatal):
    if (logLevel <= LOG_LEVEL_FATAL):
        __writeLog('[FATAL]' + sFatal);

def __writeLog(sLog):
    #aStack = inspect.trace()
    #print aStack
    #sCallerFileName = aStack[0]

    xbmc.output(sLog)

