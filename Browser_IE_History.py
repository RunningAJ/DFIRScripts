#!/usr/bin/python3
##########################################
# IE HISTORY PARSER 
#.-..----.   .----.  .--.  .----.  .----..----..----. 
#| || {_     | {}  }/ {} \ | {}  }{ {__  | {_  | {}  }
#| || {__    | .--'/  /\  \| .-. \.-._} }| {__ | .-. \
#`-'`----'   `-'   `-'  `-'`-' `-'`----' `----'`-' `-'
##########################################
# TITLE: IE History Parser
# WRITTEN BY: Adam Johnston
# DESC: The Point of this script is to parse an  
# IE history file and then extract the web
# history to a CSV File
# THE DEFAULT LOCATION FOR AN IE History file is 
# C:\users\%USER%\appdata\local\microsoft\windows\webcache\WebCacheV*.dat
# If you cannot copy the file you may have ran into a file locking issue
# You can get around this by having the user log off their computer
# Dependencies, libesedb-python and winfiletime
# pip install libesedb-python
# pip install winfiletime
# EVERYTHING IS IN UTC!!
##########################################
import pyesedb, re, datetime, filetime, argparse, csv

def main():
    # Parsing the Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--inputfile", dest="InputFile", help='Path to the IE history file. Syntax of command in Python Browser_IE_History.py -i IEHistoryFile.dat -o Results.CSV')
    parser.add_argument("-o", "--outputfile", dest="OutputFile", help="Path to Export your CSV. Syntax of command in Python Browser_IE_History.py -i IEHistoryFile.dat -o Results.CSV")
    args = parser.parse_args()

    # Now running through the command
    try:
        db = pyesedb.open(args.InputFile, mode='r')
        # Now grabbing the number of files
        NumberOfTables = db.get_number_of_tables()
        # Getting the total number of tables
        NumberOfTables = db.get_number_of_tables()
        # Now getting each table name and adding it to a list
        AllTableNames = []
        for i in range(0,NumberOfTables):
            table = db.get_table(i)
            tableName = table.get_name()
            AllTableNames.append(tableName)
        # Now extracting the internet history from each Container table
        URLHistory = []
        Headers = ['AccessTime','URL','AccessCount','RedirectURL','FileName']
        URLHistory.append(Headers)
        for i in AllTableNames:
            if re.match(r'Container_', i) is not None:
                table = db.get_table_by_name(i)
                NumberOfRecords = table.get_number_of_records()
                for h in range(0,NumberOfRecords):
                    record = table.get_record(h)
                    ticks = record.get_value_data_as_integer(13)
                    converted_time = filetime.to_datetime(ticks)
                    time = converted_time.strftime("%Y-%m-%d %H:%M:%S")
                    sublist = [time,record.get_value_data_as_string(17),record.get_value_data_as_integer(8),record.get_value_data_as_string(22),record.get_value_data_as_string(18)] 
                    URLHistory.append(sublist)
        # Now saving the results to a CSV
        with open(args.OutputFile, 'w') as f:
            wr = csv.writer(f,lineterminator='\n')
            for row in URLHistory:
                wr.writerow(row)

    except:
        print("check your syntax and make sure you are using the full file path, make sure you have libesedb-python and winfiletime installed... python Browser_IE_History.py -i /fullpath/IEHistoryfile.dat -o /fullpath/history.csv")

if __name__ == '__main__':
    main()