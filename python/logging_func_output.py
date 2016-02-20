#!/usr/bin/env python
# coding: utf-8

#### Logging Function Decorator ####
# Defining a log function decorator to use as @log
def log(original_function, filename=None):
    import logging, datetime, json
    logging._srcfile = None
    logging.logThreads = 0
    logging.logProcesses = 0
    from os import path as path
    if filename is None:
        filename = path.join("/root/DropboxSync/bflyProdimagesSync/log", str(original_function.__name__ + "_log.txt"))
    logging.basicConfig(filename=filename, level=logging.DEBUG) # level=logging.INFO)
    start_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d--%H:%M.%S')
    # print "Logging to … {0}".format(path.abspath(filename))
    def new_function(*args, **kwargs):
        try:
            result = original_function(*args, **kwargs)
            with open(filename, "wb+") as logfile:
                logfile.write("\nStart: {0}".format(start_time))
                logfile.write( "\n\tFunction \"%s\" called with\n\tkeyword arguments: %s\n\tpositional arguments: %s.\nThe result was %s.\n" % (original_function.__name__, json.dumps(kwargs), args, result))
                end_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d--%H:%M.%S')
                logfile.write("\nEnd: {0}".format(end_time))
            return result
        except TypeError as e:
            logging.exception('NoneTypeError in Logger\nTraceback:\t{0}'.format(e))
            return
    return new_function


### Simple Output  Logger
def mr_logger(src_filepath,*args):
    import datetime
    current_dt = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
    logged_items = []
    if len(args) > 0:
        for arg in args:
            logit = "{}\t{}\n".format(current_dt,arg)
            logged_items.append(logit)
    for i in logged_items:
        with open(src_filepath, 'ab+') as f:
            f.write(i)
    return src_filepath


## Log function args and calls to outfile
def log_to_file(original_function, outfile=None, configfile=None):
    import logging, datetime
    from os import path as path
    logging._srcfile = None
    logging.logThreads = 0
    logging.logProcesses = 0
    configfile = kwargs.get('configfile', 'generic_logger_config.ini')
    if outfile is None:
        outfile = kwargs.get('outfile', str(original_function.__name__ + "_log.txt"))
        outfile = path.join("/root/DropboxSync/bflyProdimagesSync/log", path.filename(outfile))
    if configfile is not None:
        logging.config.fileConfig(path.normpath(configfile))
    else:
        logging.basicConfig(filename=outfile, level=logging.DEBUG) # level=logging.INFO)
    start_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d--%H:%M.%S')
    print "Logging to … {0}".format(path.abspath(outfile))
    def new_function(*args, **kwargs):
        result = original_function(*args, **kwargs)
        with open(outfile, "ab+") as logfile:
            logfile.write("Function '%s' called with positional arguments %s and keyword arguments %s. The result was %s.\n" % (original_function.__name__, args, kwargs, result))
        return result
    return new_function


class OneLineExceptionFormatter(logging.Formatter):
    def formatException(self, exc_info):
        """
        Format an exception so that it prints on a single line.
        """
        result = super(OneLineExceptionFormatter, self).formatException(exc_info)
        return repr(result) # or format into one line however you want to

    def format(self, record):
        s = super(OneLineExceptionFormatter, self).format(record)
        if record.exc_text:
            s = s.replace('\n', '') + '|'
        return s


def configure_logging():
    import logging
    logging._srcfile = None
    logging.logThreads = 0
    logging.logProcesses = 0
    fh = logging.FileHandler(__file__.__name__ + "_log.txt", 'w')
    f = OneLineExceptionFormatter('%(asctime)s|%(levelname)s|%(message)s|',
                                  '%d/%m/%Y %H:%M:%S')
    fh.setFormatter(f)
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    root.addHandler(fh)


def main(func,*args):
    configure_logging()
    logging.info('Test Configured Logger Main Msg')
    try:
        func(*args)
    except ZeroDivisionError as e:
        logging.exception('ZeroDivisionError: %s', e)



if __name__ == '__main__':
    pass() #main()
