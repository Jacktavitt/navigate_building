ECHO OFF
TITLE rectangle finder
REM goal is to have the names of files containting rectangles written to a file

IF NOT "%~1"=="" IF NOT "%~2"=="" GOTO RUN ELSE GOTO BLANK

:BLANK 
ECHO Sample Call: recs.bat ..output file.. ..directory of images..
GOTO DONE

:RUN
SET outfile=%1
SET imagedir=%2
FOR /R %imagedir% %%G in (*.png) DO python C:\Users\TJAMS002\Documents\^
ComputerScience\Thesis\RoomFinder\source\ImageComprehension\Contours\contour_test.py -f %%G >> %outfile%
GOTO DONE

:DONE
ECHO done!