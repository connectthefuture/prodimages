#!/usr/bin/env python
# coding: utf-8

#### Logging Function Decorator ####
# Defining a log function decorator to use as @log
def log(original_function, filename=None):
    import logging, datetime, json
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
                logfile.write( "\n\tFunction \"%s\" called with\n\tkeyword arguments: %s\n\tpositional arguments: %s.\nThe result was %s.\n" % (original_function.__name__, json.dumps(kwargs), args, result)
                )
                end_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d--%H:%M.%S')
                logfile.write("\nEnd: {0}".format(end_time))
            return result
        except TypeError:
            print 'NoneTypeError in Logger'
            return
    return new_function


### Generic Logger
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
    configfile = kwargs.get('configfile', 'logconfig.ini')
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


if __name__ == '__main__':
    pass()
