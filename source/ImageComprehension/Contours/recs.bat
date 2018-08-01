echo off
title rectangle finder
REM goal is to have the names of files containting rectangles written to a file
set outfile=%1
set imagedir=%2

FOR /R %imagedir% %%G in (*.png) DO python C:\Users\TJAMS002\Documents\^
ComputerScience\Thesis\RoomFinder\source\ImageComprehension\contour_test.py -f %%G >> %outfile%
REM FOR /R in %imagedir% %%G in 