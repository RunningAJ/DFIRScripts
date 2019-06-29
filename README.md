# DFIRScripts
This is a collection of scripts that I have written to help perform DFIR. 

# Windows10_Prefetch_Parser
Purppose: Parse prefetch files and then output to a CSV for analysis of when software has been executed on a computer. 

For a folder full of prefetch files:
python3 /home/sansforensics/Desktop/Windows10_Prefetch_Parser.py -d /home/sansforensics/Desktop/ -o /home/sansforensics/Desktop/prefetchResults.csv

For an individual file
python3 /home/sansforensics/Desktop/Windows10_Prefetch_Parser.py -i /home/sansforensics/Desktop/Amcache.hve -o /home/sansforensics/Desktop/prefetchResults.csv
