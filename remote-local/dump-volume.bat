@echo off
setlocal enabledelayedexpansion

set volume=%1
set backupdir=".\\volume\\%volume%\\backup"
set timestamp=%date:~10,4%%date:~4,2%%date:~7,2%%time:~0,2%%time:~3,2%%time:~6,2%

REM Create the dump directory
md "%backupdir%"

for /f "tokens=*" %%i in ('docker run -d --rm --mount "type=volume,source=!volume!,destination=/data" ubuntu sleep infinity') do set containerId=%%i

docker exec "!containerId!" bash -c "cd /data && tar -czf ../data.tar.gz ."
docker cp "!containerId!:/data.tar.gz" "%backupdir%\\%timestamp%.tar.gz"

docker stop "!containerId!"