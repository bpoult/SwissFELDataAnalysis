import os
import logging
from cfgfile import ConfigFile
#import a_module

directory = os.getcwd()
folder = directory.split('/')

if folder[-1] == 'RIXS' or folder[-1] == 'XES':
    DEFAULT_FNAME = '/'.join(folder[:-1]) + '/common/channels.ini'
elif folder[-1] == 'common':
    DEFAULT_FNAME = '/'.join(folder) + '/channels.ini'
else:
    DEFAULT_FNAME = '/'.join(folder) + '/common/channels.ini'


log = logging.getLogger()


def update_channels(fname=DEFAULT_FNAME):
    cfg = ConfigFile(fname)
    globals().update(cfg)
    log.debug(f"Loaded channels from {fname}")
    return cfg



try:
    config = update_channels()
except FileNotFoundError:
    dirname = os.path.dirname(__file__)
    fname = os.path.join(dirname, DEFAULT_FNAME)
    config = update_channels(fname)
    log.warning(f"Fallback: loaded default channel list ({fname})")

