@echo off
setlocal

:: Set paths
set TASK_NAME=ClipboardLangShifter
set SCRIPT_DIR=%~dp0
set VBS_PATH="%SCRIPT_DIR%launch_silent.vbs"
set TASK_XML="%SCRIPT_DIR%task.xml"

:: Generate VBS script
echo Set WshShell = CreateObject("WScript.Shell") > %VBS_PATH%
echo WshShell.Run Chr(34) ^& "%SCRIPT_DIR%run.bat" ^& Chr(34), 0 >> %VBS_PATH%
echo Set WshShell = Nothing >> %VBS_PATH%

:: Remove old task if it exists
schtasks /Delete /F /TN "%TASK_NAME%" >nul 2>&1

:: Create XML file for task
echo ^<?xml version="1.0" encoding="UTF-16"?^> > %TASK_XML%
echo ^<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task"^> >> %TASK_XML%
echo   ^<RegistrationInfo^> >> %TASK_XML%
echo     ^<Description^>Fixes keyboard layout on logon^</Description^> >> %TASK_XML%
echo   ^</RegistrationInfo^> >> %TASK_XML%
echo   ^<Triggers^> >> %TASK_XML%
echo     ^<LogonTrigger^> >> %TASK_XML%
echo       ^<Enabled^>true^</Enabled^> >> %TASK_XML%
echo     ^</LogonTrigger^> >> %TASK_XML%
echo   ^</Triggers^> >> %TASK_XML%
echo   ^<Settings^> >> %TASK_XML%
echo     ^<DisallowStartIfOnBatteries^>false^</DisallowStartIfOnBatteries^> >> %TASK_XML%
echo     ^<StopIfGoingOnBatteries^>false^</StopIfGoingOnBatteries^> >> %TASK_XML%
echo     ^<MultipleInstancesPolicy^>IgnoreNew^</MultipleInstancesPolicy^> >> %TASK_XML%
echo     ^<StartWhenAvailable^>true^</StartWhenAvailable^> >> %TASK_XML%
echo     ^<IdleSettings^> >> %TASK_XML%
echo       ^<StopOnIdleEnd^>true^</StopOnIdleEnd^> >> %TASK_XML%
echo       ^<RestartOnIdle^>false^</RestartOnIdle^> >> %TASK_XML%
echo     ^</IdleSettings^> >> %TASK_XML%
echo   ^</Settings^> >> %TASK_XML%
echo   ^<Actions Context="Author"^> >> %TASK_XML%
echo     ^<Exec^> >> %TASK_XML%
echo       ^<Command^>wscript.exe^</Command^> >> %TASK_XML%
echo       ^<Arguments^>%VBS_PATH%^</Arguments^> >> %TASK_XML%
echo       ^<WorkingDirectory^>%SCRIPT_DIR%^</WorkingDirectory^> >> %TASK_XML%
echo     ^</Exec^> >> %TASK_XML%
echo   ^</Actions^> >> %TASK_XML%
echo ^</Task^> >> %TASK_XML%

:: Create new task
schtasks /Create /TN "%TASK_NAME%" /XML %TASK_XML% /F

:: Start The Task for First Time
schtasks /Run /TN "%TASK_NAME%"

:: Clean up (optional)
del %TASK_XML%

pause
endlocal