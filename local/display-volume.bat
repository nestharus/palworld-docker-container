@echo off
setlocal enabledelayedexpansion

set "volume=%~1"

docker run --rm -v %volume%:/palworld/Pal/Saved/SaveGames alpine ls -laR /palworld/Pal/Saved/SaveGames