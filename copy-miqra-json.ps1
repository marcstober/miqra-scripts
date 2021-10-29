$ErrorActionPreference = "Stop"

Copy-Item ..\MAM-parsed\miqra-json\*.json ..\miqra-data\miqra-json\
$dir = Get-ChildItem ..\miqra-data\miqra-json\*.json

foreach ($file in $dir) {
    Write-Output $file
    # indent json
    json -I -f $file # npm install -g json
    # HTML version
    py .\jsontotext.py $file
}
