#!/usr/bin/python3
###############################################################################################
# _______            ________    _____      ______ ________                                   #
#___  __ \______________  __/______  /_________  /____  __ \_____ ___________________________ #
#__  /_/ /_  ___/  _ \_  /_ _  _ \  __/  ___/_  __ \_  /_/ /  __ `/_  ___/_  ___/  _ \_  ___/ #
#_  ____/_  /   /  __/  __/ /  __/ /_ / /__ _  / / /  ____// /_/ /_  /   _(__  )/  __/  /     #
#/_/     /_/    \___//_/    \___/\__/ \___/ /_/ /_//_/     \__,_/ /_/    /____/ \___//_/      #
#                                                                                             #    
###############################################################################################
# TITLE: Prefetch parser for Windows 10
# DESC: The prefecth file is used to speed up performance for loading applications. It also has
# valueable forensics information that includes the count of how many times the program has
# executed and the last 8 run times from that exectuable.
# DATE: 18JAN2019
# VER: 1.0
# WRITTEN BY: Adam Johnston
###############################################################################################
# SYNTAX:
# For a folder full of prefetch files:
# python3 /home/sansforensics/Desktop/Windows10_Prefetch_Parser.py -d /home/sansforensics/Desktop/ -o /home/sansforensics/Desktop/prefetchResults.csv
# For an individual file
# python3 /home/sansforensics/Desktop/Windows10_Prefetch_Parser.py -i /home/sansforensics/Desktop/Amcache.hve -o /home/sansforensics/Desktop/prefetchResults.csv
###############################################################################################
# MUST HAVE THE LIBSCCA PY MODULE FOR THIS SCRIPT TO WORK
# https://pypi.org/project/libscca-python/
# https://github.com/libyal/libscca
# GOOD REF -https://github.com/bromiley/tools/blob/master/win10_prefetch/w10pf_parse.py 
###############################################################################################
# Modules needed for the script
import argparse,csv,sys,os,json,pyscca,argparse
###########################################

def parsePrefetch(inputPF):
    prefetchfile = pyscca.open(inputPF)   
    FileRunTimes = []
    ProgramName = prefetchfile.get_executable_filename()
    ProgramHash = hex(prefetchfile.get_prefetch_hash())
    prefetchCount = prefetchfile.get_run_count()
    if prefetchCount < 8:
        for i in range(prefetchCount):
            if prefetchfile.get_last_run_time_as_integer(i) != 0:
                executed = [ProgramName,ProgramHash,prefetchfile.get_last_run_time(i).isoformat(),prefetchCount]
                FileRunTimes.append(executed)
    elif prefetchCount > 7:
        for i in range(8):
            if prefetchfile.get_last_run_time_as_integer(i) != 0:
                executed = [ProgramName,ProgramHash,prefetchfile.get_last_run_time(i).isoformat(),prefetchCount]
                FileRunTimes.append(executed)
    return FileRunTimes

def main():
    # Parsing the Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--inputPF", dest="InputFile", help='Path to the prefetch file')
    parser.add_argument("-d", "--inputDirectory", dest="InputDirectory", help='Path to directory containing prefetch files')
    parser.add_argument("-o", "--outputfile", dest="OutputFile", help='Path to Export your CSV')
    args = parser.parse_args()

    try:
        FileRunTimes = []
        Headers = ['ProgramName','ProgramHash','LastRunTime','CountExecuted']
        FileRunTimes.append(Headers)
        if args.InputFile == None:
            # get all files in the directory to get each file prefetch
            files = os.listdir(args.InputDirectory)
            for i in files:
                filepath = args.InputDirectory + i
                results = parsePrefetch(filepath)
                for t in results:
                    FileRunTimes.append(t)
            
        # Now running through the individual file
        else:
            prefetchfile = pyscca.open(args.InputFile)
            prefetchCount = prefetchfile.get_run_count()
            results = parsePrefetch(args.InputFile)
            for t in results:
                    FileRunTimes.append(t)

    except Exception as e:
        print(e.message)

    #Now exporting the results to a report
    with open(args.OutputFile, 'w') as f:
        wr = csv.writer(f,lineterminator='\n')
        for row in FileRunTimes:
            wr.writerow(row)
            
if __name__ == '__main__':
    main()