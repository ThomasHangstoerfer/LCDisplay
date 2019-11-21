#!/bin/bash
#
# Switch Wifi-mode between AccessPoint and Client
#
# Author: thomas.hangstoerfer@porsch-engineering.de
#
# Based on:
# https://www.elektronik-kompendium.de/sites/raspberry-pi/2002171.htm

PWD=`pwd`
SCRIPT=`realpath ${BASH_SOURCE[@]}`
SCRIPT_NAME=`basename ${BASH_SOURCE[@]}`
SCRIPT_DIR=`dirname ${SCRIPT}`
HOSTNAME=`hostname`

if [ "$EUID" -ne 0 ]; then
    echo "Please run as root"
    exit
fi

if [ "$1" = "" ]; then
    echo ""
    echo "${SCRIPT_NAME} [ap|client|mode]"
    echo ""
    exit
fi

if [ "$1" = "ap" ]; then
    echo "Switching to AccessPoint mode"
    cp ${SCRIPT_DIR}/dhcpcd.conf.wlan_ap /etc/
    cp ${SCRIPT_DIR}/dnsmasq.conf.wlan_ap /etc/
    cp ${SCRIPT_DIR}/hostapd.conf /etc/hostapd
    chmod 600 /etc/hostapd/hostapd.conf
    
    sed -i "s/ssid=.*/ssid="${HOSTNAME}"/" /etc/hostapd/hostapd.conf
    systemctl restart dnsmasq
    systemctl enable dnsmasq
    
    systemctl unmask hostapd
    systemctl start hostapd
    systemctl enable hostapd
    
elif [ "$1" = "client" ]; then
    echo "Switching to Client mode"
    cp ${SCRIPT_DIR}/dhcpcd.conf.wlan_client /etc/
    cp ${SCRIPT_DIR}/dnsmasq.conf.wlan_client /etc/
    #cp ${SCRIPT_DIR}/hostapd.conf /etc/hostapd

    systemctl restart dnsmasq
    systemctl enable dnsmasq
    
    systemctl unmask hostapd
    systemctl stop hostapd
    systemctl disable hostapd

elif [ "$1" = "mode" ]; then
    TEST=`ps aux |grep hostapd |grep -v grep`
    if [ "${TEST}" = "" ]; then
        # hostapd is not running -> client mode
        MODE=client
    else
        MODE=ap
    fi
    echo "$MODE"
else
    echo ""
    TEST=`ps aux |grep hostapd |grep -v grep`
    if [ "${TEST}" = "" ]; then
        # hostapd is not running -> client mode
        MODE=client
    else
        MODE=ap
    fi
    echo "Current mode is: ${MODE}"
fi
