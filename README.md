# DFIRScripts
This is a collection of scripts that I have written to help perform DFIR. 

# Browser_Chrome_History
Purpose: Parse Chrome history and then output to a CSV file. 

python3 Browser_Chrome_History.py -i ChromeHistoryFile -o history.csv

# Browser_IE_History
Purpose: Parse IE history and then output to a CSV file. Only tested on Windows 10, IE11. 

python3 Browser_IE_History.py -i /fullpath/IEHistoryfile.dat -o /fullpath/history.csv

# Windows10_Amcache_Parser
Purpose: Parse the amcache to look for evidence of program execution and also the hash of the program executed. When executed this will output a CSV file.

python3 Windows10_Amcache_Parser.py -i /PathToAmcacheFile.hve -o /DirpathToOutputCSVReports

# Windows10_Prefetch_Parser
Purppose: Parse prefetch files and then output to a CSV for analysis of when software has been executed on a computer. 

For a folder full of prefetch files:
python3 /home/sansforensics/Desktop/Windows10_Prefetch_Parser.py -d /home/sansforensics/Desktop/ -o /home/sansforensics/Desktop/prefetchResults.csv

For an individual file
python3 /home/sansforensics/Desktop/Windows10_Prefetch_Parser.py -i /home/sansforensics/Desktop/Amcache.hve -o /home/sansforensics/Desktop/prefetchResults.csv
