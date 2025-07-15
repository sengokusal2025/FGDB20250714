@echo off
REM Auto-generated batch file from operation.txt
REM Generated at: 2025-07-10 15:28:21.201911
REM
REM Format: python ./f/func.py -i x -o {y+timestamp}

REM Operation 1: y1 = f1(x1)
python ./f/func.py -i x1 -o y1_20250710_152821_201
if errorlevel 1 goto error

echo All operations completed successfully.
goto end

:error
echo Error occurred during operation execution.
exit /b 1

:end
