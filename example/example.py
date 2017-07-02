import sys
sys.path.append('../')

from tplink_hs1xx import SmartPlug
from tplink_hs1xx import COMMAND

plug = SmartPlug('192.168.1.11')
plug.command(COMMAND['OFF'])
