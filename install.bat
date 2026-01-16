@echo off
REM install.bat - Installe les dépendances sur Windows

echo [+] Vérification de Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python non trouvé. Veuillez installer Python 3.7+ depuis https://python.org
    pause
    exit /b 1
)

echo [+] Mise à jour de pip...
python -m pip install --upgrade pip

echo [+] Installation de aiohttp...
pip install aiohttp

echo [+] Installation de Git (optionnel)...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Git non trouvé. Téléchargez-le depuis https://git-scm.com/download/win
)

echo.
echo [✅] Installation terminée !
echo.
echo Utilisez PowerShell ou CMD pour lancer :
echo   python server\simple-server.py 8000          (serveur)
echo   python attacker\http-flood-ultimate.py http://192.168.1.10:8000  (attaque)
pause
