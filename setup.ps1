# Download OpenOCD from Github


$downloadUrl = "https://github.com/xpack-dev-tools/openocd-xpack/releases/download/v0.12.0-4/xpack-openocd-0.12.0-4-win32-x64.zip"
$downloadPath = "./openocd.zip"

Invoke-WebRequest -Uri $downloadUrl -OutFile $downloadPath

# Unzip the downloaded file
Expand-Archive -Path $downloadPath -DestinationPath "./"

# Delete zip archive
Remove-Item $downloadPath