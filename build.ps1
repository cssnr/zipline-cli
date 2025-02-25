$ErrorActionPreference = "Stop"

#if (-Not $args[0]) {
#    Write-Output "Specify version number with format: x.x.x"
#    exit
#}
#$env:ZIPLINE_VERSION = $args[0]
#Write-Output "Version: $env:ZIPLINE_VERSION"

$egg_dir = ".\src\*.egg-info"
if (Test-Path $egg_dir) {
    Write-Output "Removing: $egg_dir"
    Remove-Item -Force -Recurse $egg_dir
}
$cache_dir = ".\src\__pycache__"
if (Test-Path $cache_dir) {
    Write-Output "Removing: $cache_dir"
    Remove-Item -Force -Recurse $cache_dir
}
if (Test-Path ".\dist") {
    Write-Output "Removing: .\dist"
    Remove-Item -Force -Recurse ".\dist"
}
if (Test-Path ".\build") {
    Write-Output "Removing: .\build"
    Remove-Item -Force -Recurse ".\build"
}

if ($args[0] -eq "clean") {
    Write-Output "Clean Only Done. Not Building."
    exit
}

python -m build
#python -m pip uninstall zipline-cli
#python -m pip install .\dist\zipline_cli-0.0.1-py3-none-any.whl

Write-Output "Success."
