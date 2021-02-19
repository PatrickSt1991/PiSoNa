#!/usr/bin/env python

# -------------------------------------------------------------------------
# Creation Date: Thu May 2020    
# Modified Date: Fri Feb 2021 (simplified)
#
# @ Author: Patrick Stel                                                  
# @ Purpose: Script to check if NAS is powered on, turn off if it's idle. 
#            Script is running from Raspberry PI with Sonarr installed.
# -------------------------------------------------------------------------
import urllib
import paramiko
import json
import os
import transmissionrpc
from transmissionrpc.error import TransmissionError

# Check if NAS is actually running (ping)
PingNAS = os.system("ping -c 1 192.168.*.***")  #Change yo NAS IP

if PingNAS == 0:
    # TORRENT CHECK
    tc = transmissionrpc.Client('192.168.#.###', port=****, user='******', password='******') #Change to your IP, Port, Username and Password
    for torrent in tc.get_torrents():
        if torrent.status == 'downloading' or torrent.status == 'stopped':
            exit()

    # USENET CHECK
    SABnzbd = urllib.urlopen("http://192.168.#.###:####/api?mode=queue&output=json&apikey=******************") #Change to you IP and API Key
    SABnzbd_data = json.loads(SABnzbd.read())
    if SABnzbd_data["queue"]["status"] != 'Idle':  #If you want you can also check SABnzbd_data["qeue"]["slots"] if empty (if item is extracting)
        exit()

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname='192.168.#.###', port=**, username='******', password='******')  #Change to your IP, Port, Username, Passowrd
    stdin, stdout, stderr = ssh.exec_command("sudo poweroff")
    ssh.close()
