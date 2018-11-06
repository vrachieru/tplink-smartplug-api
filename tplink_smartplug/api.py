import json
import socket
import struct
import datetime

class SmartPlug(object):

    def __init__(self, host, port=9999, timeout=5):
        '''
        Create a new SmartPlug instance.

        :param str host: host name or ip address on which the device listens
        :param int port: port on which the device listens (default: 9999)
        :param int timeout: socket timeout (default: 5)
        '''
        self.host = host
        self.port = port
        self.timeout = timeout

    @property
    def info(self):
        '''
        Get system information

        :return system information
        '''
        return self.command(('system', 'get_sysinfo'))

    @property
    def device_id(self):
        '''
        Get device id
        
        :return: device id
        '''
        return self.info['deviceId']

    @device_id.setter
    def device_id(self, device_id):
        '''
        Set new device id
        
        :param str device_id: device id
        '''
        return self.command(('system', 'set_device_id', {'deviceId': device_id}))

    @property
    def hardware_id(self):
        '''
        Get device hardware id
        
        :return: device hardware id
        '''
        return self.info['hwId']

    @hardware_id.setter
    def hardware_id(self, hardware_id):
        '''
        Set new hardware id
        
        :param str hardware_id: hardware id
        '''
        return self.command(('system', 'set_hw_id', {'hwId': hardware_id}))

    @property
    def model(self):
        '''
        Get device model
        
        :return: device model
        '''
        return self.info['model']

    @property
    def mac(self):
        '''
        Get mac address
        
        :return: mac address in hexadecimal with colons, e.g. 01:23:45:67:89:ab
        '''
        return self.info['mac']

    @mac.setter
    def mac(self, mac):
        '''
        Set new mac address
        
        :param str mac: mac in hexadecimal with colons, e.g. 01:23:45:67:89:ab
        '''
        return self.command(('system', 'set_mac_addr', {'mac': mac}))

    @property
    def name(self):
        '''
        Get current device name (alias)

        :return: device name aka alias.
        '''
        return self.info['alias']

    @name.setter
    def name(self, name):
        '''
        Set the device name aka alias

        :param name: new name
        '''
        return self.command(('system', 'set_dev_alias', {'alias': name}))

    @property
    def rssi(self):
        '''
        Get WiFi signal strength (rssi)

        :return: rssi
        '''
        return self.info['rssi']

    @property
    def time(self):
        '''
        Get plug date and time

        :return: datetime
        '''
        dt = self.command(('time', 'get_time'))
        return datetime.datetime(dt['year'], dt['month'], dt['mday'], dt['hour'], dt['min'], dt['sec'])

    @property
    def timezone(self):
        '''
        Get timezone

        :return: timezone
        '''
        return self.command(('time', 'get_timezone'))

    @property
    def icon(self):
        '''
        Get icon

        :return: plug icon
        '''
        return self.command(('system', 'get_dev_icon'))

    @icon.setter
    def icon(self, icon, hash):
        '''
        Set the icon of the plug

        :param str icon: icon id
        :param str hash: icon hash
        '''
        return self.command(('system', 'set_dev_icon', {'icon': icon, 'hash': hash}))

    @property
    def location(self):
        '''
        Get the plug location

        :return: dict with latitude and longitude
        '''
        info = self.info
        location_keys = ['latitude', 'longitude']
        return {key: info[key] for key in location_keys}

    @location.setter
    def location(self, latitude, longitude):
        '''
        Set the plug location
        
        :param float latitude: location latitude
        :param float longitude: location longitude
        '''
        self.command(('system', 'set_dev_location', {'latitude': latitude, 'longitude': longitude}))

    @property
    def led(self):
        '''
        Get the led state

        :return: True if led is on, False otherwise
        '''
        return bool(1 - self.info['led_off'])

    @led.setter
    def led(self, state):
        '''
        Set the state of the led (night mode)
        
        :param bool state: True to set led on, False to set led off
        '''
        self.command('system', 'set_led_off', {'off': int(not state)})

    @property
    def is_on(self):
        '''
        Get whether device is on

        :return: True if device is on, False otherwise
        '''
        return bool(self.info['relay_state'])

    def turn_on(self):
        '''
        Turn the plug on
        '''
        self.command(('system', 'set_relay_state', {'state': 1}))

    def turn_off(self):
        '''
        Turn the plug off
        '''
        self.command(('system', 'set_relay_state', {'state': 0}))

    def reboot(self, delay=1):
        '''
        Reboot plug

        :param int delay: reboot delay in seconds (default: 1)
        '''
        return self.command(('system', 'reboot', {'delay': delay}))

    def factory_reset(self, delay=1):
        '''
        Factory reset the plug

        :param int delay: reboot delay in seconds (default: 1)
        '''
        return self.command(('system', 'reset', {'delay': delay}))

    def command(self, cmd):
        '''
        Request information from a TP-Link SmartHome Device and return the response

        :param cmd: command to send to the device (can be either tuple, dict or json string)
        :return: json response
        '''
        if isinstance(cmd, tuple):
            target, cmd, args = (cmd + ({},))[:3]
            cmd = {target: {cmd: args}}

        if isinstance(cmd, dict):
            cmd = json.dumps(cmd)

        try:
            sock = socket.create_connection((self.host, self.port), self.timeout)
            sock.send(self.encrypt(cmd))
            data = sock.recv(4096)
        finally:
            sock.close()

        response = self.decrypt(data[4:])
        response = json.loads(response)
        response = response.get(list(response)[0]) # extract target
        response = response.get(list(response)[0]) # extract command
        
        return response

    def encrypt(self, plaintext):
        '''
        Encrypt a request for a TP-Link Smart Home Device

        :param request: plaintext request data
        :return: ciphertext request
        '''
        key = 171

        plainbytes = plaintext.encode()
        buffer = bytearray(struct.pack('>I', len(plainbytes)))

        for plainbyte in plainbytes:
            cipherbyte = key ^ plainbyte
            key = cipherbyte
            buffer.append(cipherbyte)

        return bytes(buffer)

    def decrypt(self, ciphertext):
        '''
        Decrypt a response of a TP-Link Smart Home Device

        :param ciphertext: encrypted response data
        :return: plaintext response
        '''
        key = 171

        buffer = []
        for cipherbyte in ciphertext:
            plainbyte = key ^ cipherbyte
            key = cipherbyte
            buffer.append(plainbyte)

        plaintext = bytes(buffer)

        return plaintext.decode()
