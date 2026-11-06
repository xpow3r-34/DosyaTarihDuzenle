@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>nul
if not errorlevel 1 goto use_py
where python >nul 2>nul
if not errorlevel 1 goto use_python

echo Python 3.10 veya uzeri bulunamadi. Lutfen Python'u kurup yeniden deneyin.
pause
goto end

:use_py
py -3 -c "import PIL, tkinterdnd2" >nul 2>nul
if errorlevel 1 (
    py -3 -m pip install -r requirements.txt
    if errorlevel 1 goto install_error
)
py -3 app.py
goto end

:use_python
python -c "import PIL, tkinterdnd2" >nul 2>nul
if errorlevel 1 (
    python -m pip install -r requirements.txt
    if errorlevel 1 goto install_error
)
python app.py
goto end

:install_error
echo Gerekli paketler kurulamadi. Internet baglantisini ve pip kurulumunu kontrol edin.
pause

:end
endlocal
