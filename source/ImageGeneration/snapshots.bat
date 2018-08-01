echo off
title snapshot batch file
REM goal is to pass a directory of hallway images and have it generate n snapshots of each
REM sample call source\ImageGeneration\snapshots.bat C:\Users\TJAMS002\Documents\ComputerScience\Thesis\RoomFinder\source\ImageGeneration\HALLWAYS\ 25 10 C:\Users\TJAMS002\Documents\ComputerScience\Thesis\RoomFinder\source\ImageGeneration\SNAPS\


IF NOT "%~1"=="" IF NOT "%~2"=="" IF NOT "%~3"=="" IF NOT "%~4"=="" GOTO RUN ELSE GOTO BLANK

:BLANK 
ECHO Sample Call: snapshots.bat  ..directory containing files..  ..percent size of snaps..  ..num snaps..  ..save directory..
GOTO DONE

:RUN
set odirectory=%1
set percent=%2
set num=%3
set sdir=%4
echo all files in %odirectory% with have a kernel of %percent% percent run %num% times. Files will be saved to %sdir%
FOR /R %odirectory% %%G IN (*.png) DO python C:\Users\TJAMS002\Documents\ComputerScience\Thesis\RoomFinder\source\ImageGeneration\snapshot.py -f %%G -p %percent% -n %num% -d %sdir%
GOTO DONE

:DONE
echo done!