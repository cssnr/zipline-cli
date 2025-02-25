$ErrorActionPreference = "Stop"

#if (-Not $args[0]) {
#    Write-Output "Specify version number with format: x.x.x"
#    exit
#}
#$env:ZIPLINE_VERSION = $args[0]
#Write-Output "Version: $env:ZIPLINE_VERSION"

$egg_dir = ".\*.egg-info"
if (Test-Path $egg_dir) {
    Remove-Item -Force -Recurse $egg_dir
}
if (Test-Path ".\__pycache__") {
    Remove-Item -Force -Recurse ".\__pycache__"
}
if (Test-Path ".\build") {
    Remove-Item -Force -Recurse ".\build"
}
if (Test-Path ".\dist") {
    Remove-Item -Force -Recurse ".\dist"
}

if ($args[0] -eq "clean") {
    Write-Output "Clean Only Done. Not Building."
    exit
}

python.exe -m build

Write-Output "Success."
