import inotify.adapters
from prometheus_client import Counter, start_http_server
#from argparse import ArgumentParser
import os
dir = os.environ['DIR']
tag = os.environ['TAG']
# const path, iNotify watching for this path inside container bind to host machine
WATCH_DIR = '/watchdir/'

# parser = ArgumentParser()
# parser.add_argument("-d", "-dir", "-directory", dest="path",
#                     help="input target monitored FOLDER", metavar="DIR")
# parser.add_argument("-t", "-tag", dest="tag",
#                     help="choose correct TAG defaults to CDR", metavar="TYPE", default="cdr")
#
# args = parser.parse_args()
# dir_path = args.__getattribute__('path')
# tag = args.__getattribute__('tag')

def _main():
    c = Counter('ftp_failed_directory', tag)
    i = inotify.adapters.Inotify()
    # watching for mounted path from container to host
    i.add_watch(WATCH_DIR)

    for event in i.event_gen(yield_nones=False):
        (_, type_names, path, filename) = event

        print("PATH=[{}] FILENAME=[{}] EVENT_TYPES={}".format(
            path, filename, type_names))
        if len(type_names) > 0 and type_names[0] == 'IN_MOVED_TO' or type_names[0] == 'IN_CREATE':
            c.inc()


if __name__ == '__main__':
    # expose metrics on port 3000
    start_http_server(3000)
    _main()
