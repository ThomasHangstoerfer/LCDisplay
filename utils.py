# -*- coding: utf-8 -*-
#
# Author: Thomas Hangstoerfer
# License: MIT
#

from socket import socket, AF_INET, SOCK_DGRAM
from threading import Timer
import os
import subprocess
import traceback
import sys
import re
import psutil  # for cpu-load

bl_power_file = "/sys/class/backlight/rpi_backlight/bl_power"

def singleton(cls):
    # https://stackoverflow.com/questions/31875/is-there-a-simple-elegant-way-to-define-singletons
    # 'Duck()'
    obj = cls()
    # Always return the same object
    cls.__new__ = staticmethod(lambda cls: obj)
    # Disable __init__
    try:
        del cls.__init__
    except AttributeError:
        pass
    return cls


def setBacklight(on):
    if on:
        os.system('echo 1 > ' + bl_power_file)
    else:
        os.system('echo 0 > ' + bl_power_file)


def get_ip_address():
    sockname = ''
    try:
        s = socket(AF_INET, SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        sockname = s.getsockname()[0]
    except:
        print("Could not get IP-Adress")
    return sockname


def get_cpu_temp():
    temp = ""
    try:
        output = subprocess.run(['vcgencmd', 'measure_temp'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        temp = output.split("=")[1]
        temp = temp.split(".")[0]
        temp = temp + "°C"
    except:
        pass
    return temp

def get_uptime():
    uptime = ""
    try:
        output = subprocess.run(['uptime'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        list = output.split(" ")
        uptime = list[3] + list[4][:-1]
    except:
        pass
    return uptime

def get_hostname():
    hostname = ""
    try:
        output = subprocess.run(['hostname'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        hostname = output
    except:
        pass
    return hostname



def get_wifi_mode():
    #print("get_wifi_mode()")
    mode = ""
    try:
        output = subprocess.run(['/home/pi/LCDisplay/conf/wifi_mode.sh', 'mode'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        mode = output.rstrip()
        # print('get_wifi_mode(): ' + mode)

    except Exception as e:
        print("except", sys.exc_info()[0])
        print(traceback.format_exc())
        pass
    return mode

def switch_wifi_mode(mode):
    print("switch_wifi_mode(%s)" % mode)
    try:
        output = subprocess.run(['/home/pi/LCDisplay/conf/wifi_mode.sh', mode], stdout=subprocess.PIPE).stdout.decode('utf-8')
        mode = output.rstrip()
        print('switch_wifi_mode(): ' + mode)

    except Exception as e:
        print("except", sys.exc_info()[0])
        print(traceback.format_exc())
        pass
    return mode



def get_ap_ssid():
    # print("get_ap_ssid()")
    ssid = ""
    try:
        ps = subprocess.Popen(('grep', 'ssid', '/etc/hostapd/hostapd.conf'), stdout=subprocess.PIPE)
        output = subprocess.check_output(('cut', '-d', '=', '-f', '2'), stdin=ps.stdout).decode('utf-8')
        ps.wait()
        ssid = output.rstrip()
        # print('get_ap_ssid(): ' + ssid)

    except Exception as e:
        print("except", sys.exc_info()[0])
        print(traceback.format_exc())
        pass
    return ssid

def get_ap_password():
    # print("get_ap_password()")
    password = ""
    try:
        ps = subprocess.Popen(('grep', '^wpa_passphrase', '/etc/hostapd/hostapd.conf'), stdout=subprocess.PIPE)
        output = subprocess.check_output(('cut', '-d', '=', '-f', '2'), stdin=ps.stdout).decode('utf-8')
        ps.wait()
        password = output.rstrip()
        # print('get_ap_password(): ' + password)

    except Exception as e:
        print("except", sys.exc_info()[0])
        print(traceback.format_exc())
        pass
    return password



def get_make_running():
    #print("get_make_running()")
    temp = "not running"
    try:
        output = subprocess.check_output("ps a|grep make|grep -v grep", shell=True, stderr=subprocess.STDOUT )

        if len(output) > 0:
            temp = "running"
        #print(output)
        #print(temp)
    except Exception as e:
        print("except", sys.exc_info()[0])
        pass
    return temp


def get_network_info(wlan_device):

    try:
        output = subprocess.run(['iwconfig', 'wlan0'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        # print('output = ' + output)
    except Exception as e:
        print('Exception: ', e)

    essid = ''
    essid_search = re.search('ESSID.(.*).', output)
    if essid_search:
        essid = essid_search.group(1)
        essid = essid.replace('"', '')
    # print("essid " + essid)

    quality = 0
    quality_search = re.search('Link Quality=([0-9]*)/([0-9]*)', output)
    if quality_search:
        quality = int((int(quality_search.group(1)) * 100) / int(quality_search.group(2)))
    # print("quality ", quality)

    bitrate = 0
    bitrate_unit = ""
    bitrate_search = re.search('Bit Rate=([0-9]*) (.*)\s*Tx', output)
    if bitrate_search:
        bitrate = bitrate_search.group(1)
        bitrate_unit = bitrate_search.group(2)
    # print("bitrate: %s" % bitrate)
    # print("bitrate_unit: %s" % bitrate_unit)

    return bitrate, bitrate_unit, quality, essid


def running_on_pi():
    return os.path.isfile(bl_power_file)

def shutdown():
    try:
        output = subprocess.run(['shutdown', 'now'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    except:
        pass

def reboot():
    try:
        output = subprocess.run(['reboot', 'now'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    except:
        pass


class CPULoad:
    def __init__(self):
        self.history = []
        self.max_measurement_count = 12
        self.update_timeout = 2
        self.timer = None
        self.is_running = False
        self.is_started = False

    def start(self):
        print('CPULoad.start() ', self.is_running)
        self.is_started = True
        if not self.is_running:
            self.timer = Timer(self.update_timeout, self.timer_expired)
            self.timer.start()
            self.measure_cpu_load()
            self.is_running = True

    def stop(self):
        print('CPULoad.stop()')
        self.is_started = False
        self.timer.cancel()
        self.is_running = False

    def timer_expired(self):
        self.timer.cancel()
        if self.is_started:
            self.timer = Timer(self.update_timeout, self.timer_expired)
            self.timer.start()
        self.measure_cpu_load()

    def measure_cpu_load(self):
        # print('CPULoad.measure_cpu_load()')
        self.history.append(psutil.cpu_percent())
        while len(self.history) > self.max_measurement_count:
            self.history.pop(0)


class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.function   = function
        self.interval   = interval
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        #self.ignore_next = True
        self.ignore_next = False
        self.to_be_stopped = False
        self.start()

    def _run(self):
        self.is_running = False
        #print 'self.to_be_stopped = %s' % self.to_be_stopped
        if ( self.to_be_stopped == False ):
            self.start()
        #print('RepeatedTimer._run() ignore_next = ', self.ignore_next)
        if ( self.ignore_next ):
            #print('ignore first display_off')
            self.ignore_next = False
        else:
            self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        #print 'RepeatedTimer.stop()'
        self._timer.cancel()
        self.is_running = False

    def restart(self):
        #print 'RepeatedTimer.restart()'
        self.stop()
        self.start()

    def finish(self):
        #print 'RepeatedTimer.finish()'
        self.to_be_stopped = True
        self.stop()

cpu_load = CPULoad()
cpu_load.start()
