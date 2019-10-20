import sys
sys.path.append('../')

from tplink_smartplug import SmartPlug

plug = SmartPlug('192.168.xxx.xxx')

print('Get Daily Statistic for October 2019:             %s' % plug.emeter_stats(month=10, year=2019))
print('Get Montly Statistic for 2019:                    %s' % plug.emeter_stats(year=2019))
print('Get Realtime Current and Voltage Reading:         %s' % plug.emeter_stats())
