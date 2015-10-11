#!/usr/bin/env python
# -*- coding: utf-8 -*-



def port_tester(port, host=None):
    import socket;
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if not host:
        host = '127.0.0.1'
    result = sock.connect_ex((host,port))
    if result == 0:
       print "Port {} is open on {}".format(port,host)
       return True
    else:
       print "Port {} is not open on {}".format(port,host)
       return False


def url_tester(url):
    import requests
    res = requests.get(url)
    http_code = res.status_code
    return http_code


def main():
    import sys
    args = sys.argv
    if args:
        try:
            host = args[2]
            port = sys.argv[1]
        except IndexError:
            host = None
            port = sys.argv[1]
    else:
        port = '80'
    if len(port.split()) == 1:
        port_tester(port, host=None)
    else:
        for p in port.split():
            port_tester(p, host=None)
    return


if __name__ == '__main__':
    main()