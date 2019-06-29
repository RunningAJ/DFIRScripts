#!/usr/bin/python3
#############################################################################
#   _                            _              ___                         #
#  /_\  _ __ ___   ___ __ _  ___| |__   ___    / _ \__ _ _ __ ___  ___ _ __ #
# //_\\| '_ ` _ \ / __/ _` |/ __| '_ \ / _ \  / /_)/ _` | '__/ __|/ _ \ '__|#
#/  _  \ | | | | | (_| (_| | (__| | | |  __/ / ___/ (_| | |  \__ \  __/ |   #
#\_/ \_/_| |_| |_|\___\__,_|\___|_| |_|\___| \/    \__,_|_|  |___/\___|_|   #
#############################################################################
# TITLE: AMCACHE PARSER FOR WINDOWS 10
# DESC: Script to parse the amacache hive file
# to look for application execution.
# DATE: 15JAN2019
# VER: 1.0
# WRITTEN BY: Adam Johnston
# NOTES: Must have the following module installed
# python-registry (pip install python-registry)
# https://github.com/williballenthin/python-registry/tree/master/samples
#############################################################################
# DIRECTIONS: The amcache file exists in the following location on a windows system
# C:\Windows\appcompat\Programs\Amcache.hve
# Once this file is copied run the following command to extract the contents to several reports
# python Amcache.py -i /PathToAmcacheFile.hve -o /DirpathToOutputCSVReports
#############################################################################
# Importing Modules
import sys,csv,argparse
from Registry import Registry
#############################################################################

def main():
    # Parsing the Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--inputfile", dest="InputFile", help='Path to the Amcache Hive file. Syntax of command is Python Windows10_Amcache_Parser.py -i PathToAmcacheFile.hve -o /DirReport')
    parser.add_argument("-o", "--outputdirectory", dest="OutputDir", help="Dir path to Export your CSV reports. Syntax of command is Python Windows10_Amcache_Parser.py -i PathToAmcacheFile.hve -o /DirReport/")
    args = parser.parse_args()

    # Now running the command to extract the Hive file contents 
    try:
        # Importing the Hive file
        reg = Registry.Registry(args.InputFile)

        # Getting the root key
        topLevel = reg.root()
        rootKey = topLevel.subkey('Root')

        #####################################################################
        # Getting the list of applications installed

        # Grabbing the InventoryApplication Key
        inventoryApplications = rootKey.subkey('InventoryApplication')
        keyCount = inventoryApplications.subkeys_number()

        # Now parsing the subkeys from the InventoryApplication
        InventoryOfApplications = []
        for i in range(keyCount):
            applicationKey = inventoryApplications.subkeys()[i]
            # Now parsing through all the values on this key
            numberOfValues = applicationKey.values_number()
            ApplicationEntry = {}
            for d in range(numberOfValues):
                value = applicationKey.values()[d]
                name = value.name()
                value = value.value()
                ApplicationEntry[name] = value
            # Now adding the timestamp of the program's first execution 
            FirstTimeOfExecution = applicationKey.timestamp()
            ApplicationEntry['TimeOfFirstExecution'] = FirstTimeOfExecution.isoformat()
            # Now adding the entry into the inventory of applications
            InventoryOfApplications.append(ApplicationEntry)

        #####################################################################
        # Getting the list of files executed
        
        # InventoryApplicationFile is the key name
        inventoryApplications = rootKey.subkey('InventoryApplicationFile')
        keyCount = inventoryApplications.subkeys_number()

        # Now parsing the subkeys to get their values
        InventoryOfApplicationFiles = []
        for i in range(keyCount):
            applicationKey = inventoryApplications.subkeys()[i]
            # Now parsing through all the values on this key
            numberOfValues = applicationKey.values_number()
            ApplicationEntry = {}
            for d in range(numberOfValues):
                value = applicationKey.values()[d]
                name = value.name()
                value = value.value()
                ApplicationEntry[name] = value
            # Now adding the timestamp of the program's first execution 
            FirstTimeOfExecution = applicationKey.timestamp()
            ApplicationEntry['TimeOfFirstExecution'] = FirstTimeOfExecution.isoformat()
            # Now adding the entry into the inventory of applications
            InventoryOfApplicationFiles.append(ApplicationEntry)

        #####################################################################
        # Now extracting the lists to a report direcotry
        Outdir = args.OutputDir
        # Now exporting the results to several CSVs
        InventoryOfApplicationsCSV = []
        ExportPath = Outdir + 'InventoryOfApplications.csv'
        Headers = ['StoreAppType', 'RegistryKeyPath', 'Source', 'RootDirPath', 'InstallDate', 'OSVersionAtInstallTime', 'MsiProductCode', 'ProgramInstanceId', 'MsiPackageCode', 'ProgramId', 'InboxModernApp', 'Type', 'BundleManifestPath', 'ManifestPath', 'Publisher', 'Language', 'UninstallString', 'Version', 'TimeOfFirstExecution', 'Name', 'PackageFullName', 'HiddenArp']
        InventoryOfApplicationsCSV.append(Headers)
        for i in InventoryOfApplications:
            sublist = list(i.values())
            InventoryOfApplicationsCSV.append(sublist)

        # Exporting Report 1
        with open(ExportPath, 'w') as f:
                    wr = csv.writer(f,lineterminator='\n')
                    for row in InventoryOfApplicationsCSV:
                        wr.writerow(row)

        # Now exporting InventoryFile Results
        InventoryOfApplicationFilesCSV = []
        ExportPath = Outdir + 'InventoryOfFiles.csv'
        Headers = ['IsOsComponent', 'Publisher', 'FileId', 'BinaryType', 'LowerCaseLongPath', 'LinkDate', 'Language', 'BinProductVersion', 'Version', 'ProgramId', 'ProductVersion', 'LongPathHash', 'IsPeFile', 'BinFileVersion', 'Name', 'TimeOfFirstExecution', 'Size', 'Usn', 'ProductName']
        InventoryOfApplicationFilesCSV.append(Headers)
        for i in InventoryOfApplicationFiles:
            sublist = list(i.values())
            InventoryOfApplicationFilesCSV.append(sublist)

        # Exporting Report 2
        with open(ExportPath, 'w') as f:
                    wr = csv.writer(f,lineterminator='\n')
                    for row in InventoryOfApplicationFilesCSV:
                        wr.writerow(row)
                        

    except:
        print('check your syntax....python /home/sansforensics/Desktop/Windows10_Amcache_Parser.py -i /home/sansforensics/Desktop/Amcache.hve -o /home/sansforensics/Desktop/amcacheTest/')

if __name__ == '__main__':
    main()