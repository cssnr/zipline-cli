$ErrorActionPreference = "Stop"

$egg_dir = "zipline_cli.egg-info"
if (Test-Path $egg_dir) {
    Remove-Item -Force -Recurse $egg_dir
}
if (Test-Path ".\build") {
    Remove-Item -Force -Recurse ".\build"
}
if (Test-Path ".\dist") {
    Remove-Item -Force -Recurse ".\dist"
}

python.exe -m pip uninstall -y zipline-cli
python.exe -m build

Write-Output "Done."
