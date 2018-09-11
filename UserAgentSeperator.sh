#!/bin/bash
###########################################################
# TITLE: TSHARK HTTP-USERAGENT POST PCAP SEPERATOR
###########################################################
#                                 ,-
#                               ,'::|
#                              /::::|
#                            ,'::::o\                                      _..
#         ____........-------,..::?88b                                  ,-' /
# _.--"""". . . .      .   .  .  .  ""`-._                           ,-' .;'
#<. - :::::o......  ...   . . .. . .  .  .""--._                  ,-'. .;'
# `-._  ` `":`:`:`::||||:::::::::::::::::.:. .  ""--._ ,'|     ,-'.  .;'
#     """_=--       //'doo.. ````:`:`::::::::::.:.:.:. .`-`._-'.   .;'
#         ""--.__     P(       \               ` ``:`:``:::: .   .;'
#                "\""--.:-.     `.                             .:/
#                  \. /    `-._   `.""-----.,-..::(--"".\""`.  `:\
#                   `P         `-._ \          `-:\          `. `:\
#                                   ""            "            `-._)
###########################################################
# BY: RunningAJ
# DATE: 10SEP2018
# PURPOSE: Find C2/Data Exfil occuring over HTTP POST REQUEST 
# DESCRIPTION: The Point of this script is to parse a PCAP using TSHARK and then seperate that file into seperate PCAPs
# based on http user agent strings performing POST request. This could help to detect potential C2/Data Exfil.  
###########################################################
# Example command
# UserAgentSeperator /folder/filelocation.pcap /outputdirectory
###########################################################
# Setting variable for the script to run with
PCAP=$1
output=$2
# Now breaking up the PCAP to look for sub-http user agent strings 
agents=$(tshark -n -r $PCAP -T fields -e http.user_agent | sort | uniq)
# Now breaking all the user agents up by post request 
IFS=$'\n' 
for i in $agents; 
do
        fname=$(echo $i | tr -d '/,')
        searchstring='http.request.method == "POST" and http.user_agent == "'$i
        searchstring=$searchstring'"'
        tshark -n -r $PCAP -Y $searchstring -w $output/$fname.pcap
done
