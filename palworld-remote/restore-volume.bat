@echo off
setlocal enabledelayedexpansion

REM Process named parameters
:loop
if "%~1"=="" goto :endloop
if "%~1"=="--volume" (
  set "volume=%~2"
  shift /1
)
if "%~1"=="--to-volume" (
  set "to_volume=%~2"
  shift /1
)
if "%~1"=="--from-volume" (
  set "from_volume=%~2"
  shift /1
)
if "%~1"=="--dump-name" (
  set "dump_name=%~2"
  shift /1
)
shift /1
goto :loop
:endloop

if not defined volume (
  if not defined from_volume (
    echo Error: volume is a required parameter. Provide it as --volume=value.
    exit /b 1
  )
  if not defined to_volume (
    echo Error: volume is a required parameter. Provide it as --volume=value.
    exit /b 1
  )
) else (
  if defined from_volume (
    echo Error: must either use --volume or --from-volume and --to-volume
    exit /b 1
  )
  if defined to_volume (
    echo Error: must either use --volume or --from-volume and --to-volume
    exit /b 1
  )
)

if not defined volume (
  set "volume=%from_volume%"
)
if not defined from_volume (
  set "from_volume=%volume%"
)
if not defined to_volume (
  set "to_volume=%volume%"
)

set "backupdir=./volume/%from_volume%/backup"

if not defined dump_name (
  for /F "delims=" %%I in ('dir /B /O:N /A:-D "%backupdir%"') do (
    set "dump_name=%%I"
  )
)

if not "%dump_name:~-7%"==".tar.gz" (
  set "dump_name=%dump_name%.tar.gz"
)

REM Docker command. Ensure Docker is installed and added to PATH.
docker run --rm --mount source="%to_volume%",destination=/data --mount type=bind,source="%cd%/%backupdir%",destination=/backup-dir cm2network/steamcmd:root bash -c "rm -rf /data/* && tar xvzf /backup-dir/%dump_name% -C /data . && chown -R steam:steam /data"