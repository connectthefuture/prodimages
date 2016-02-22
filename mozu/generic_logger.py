#!/usr/bin/env python
# coding: utf-8


def basic_log_file_obj(log_configuration='Admin_Client', **kwargs):
    import logging, datetime
    import logging.config
    logging._srcfile = None
    logging.logThreads = 0
    logging.logProcesses = 0
    from os import path as path
    configfile = kwargs.get('configfile', 'generic_logger_config.ini')
    if outfile is None:
        outfile = kwargs.get('outfile', str(__file__.__name__ + "_log.txt"))
        outfile = path.join("/root/DropboxSync/bflyProdimagesSync/log", path.filename(outfile))
    if configfile is not None:
        logging.config.fileConfig(path.normpath(configfile))
        hdlr = logging.FileHandler(outfile)
        #formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        formatter = logging.Formatter('%(asctime)s | %(name)s | %(module)s-%(lineno)04d | %(levelname)s | %(message)s')
        hdlr.setFormatter(formatter)
        myLogger = logging.getLogger(log_configuration)
        myLogger.addHandler(hdlr) 
        myLogger.setLevel(logging.WARNING)
        return myLogger
    else:
        logging.basicConfig(filename=outfile, filemode='w', level=logging.DEBUG) # level=logging.INFO)
        myLogger = logging.getLogger(log_configuration)      
        imsg='\nLOGGING Level 1 - Active....\nINFO MODE SET'
        wmsg='\nLOGGING Level 2 - Active....\nWARNING MODE SET'
        emsg='\nLOGGING Level 3 - Active....\nERROR MODE SET'
        cmsg='\nLOGGING Level 4 - Active....\nCRITICAL MODE SET'
        exmsg='\nEXCEPTION!!!!!....\n--------Exception Raised---------\n'
        dmsg='\nLOGGING DEBUGER - Active....\nDEBUG MODE SET'
        myLogger.info(imsg)
        myLogger.warn(wmsg)
        myLogger.error(emsg)
        myLogger.critical(cmsg)
        myLogger.exception(exmsg)
        myLogger.debug(dmsg)
        myLogger.setLevel(logging.WARNING)
        return myLogger

#logger.error('We have a problem')
#logger.info('While this is just chatty')


if __name__ == '__main__':
    #import sys
    logrun = basic_log_file_obj()
    numeric_level = getattr(logrun, loglevel.upper(), None)
    logrun.debug('Numeric Level Arg Set to {0}'.format(numeric_level))
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: {0}'.format(loglevel))
    logrun.basicConfig(level=numeric_level)
    #pass()

# if __name__ == '__main__':
#     # Configure the logger
#     # loggerConfigFileName: The name and path of your configuration file
#     logging.config.fileConfig(path.normpath(loggerConfigFileName))

#     # Create the logger
#     # Admin_Client: The name of a logger defined in the config file
#     myLogger = logging.getLogger('Admin_Client')

#     imsg='GENERIC LOGGING Level 1 - Active....\nINFO MODE SET'
#     wmsg='GENERIC LOGGING Level 2 - Active....\nWARNING MODE SET'
#     emsg='GENERIC LOGGING Level 3 - Active....\nERROR MODE SET'
#     cmsg='GENERIC LOGGING Level 4 - Active....\nCRITICAL MODE SET'
#     dmsg='GENERIC LOGGING DEBUGGER - Active....\nDEBUG MODE SET'
#     myLogger.info(imsg)
#     myLogger.warn(wmsg)
#     myLogger.error(emsg)
#     myLogger.critical(cmsg)
#     myLogger.debug(dmsg)

#     # Shut down the logger
#     logging.shutdown()
