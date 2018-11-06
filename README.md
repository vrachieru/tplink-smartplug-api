<p align="center">
    <img src="https://user-images.githubusercontent.com/5860071/48065298-f97e8400-e1d2-11e8-999c-1a84c25cac14.png" width="150px" border="0" />
    <br/>
    <a href="https://github.com/vrachieru/tplink-smartplug-api/releases/latest">
        <img src="https://img.shields.io/badge/version-1.1.0-brightgreen.svg?style=flat-square" alt="Version">
    </a>
    <a href="https://travis-ci.org/vrachieru/tplink-smartplug-api">
        <img src="https://img.shields.io/travis/vrachieru/tplink-smartplug-api.svg?style=flat-square" alt="Version">
    </a>
    <br/>
    TP-Link HS1xx smart plug API wrapper
</p>

## About TP-Link SmartPlug

* [TP-Link Smart Plugs](https://www.tp-link.com/us/home-networking/smart-home/smart-plugs) are power plugs that can be turned on and off remotely via an app 
* Can be operated either via cloud or lan
* Offer energy monitoring and scheduling capabilities 

## Features

* Configure device
* Query device information
* Change plug state

## Install

```bash
$ pip3 install git+https://github.com/vrachieru/tplink-smartplug-api.git
```
or
```bash
$ git clone https://github.com/vrachieru/tplink-smartplug-api.git
$ pip3 install ./tplink-smartplug-api
```

## Usage

### Reading device information

```python
from tplink_smartplug import SmartPlug

plug = SmartPlug('192.168.xxx.xxx')

print('Name:      %s' % plug.name)
print('Model:     %s' % plug.model)
print('Mac:       %s' % plug.mac)
print('Time:      %s' % plug.time)

print('Is on:     %s' % plug.is_on)
print('Nightmode: %s' % (not plug.led))
print('RSSI:      %s' % plug.rssi)
```

```bash
$ python3 example.py
Name:      Livingroom Floor Lamps
Model:     HS100(EU)
Mac:       50:C7:XX:XX:XX:XX
Time:      2018-11-06 14:14:00

Is on:     True
Nightmode: False
RSSI:      -59
```

### Change state

```python
from tplink_smartplug import SmartPlug

plug = SmartPlug('192.168.xxx.xxx')

if plug.is_on:
    plug.turn_off()
    print('Plug turned off')
else:
    plug.turn_on()
    print('Plug turned on')
```

```bash
$ python3 example.py
Plug turned off

$ python3 example.py
Plug turned on
```

## Protocol

A python client for the proprietary TP-Link Smart Home protocol to control TP-Link `HS100` and `HS110` WiFi Smart Plugs.  
The SmartHome protocol runs on TCP port `9999` and uses a trivial `XOR` autokey encryption that provides no security.

The initial key (`initialization vector`) has a hardcoded value of `-85 (= 171)`.  
The first byte of the plaintext is `XORed` with the key. The key is then set to the plaintext byte.  
During the next iteration, the next plaintext byte is `XORed` with the previous plaintext byte. 

Decryption works the same, with the keystream made out of cyphertext bytes.  
This is known as an autokey cipher and while it has better statistical properties than simple `XOR` encryption with a repeating key, it can be easily broken by known plaintext attacks.

There is no authentication mechanism and commands are accepted independent of device state (configured/unconfigured).

Commands are formatted using JSON, for example:
```json
{ 
    "system": { 
        "get_sysinfo": {} 
    }
}
```

Commands can be nested, for example:
```json
{
    "system": {
        "get_sysinfo": {}
    },
    "time": {
        "get_time": {}
    }
}
```

## Reference

[1] https://www.softscheck.com/en/reverse-engineering-tp-link-hs110/

## License

MIT