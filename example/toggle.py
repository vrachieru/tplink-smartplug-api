import sys
sys.path.append('../')

from tplink_smartplug import SmartPlug

plug = SmartPlug('192.168.xxx.xxx')

if plug.is_on:
    plug.turn_off()
    print('Plug turned off')
else:
    plug.turn_on()
    print('Plug turned on')
