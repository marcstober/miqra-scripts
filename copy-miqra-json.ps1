$ErrorActionPreference = "Stop"

# Delete all files in miqra-json directory
Remove-Item -Path ..\miqra-data\miqra-json\*
Remove-Item -Path ..\miqra-data\miqra-json-html\*


Copy-Item ..\MAM-parsed\plus\*.json ..\miqra-data\miqra-json\
$dir = Get-ChildItem ..\miqra-data\miqra-json\*.json

foreach ($file in $dir) {
    # indent json
    # json -I -f $file # npm install -g json
    # HTML version
    # if ($file.Name -like "*Genesis.json" -or $file.Name -like "*Levit.json" -or $file.Name -like "*Numbers.json") {
    # if ($file.Name -like "*Deuter.json") {
    write-Output $file.Name
    py .\jsontotext.py $file
    if ($LASTEXITCODE -ne 0) {
        Write-Output "Error in jsontotext.py"
        break
    }
    # }
}

