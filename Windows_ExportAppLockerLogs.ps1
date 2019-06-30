##################################################################
# App Locker Logs summarizer 
######################################################
# NAME: Applocker-Logs-Summarizer
# DESC: The point of this script is to extract events 
# from the applocker log and then to summarize the events
# or provide a detailed list of events in a CSV 
# DATE: 13FEB2019 
# WRITTEN BY: Adam Johnston   
######################################################
function Export-AppLockerLogs{

<# 
.SYNOPSIS
The point of this script is to extract program execution from the Applocker EXE Logs. This will either summarize events or provide a detailed csv report. This 
can be used to provide forensic analysis to determined if a malicious tool was executed.

.DESCRIPTION

.EXAMPLE  
$results = export-applockerlogs -path C:\Windows\System32\winevt\Logs\Microsoft-Windows-AppLocker%4EXE and DLL.evtx -summarized yes
$results = export-applockerlogs -path C:\Windows\System32\winevt\Logs\Microsoft-Windows-AppLocker%4EXE and DLL.evtx -detailed yes
#>

# Setting up the parameters to run the function
param(
[switch]$detailed,
[switch]$summarized,
$path    
)

# Class to structure event summarization
class ApplicationExecution {
$ApplicationName
$ApplicationPath
$FirstRunTime
$LastRunTime 
$Action
$count
}

# Importing the Applocker Log
$log = Get-WinEvent -Path $path

# Now summarizing the logs to export to a CSV 
if($summarized -eq $true){

    # Getting Unique Event Messages
    $uniqueMessages = $log | select-object Message | Sort-Object Message -Unique
    
    # Now summarizing the events
    $ApplicationRunTimeSummary = @()

    foreach($t in $uniqueMessages){
        if($t.Message -ne "The AppLocker policy was applied successfully to this computer." ){
        $another = $log | Where-Object Message -EQ $t.Message 
        # now we need to just add the count of times executed, the first run date and the last run date, plus the action ^(.*?) 
        $applicationInfo = New-Object -TypeName ApplicationExecution
        $applicationInfo.ApplicationName = $another[0].Message | Select-String -Pattern '[\w]*.EXE'  | % { $_.Matches } | % { $_.Value }
        $applicationInfo.ApplicationPath = $another[0].Message | Select-String -Pattern '.+?(?= was)'  | % { $_.Matches } | % { $_.Value }
        $applicationInfo.FirstRunTime = $another[-1].TimeCreated
        $applicationInfo.LastRunTime = $another[0].TimeCreated
        $applicationInfo.count = $another.Count
            if ($t.Message -cmatch "was allowed"){$applicationInfo.Action = 'allowed' } elseif($t.Message -cmatch "was not allowed") {$applicationInfo.Action = 'blocked' }
        $ApplicationRunTimeSummary += $applicationInfo
    }
    }
    $ApplicationExport = $ApplicationRunTimeSummary | Sort-Object count -Descending
}
elseif($detailed -eq $true){
    # Exporting the full logs to an array
    $ApplicationExport = $log 
}
return $ApplicationExport
}