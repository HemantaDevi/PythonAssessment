@echo off
cls
set PATH=%PATH%;C:\python
:my_loop
IF %1=="" GOTO completed
  python C:\subsceneSub.py %1
  SHIFT
  GOTO my_loop
:completed