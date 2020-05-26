#!/usr/bin/env python3

# -------------------------------------------------------------------------
# Creation Date: Mon 25 May 2020
#
# @ Author: Patrick Stel 
# @ Purpose: Script to check phone is on WiFi.
# -------------------------------------------------------------------------

import requests
import os

DomoticzIP = "http://192.168.0.125:8080"
DomoticzRequest = requests.get(DomoticzIP + "/json.htm?type=command&param=getuservariable&idx=3") #IDX version

DomoticzData = DomoticzRequest.json()
DomoticzMac = DomoticzData['result'][0]['Value']
macAddresses = DomoticzMac.split(",")

WifiScan = os.system('sudo nmap -sP -n 192.168.0.1/24 > output_nmap.txt')
if os.path.exists('output_nmap.txt'):
    fp = open('output_nmap.txt', "r")
    WifiScan_output = fp.read()
    fp.close()
    os.remove('output_nmap.txt')

for macAddress in macAddresses:
    cleanAddress = macAddress.strip()
    if cleanAddress in WifiScan_output:
        SetSwitchOn = requests.get(DomoticzIP + "/json.htm?type=command&param=switchlight&idx=22&switchcmd=On")
    else:
        SetSwitchOff = requests.get(DomoticzIP + "/json.htm?type=command&param=switchlight&idx=22&switchcmd=Off")