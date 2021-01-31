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
wakeUp = 'sudo etherwake -i eth0 00:00:00:00:00:00' #Change to your NAS MAC Address
sonarr_api_baseurl = 'http://192.168.0.125:8989/api/' #Change to your Sonarr API URL
sonarr_api_key = '' #Fill in API key 
mountNAS = 'sudo mount -a -t nfs'

# Payload API Calls
headers = {
    'Content-Type': 'application/json',
}

apiCalls = ['{name: "CheckHealth"}',
            '{name: "RssSync"}',
            '{name: "RescanSeries"}',
            '{name: "missingEpisodeSearch"}',
            '{name: "downloadedepisodesscan", path: "/media/NAS/Series"}',
            '{name: "downloadedepisodesscan", path: "/media/NAS-ExternalHDD/Series"}',
            '{name: "downloadedepisodesscan", path: "/media/NAS-ExternalHDD2/Series"}'
            ]

search_date_today = datetime.date.today()
search_date_tomorrow = search_date_today + datetime.timedelta(days = 1)

link_sonarr_calendar = sonarr_api_baseurl + "calendar?apikey=" + sonarr_api_key + "&start=" + str(search_date_today) + "&end=" + str(search_date_tomorrow)
webpage_sonarr_calendar = requests.get(link_sonarr_calendar)

# Check Sonarr Calendar if seriesId exists
lookup_seriesId = '"seriesId":'
check_result_seriesId = lookup_seriesId in webpage_sonarr_calendar.text

link_sonarr_queue = sonarr_api_baseurl+ "queue?apikey=" + sonarr_api_key
webpage_sonarr_queue = requests.get(link_sonarr_queue)

# Check Sonarr queue if series exists
lookup_series = '"series":'
check_result_series = lookup_series in webpage_sonarr_queue.text

# Boot up NAS, wait, send API commands for establishing connection with NAS
if check_result_seriesId or check_result_series:
    NAS_Status = os.system("ping -c 1 192.168.0.123") #Change to NAS IP
    if NAS_Status != 0:
        os.system(wakeUp)
        time.sleep(300)
        os.system(mountNAS)
        for api in apiCalls:
            requests.post(sonarr_api_baseurl + 'command?apikey=' + sonarr_api_key, headers=headers, data=api)
