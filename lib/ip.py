import netifaces as ni

from re import *
from subprocess import *

def get_ip_and_wifi(interface='wlan0'):
    ni.ifaddresses(interface)
    ip = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']

    proc   = Popen(['iwconfig'], stdout=PIPE)
    intext = str(proc.communicate()[0])

    m2    = search('ESSID:".*" ',intext)
    ESSID = m2.group(0).split('"')[1]
    return {'ip': ip, 'wifi': ESSID}
