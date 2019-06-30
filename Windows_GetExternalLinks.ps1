#####################################################################################################
# GET LINK CONTENTS 
#######################################################
# External Icons in Link files 
# WRITTEN BY: Adam Johnston
# DATE: 19DEC2018
# DESC: The point of this script is to find link files
# then parse the link file to see if the icon location 
# is pointing to a shared folder location 
# REF ATTACK: https://attack.mitre.org/techniques/T1187/
# EXAMPLE: get-externalLinks -path c:\
######################################################## 

function get-externalLinks {

<# 
.SYNOPSIS
The point of this script is to find link files then parse the link file to see if the icon location is pointing to a shared folder location
REF ATTACK: https://attack.mitre.org/techniques/T1187/ 

.DESCRIPTION

.EXAMPLE  
get-externalLinks -path c:\
#>

param($path)

# Function to get the contents of a link file
function get-linkContents{
param($ShortcutPath)
$shell = New-Object -ComObject WScript.Shell
$shortcutContents = $shell.CreateShortcut($ShortcutPath)
return $shortcutContents
}

# Now parsing a system to get all .lnk locations 
$results = Get-ChildItem $path -Recurse -Include *.lnk -ErrorAction SilentlyContinue

# Now looking at each link to see if the icon path points to a file share
$ExternalLinks = @()
foreach($i in $results){
$link = get-linkContents -ShortcutPath $i.Fullname
$test = $link.IconLocation | Select-String -Pattern "\\\\[\w.]*\\"
if ($test -ne $null){
$ExternalLinks += $test
}
}
if ($ExternalLinks.Count -eq 0) { Write-Output "No External Links Found"}
return $ExternalLinks
}