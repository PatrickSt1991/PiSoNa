#!/usr/bin/env python

#-------------------------------------------------------------------------
# Creation Date: Thu May 2020                                             
#
# @ Author: Patrick Stel                                                  
# @ Purpose: Script to check if Sonarr has new episodes, if so wakeup NAS.
#            Script is running from Raspberry PI with Sonarr installed.
#-------------------------------------------------------------------------

import requests
import datetime
import os
import time

# General parameters
wakeUp = 'sudo etherwake -i eth0 00:00:00:00:00:00' # Change 00:00:00:00:00:00 to the MAC address of your NAS 
restartSonarr = 'sudo systemctl restart sonarr.service'
sonarr_api_baseurl = 'http://192.168.0.0:8989/api/' # Change the IP to you Sonarr IP
sonarr_api_key = '' # Fill in Sonarr API Key
mountNAS = 'sudo mount -a'

# Payload API Calls
headers = {
    'Content-Type': 'application/json',
}

# Change the path in downloadedepisodescan to your path
apiCalls = ['{name: "CheckHealth"}',
            '{name: "RssSync"}',
            '{name: "RescanSeries"}',
            '{name: "missingEpisodeSearch"}',
            '{name: "downloadedepisodesscan", path: "/media/NAS-ExternalHDD/Series"}',
            '{name: "downloadedepisodesscan", path: "/media/NAS/Series"}'
            ]

search_date_today = datetime.date.today()
search_date_tomorrow = search_date_today + datetime.timedelta(days = 1) 

link_sonarr_calendar = sonarr_api_baseurl + "calendar?apikey=" + sonarr_api_key + "&start=" + str(search_date_today) + "&end=" + str(search_date_tomorrow)
webpage_sonarr_calendar = requests.get(link_sonarr_calendar)

# Check Sonarr Calendar if seriesId exists
lookup_seriesId = '"seriesId":'
check_result_seriesId = lookup_seriesId in webpage_sonarr_calendar.text

# Boot up NAS, wait, send API commands for establishing connection with NAS
if check_result_seriesId:
    os.system(wakeUp)
    time.sleep(300) #5 Minutes
    os.system(mountNAS)
    os.system(restartSonarr)
    for api in apiCalls:
        requests.post(sonarr_api_baseurl + 'command?apikey=' + sonarr_api_key, headers=headers, data=api)