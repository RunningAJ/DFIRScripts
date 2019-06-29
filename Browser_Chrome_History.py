#!/usr/bin/python3
##########################################
#   _____ _                                _____                         
#  / ____| |                              |  __ \                        
# | |    | |__  _ __ ___  _ __ ___   ___  | |__) |_ _ _ __ ___  ___ _ __ 
# | |    | '_ \| '__/ _ \| '_ ` _ \ / _ \ |  ___/ _` | '__/ __|/ _ \ '__|
# | |____| | | | | | (_) | | | | | |  __/ | |  | (_| | |  \__ \  __/ |   
#  \_____|_| |_|_|  \___/|_| |_| |_|\___| |_|   \__,_|_|  |___/\___|_|                                                                                                                                                
#                                                                      
# TITLE: Chrome History Parser
# WRITTEN BY: Adam Johnston
# DESC: The Point of this script is to parse a  
# Chrome history file and then extract the web
# history to a CSV File
# THE DEFAULT LOCATION FOR A CHROME FILE IS
# C:\users\%USER%\appdata\local\google\chrome\user data\default\history
###########################################
import csv,sqlite3,argparse

def main():
    # Parsing the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--inputfile", dest="InputFile", help='Path to the Chrome history file. Syntax of command in Python Browser_Chrome_History.py.py -i ChromeHistoryFile -o Results.CSV')
    parser.add_argument("-o", "--outputfile", dest="OutputFile", help="Path to Export your CSV. Syntax of command in Python Browser_Chrome_History.py.py -i ChromeHistoryFile -o Results.CSV")
    args = parser.parse_args()

    # Now parsing the file
    try:
        # Querying the file
        conn = sqlite3.connect(args.InputFile)
        c = conn.cursor()
        results = c.execute('SELECT datetime(last_visit_time/1000000-11644473600, "unixepoch") as last_visited, url , title, visit_count FROM urls;')
        # Now outputting the Query Results
        HistoryResults = []
        Headers = ['LastVisit','URL','Title','Count']
        HistoryResults.append(Headers)
        for i in results:
            HistoryResults.append(i)
        with open(args.OutputFile, 'w', encoding='utf-8') as f:
            wr = csv.writer(f,lineterminator='\n')
            for row in HistoryResults:
                wr.writerow(row)
    except:
        print("check your syntax and make sure you are using the full file path... python Browser_Chrome_History.py -i ChromeHistoryFile -o history.csv")
        
if __name__ == '__main__':
    main()