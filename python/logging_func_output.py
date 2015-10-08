#!/usr/bin/env python
# coding: utf-8


def log(original_function, filename=None):
    import logging
    from os import path as path
    if filename is None:
        filename = str("__main__" + "_log.txt")
    logging.basicConfig(filename=filename, level=logging.INFO)
    print "Logging to … {0}".format(path.abspath(filename))
    def new_function(*args, **kwargs):
        result = original_function(*args, **kwargs)
        with open(filename, "ab+") as logfile:
            logfile.write("Function '%s' called with positional arguments %s and keyword arguments %s. The result was %s.\n" % (original_function.__name__, args, kwargs, result))
        return result
    return new_function

