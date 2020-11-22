rmdir /s /q dist

python -m PyInstaller nydus.spec
IF %ERRORLEVEL% EQU 1 (
    exit 1
)

robocopy src/plugins dist/plugins /MIR
FOR /d /r dist/ %%d IN ("__pycache__", ".gitignore") DO @IF EXIST "%%d" rd /s /q "%%d"

exit 0
