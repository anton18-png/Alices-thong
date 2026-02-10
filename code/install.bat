@echo off
setlocal

rem Задайте путь к исходной папке, заменив %USERNAME% на текущего пользователя
set "sourceFolder=%USERPROFILE%\AppData\Local\Yandex\YandexBrowser\Application"

rem Путь назначения
set "destFolder=C:\Apps\Alices-Thong\browser"

rem Создаем целевую папку, если она не существует
if not exist "%destFolder%" (
    mkdir "%destFolder%"
)

rem Копируем все файлы и папки из исходной в целевую
xcopy "%sourceFolder%\*" "%destFolder%\" /S /E /Y /H

rem Теперь копируем папки из User Data
set "userDataFolder=%USERPROFILE%\AppData\Local\Yandex\YandexBrowser\Application\User Data"
set "destUserData=C:\Apps\Alices-Thong\user_data"

rem Создаем папку назначения для User Data, если не существует
if not exist "%destUserData%" (
    mkdir "%destUserData%"
)

rem Копируем все содержимое из User Data в новую папку
xcopy "%userDataFolder%\*" "%destUserData%\" /S /E /Y /H

rem Запускаем файл remove-yandex.exe из папки назначения
start "" "C:\Apps\Alices-Thong\remove-yandex.exe"

