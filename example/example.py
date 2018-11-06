import sys
sys.path.append('../')

from tplink_smartplug import SmartPlug
from tplink_smartplug import COMMAND

plug = SmartPlug('192.168.1.104')
plug.command(COMMAND['OFF'])
