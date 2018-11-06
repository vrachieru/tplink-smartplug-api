import sys
sys.path.append('../')

from tplink_smartplug import SmartPlug

plug = SmartPlug('192.168.xxx.xxx')

print('Name:      %s' % plug.name)
print('Model:     %s' % plug.model)
print('Mac:       %s' % plug.mac)
print('Time:      %s' % plug.time)

print('')

print('Is on:     %s' % plug.is_on)
print('Nightmode: %s' % (not plug.led))
print('RSSI:      %s' % plug.rssi)
