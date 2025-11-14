@echo off
echo Starting Invoice Audit System (Fast Mode with China Mirror)...
echo.

echo Step 1: Check Python...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed
    pause
    exit /b 1
)

echo Step 2: Installing dependencies with China mirror...
cd backend
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
if errorlevel 1 (
    echo Trying alternative mirror...
    pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
)

echo Step 3: Starting backend server...
start "Backend" cmd /k "python main.py"
timeout /t 3 /nobreak > nul

echo Step 4: Starting frontend server...
cd ..\frontend
start "Frontend" cmd /k "python -m http.server 5173"
timeout /t 2 /nobreak > nul

echo.
echo System started successfully!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo Opening browser in 3 seconds...
timeout /t 3 /nobreak > nul
start http://localhost:5173

echo.
echo Press any key to exit (servers will keep running)
pause > nul
