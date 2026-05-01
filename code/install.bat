@echo off
setlocal

rem Задайте путь к исходной папке, заменив %USERNAME% на текущего пользователя
set "sourceFolder=%USERPROFILE%\AppData\Local\Yandex\YandexBrowser\Application"

rem Путь назначения
set "destFolder=%cd%\app"

rem Создаем целевую папку, если она не существует
if not exist "%destFolder%" (
    mkdir "%destFolder%"
)

rem Копируем все файлы и папки из исходной в целевую
xcopy "%sourceFolder%\*" "%destFolder%\" /S /E /Y /H

cd app
CleanYandex.bat

cd ..
start "" "StartAlicesThong.exe"