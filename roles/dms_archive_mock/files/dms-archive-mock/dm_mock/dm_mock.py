import sys
import os
import json
import time
import requests
import urllib
from argparse import ArgumentParser
from subprocess import Popen
from subprocess import PIPE


LS_PATH = '/bin/ls'
DMATTR_FIELDS = ['bfid',
                 'emask',
                 'fhandle',
                 'flags',
                 'nregn',
                 'owner',
                 'path',
                 'projid',
                 'sitetag',
                 'size',
                 'space',
                 'state']

if os.path.exists(os.path.join(os.path.expanduser("~"),
                               ".dmmock_server.json")):
    with open(os.path.join(os.path.expanduser("~"),
                           ".dmmock_server.json"), "r") as fp:
        CONFIG = json.load(fp)
else:
    with open("/etc/dmmock_server.json", "r") as fp:
        CONFIG = json.load(fp)


def url_encode(p):
    return urllib.parse.quote(p)


def ls_inode_object(path):
    global CONFIG
    host = CONFIG.get('host', '127.0.0.1')
    port = CONFIG.get('port', 5000)
    res = requests.get("http://{0}:{1}/{2}".format(host, port,
                                                   url_encode(path)))
    res.raise_for_status()
    return res.json()


def wait_for_states(paths, states):
    global CONFIG
    host = CONFIG.get('host', '127.0.0.1')
    port = CONFIG.get('port', 5000)
    active_paths = {p: True for p in paths}
    ap = [k for k in active_paths.keys()]
    while len(ap) > 0:
        for p in ap:
            res = requests.get("http://{0}:{1}/{2}".format(host, port,
                                                           url_encode(p)))
            res.raise_for_status()
            obj = res.json()
            if obj['state'] in states:
                del active_paths[p]
        time.sleep(1)
        ap = [k for k in active_paths.keys()]


def dmls(argv=sys.argv[1:]):
    parser = ArgumentParser(description='')
    parser.add_argument('files', type=str, nargs='*')
    args, unknown = parser.parse_known_args([a for a in argv
                                             if a not in ['-h', '--help']])
    files = args.files
    if len(files) == 1:
        curr_dir = os.path.abspath(files[0])
        if not os.path.isdir(curr_dir):
            curr_dir = os.path.dirname(curr_dir)
    else:
        curr_dir = os.getcwd()
    argv = argv + ['--time-style', 'long-iso']
    proc = Popen([LS_PATH] + argv, stdout=PIPE, stderr=PIPE)
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        line = line.rstrip()
        if line.endswith(b':'):
            curr_dir = os.path.abspath(line[0:-1])
        if line == b'':
            print('')
        else:
            _dmls_process_line(line, curr_dir)
    while True:
        line = proc.stderr.readline()
        if not line:
            break
        print(line.decode())
    sys.exit(proc.returncode)


def _dmls_process_line(line, basedir):
    fmt = '{0} {1} {2:<12} {3:<12} {4:>12} {5} {6} {7}'
    cols = line.split(maxsplit=7)
    if len(cols) == 8:
        if not isinstance(basedir, str):
            basedir = basedir.decode()
        p = os.path.join(basedir, cols[-1].decode())
        obj = ls_inode_object(p)
        s = [item.decode()
             for item in cols[0:6] + [obj.get('state').encode()] + [cols[7]]]
        print(fmt.format(*tuple(s)))
    else:
        print(line.decode())


def dmput(argv=sys.argv[1:]):
    global CONFIG
    host = CONFIG.get('host', '127.0.0.1')
    port = CONFIG.get('port', 5000)

    parser = ArgumentParser(description='')
    parser.add_argument('files', type=str, nargs='*')
    parser.add_argument("-r", action='store_true', dest='remove',
                        help="remove file locally")
    parser.add_argument("-w", action='store_true', dest='wait',
                        help="wait until all files have been copied")
    args = parser.parse_args(argv)
    paths = [os.path.abspath(f) for f in args.files]
    for p in paths:
        params = {"remove": "1" if args.remove else "0",
                  "op": "put"}
        res = requests.put("http://{0}:{1}/{2}".format(host, port,
                                                       url_encode(p)),
                           params=params)
        res.raise_for_status()
    if args.wait:
        wait_for_states(paths, ['DUL', 'OFL'])


def dmget(argv=sys.argv[1:]):
    global CONFIG
    host = CONFIG.get('host', '127.0.0.1')
    port = CONFIG.get('port', 5000)

    parser = ArgumentParser(description='')
    parser.add_argument('files', type=str, nargs='*')
    parser.add_argument("-q", action='store_true', dest='quit',
                        help="recalls migrated file")
    parser.add_argument("-a", action='store_true', dest='access_time',
                        help="Update the access time of the file.")
    args = parser.parse_args(argv)
    paths = [os.path.abspath(f) for f in args.files]
    for p in paths:
        params = {"op": "get",
                  "access_time": args.access_time}
        res = requests.put("http://{0}:{1}/{2}".format(host,
                                                       port,
                                                       url_encode(p)),
                           params=params)
        res.raise_for_status()
    if not args.quit:
        wait_for_states(paths, ['DUL', 'REG'])


def dmattr_format_attr(obj, attr=DMATTR_FIELDS, delim=" "):
    line = ''
    for f in attr:
        if line:
            line += delim
        line += str(obj.get(f))
    print(line)


def dmattr_long_format_attr(obj, attr=DMATTR_FIELDS, delim=None):
    fmt = "{0: >%d} : {1}" % max([len(f) for f in DMATTR_FIELDS])
    for f in attr:
        print(fmt.format(f, str(obj.get(f))))
    print("")


def dmattr(argv=sys.argv[1:]):
    parser = ArgumentParser(description='')
    parser.add_argument('files', type=str, nargs='*')
    parser.add_argument("-l", action='store_true', dest='long',
                        help="long format")
    parser.add_argument("-d",
                        type=str,
                        dest="delim",
                        default=' ',
                        help=("Specifies the delimiter that " +
                              "separates the attributes in " +
                              "the dmattr output."))
    parser.add_argument("-a",
                        type=str,
                        default=",".join(DMATTR_FIELDS),
                        dest="attr",
                        help=("Displays one or more of file attributes"))
    args = parser.parse_args(argv)
    if args.long:
        formatter = dmattr_long_format_attr
    else:
        formatter = dmattr_format_attr
    for f in args.files:
        obj = ls_inode_object(os.path.abspath(f))
        obj['path'] = f
        formatter(obj,
                  attr=args.attr.split(","),
                  delim=args.delim)
