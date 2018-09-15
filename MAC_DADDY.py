#############################################################################################
# __    __     ______     ______        _____     ______     _____     _____     __  __     #
#/\ "-./  \   /\  __ \   /\  ___\      /\  __-.  /\  __ \   /\  __-.  /\  __-.  /\ \_\ \    #
#\ \ \-./\ \  \ \  __ \  \ \ \____     \ \ \/\ \ \ \  __ \  \ \ \/\ \ \ \ \/\ \ \ \____ \   #
# \ \_\ \ \_\  \ \_\ \_\  \ \_____\     \ \____-  \ \_\ \_\  \ \____-  \ \____-  \/\_____\  #
#  \/_/  \/_/   \/_/\/_/   \/_____/      \/____/   \/_/\/_/   \/____/   \/____/   \/_____/  #
#############################################################################################
# TITLE: MAC DADDY
# ASCII art by http://patorjk.com/
# WRITTEN BY: RunningAJ (https://github.com/RunningAJ)
# VERSION: 1.0 Date 15Sep2018
# WRITTEN in Python3
# DESCRIPTION: The purpose of this script is to scan the local network you are connected to
# and then lookup each MAC address hardware vendor to give to a device list. This script
# came about as an easy way for me to identify many of the IoT devices connected on my home
# network.
#
# Thanks to https://macvendors.com/  for providing the API to lookup MACs with accuracy
############################################################################################# 
# Importing Modules for the script
from beautifulscraper import BeautifulScraper
import time, nmap, re

##########################################################
# FUNCTION TO LOOKUP THE MAC FROM https://macvendors.com
##########################################################
def maclookup(macaddress):
    # Now parsing the MAC to get rid of special characters
    macaddress = re.findall('[\d\w]*',macaddress)
    mac = ''
    for i in macaddress:
        mac = mac + i
    # Now putting in a one second timeout so that we do not violate the terms
    # Of the API object (one per second, 1000 per day)
    time.sleep(1)
    # Now getting the mac
    url = 'https://api.macvendors.com/' + mac
    scraper = BeautifulScraper()
    body = scraper.go(url)
    results = str(body)
    return results

##########################################################
# FUNCTION TO SCAN A NETWORK TO LOOK FOR THE MACS ON IT
##########################################################
def arpscan(network):
    scan  = nmap.PortScanner()
    # Running the nmpac scan
    scanresults = scan.scan(hosts=network, arguments=' -sP -PR')
    # Now extracting the results of the scan
    arpresults = []
    for i in scanresults['scan']:
        try:
            subresult = []
            subresult.append(i)
            subresult.append(scanresults['scan'][i]['addresses']['mac'])
            arpresults.append(subresult)
        except:
            pass
    return arpresults

##########################################################
# NOW SCANNING A NETWORK AND LOOKING UP EVERY MAC
##########################################################
network = input('Enter the network you want to scan (Ex 192.168.0.0/24): ')
networkscan = arpscan(network)
# Results of the scan
MACResults = []
for i in networkscan:
    results = []
    try:
        lookup = maclookup(i[1])
    except:
        lookup = 'MAC NOT FOUND'
    results.append(i[0])
    results.append(i[1])
    results.append(lookup)
    MACResults.append(results)
# Now printing the results
for i in MACResults:
    print(i)
