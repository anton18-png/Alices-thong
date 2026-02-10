@echo off
setlocal

rem Удаление папок
rmdir /S /Q "C:\Program Files (x86)\Yandex"
rmdir /S /Q "C:\Program Files\Yandex"
rmdir /S /Q "%USERPROFILE%\AppData\Local\Yandex"

rem Удаление файлов (замените имя пользователя, если нужно)
del /Q "%USERPROFILE%\AppData\Roaming\Microsoft\Internet Explorer\Quick Launch\Yandex.lnk"
del /Q "%USERPROFILE%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Yandex.lnk"
del /Q "%USERPROFILE%\AppData\Roaming\Microsoft\Internet Explorer\Quick Launch\User Pinned\TaskBar\yandex.website"

rem Удаление файлов и папок в системе (требует прав администратора)
rmdir /S /Q "C:\Windows\System32\Tasks\Восстановление сервиса обновлений Яндекс Браузера"
rmdir /S /Q "C:\Windows\System32\Tasks\Обновление Браузера Яндекс"
rmdir /S /Q "C:\Windows\System32\Tasks\Системное обновление Браузера Яндекс"
del /Q "C:\Windows\System32\Tasks\Восстановление сервиса обновлений Яндекс Браузера"
del /Q "C:\Windows\System32\Tasks\Обновление Браузера Яндекс"
del /Q "C:\Windows\System32\Tasks\Системное обновление Браузера Яндекс"

rem Удаление файлов журналов и задач
del /Q "C:\Windows\SystemTemp\yandex_browser_installer.log"
del /Q "C:\Windows\SystemTemp\yandex_browser_service_update.log"
del /Q "C:\Windows\Tasks\Восстановление сервиса обновлений Яндекс Браузера.job"
del /Q "C:\Windows\Tasks\Обновление Браузера Яндекс.job"
del /Q "C:\Windows\Tasks\Системное обновление Браузера Яндекс.job"

rem Удаление реестровых ключей
reg delete "HKCU\SOFTWARE\AppDataLow\Yandex" /f >nul 2>&1
reg delete "HKCU\SOFTWARE\Yandex" /f >nul 2>&1
reg delete "HKCU\SOFTWARE\Yandex\YandexBrowser" /f >nul 2>&1

reg delete "HKLM\SOFTWARE\Wow6432Node\Yandex" /f >nul 2>&1
reg delete "HKLM\SOFTWARE\Wow6432Node\Yandex\YandexBrowser" /f >nul 2>&1

rem Удаление папок пользователя
rmdir /S /Q "%USERPROFILE%\AppData\Roaming\Yandex" >nul 2>&1
rmdir /S /Q "%USERPROFILE%\AppData\Local\Yandex" >nul 2>&1
rmdir /S /Q "%USERPROFILE%\AppData\Local\Yandex\YandexBrowser" >nul 2>&1

rem Удаление системных файлов предфetch
del /Q "C:\Windows\Prefetch\SERVICE_UPDATE.EXE-09263450.pf" >nul 2>&1
del /Q "C:\Windows\Prefetch\SERVICE_UPDATE.EXE-22D56917.pf" >nul 2>&1
del /Q "C:\Windows\Prefetch\SERVICE_UPDATE.EXE-4EF6F8CF.pf" >nul 2>&1
del /Q "C:\Windows\Prefetch\SERVICE_UPDATE.EXE-4EF6F8D3.pf" >nul 2>&1
del /Q "C:\Windows\Prefetch\SERVICE_UPDATE.EXE-53ADF4FF.pf" >nul 2>&1
del /Q "C:\Windows\Prefetch\SERVICE_UPDATE.EXE-7A37A775.pf" >nul 2>&1
del /Q "C:\Windows\Prefetch\SERVICE_UPDATE.EXE-B913B237.pf" >nul 2>&1
del /Q "C:\Windows\Prefetch\SERVICE_UPDATE.EXE-E263A33F.pf" >nul 2>&1
del /Q "C:\Windows\Prefetch\SERVICE_UPDATE.EXE-E5740EE6.pf" >nul 2>&1

rem Удаление реестровых ключей
Reg.exe add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\BITS" /v "PerfMMFileName" /t REG_SZ /d "Global\MMF_BITS7f5e4196-c55f-4feb-bb3a-4a1614c0a3c5" /f
Reg.exe delete "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\CompatibilityAdapter\Signatures" /v "Восстановление сервиса обновлений Яндекс Браузера.job" /f
Reg.exe delete "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\CompatibilityAdapter\Signatures" /v "Восстановление сервиса обновлений Яндекс Браузера.job.fp" /f
Reg.exe delete "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\CompatibilityAdapter\Signatures" /v "Обновление Браузера Яндекс.job" /f
Reg.exe delete "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\CompatibilityAdapter\Signatures" /v "Обновление Браузера Яндекс.job.fp" /f
Reg.exe delete "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\CompatibilityAdapter\Signatures" /v "Системное обновление Браузера Яндекс.job" /f
Reg.exe delete "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\CompatibilityAdapter\Signatures" /v "Системное обновление Браузера Яндекс.job.fp" /f
Reg.exe add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\CompatibilityAdapter\Signatures" /f
Reg.exe delete "HKLM\SOFTWARE\Policies\Yandex" /f
Reg.exe delete "HKLM\SOFTWARE\WOW6432Node\Yandex" /f
Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Services\BITS" /v "Start" /t REG_DWORD /d "2" /f
Reg.exe delete "HKCU\SOFTWARE\AppDataLow\Yandex" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\.crx" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\.css\OpenWithProgids" /v "YandexCSS.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe add "HKCU\SOFTWARE\Classes\.css\OpenWithProgids" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\.epub\OpenWithProgids" /v "YandexEPUB.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe add "HKCU\SOFTWARE\Classes\.epub\OpenWithProgids" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\.fb2\OpenWithProgids" /v "YandexFB2.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe add "HKCU\SOFTWARE\Classes\.fb2\OpenWithProgids" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\.gif\OpenWithProgids" /v "YandexGIF.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe add "HKCU\SOFTWARE\Classes\.gif\OpenWithProgids" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\.htm\OpenWithProgids" /v "YandexHTML.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe add "HKCU\SOFTWARE\Classes\.htm\OpenWithProgids" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\.html\OpenWithProgids" /v "YandexHTML.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe add "HKCU\SOFTWARE\Classes\.html\OpenWithProgids" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\.infected\OpenWithProgids" /v "YandexINFE.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe add "HKCU\SOFTWARE\Classes\.infected\OpenWithProgids" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\.jpeg\OpenWithProgids" /v "YandexJPEG.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe add "HKCU\SOFTWARE\Classes\.jpeg\OpenWithProgids" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\.jpg\OpenWithProgids" /v "YandexJPEG.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe add "HKCU\SOFTWARE\Classes\.jpg\OpenWithProgids" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\.js\OpenWithProgids" /v "YandexJS.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe add "HKCU\SOFTWARE\Classes\.js\OpenWithProgids" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\.mhtml\OpenWithProgids" /v "YandexHTML.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe add "HKCU\SOFTWARE\Classes\.mhtml\OpenWithProgids" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\.pdf\OpenWithProgids" /v "YandexPDF.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe add "HKCU\SOFTWARE\Classes\.pdf\OpenWithProgids" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\.png\OpenWithProgids" /v "YandexPNG.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe add "HKCU\SOFTWARE\Classes\.png\OpenWithProgids" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\.shtml\OpenWithProgids" /v "YandexHTML.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe add "HKCU\SOFTWARE\Classes\.shtml\OpenWithProgids" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\.svg\OpenWithProgids" /v "YandexSVG.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe add "HKCU\SOFTWARE\Classes\.svg\OpenWithProgids" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\.swf\OpenWithProgids" /v "YandexSWF.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe add "HKCU\SOFTWARE\Classes\.swf\OpenWithProgids" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\.tif\OpenWithProgids" /v "YandexTIFF.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe add "HKCU\SOFTWARE\Classes\.tif\OpenWithProgids" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\.tiff\OpenWithProgids" /v "YandexTIFF.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe add "HKCU\SOFTWARE\Classes\.tiff\OpenWithProgids" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\.txt\OpenWithProgids" /v "YandexTXT.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe add "HKCU\SOFTWARE\Classes\.txt\OpenWithProgids" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\.webm\OpenWithProgids" /v "YandexWEBM.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe add "HKCU\SOFTWARE\Classes\.webm\OpenWithProgids" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\.webp\OpenWithProgids" /v "YandexWEBP.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe add "HKCU\SOFTWARE\Classes\.webp\OpenWithProgids" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\.xht\OpenWithProgids" /v "YandexHTML.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe add "HKCU\SOFTWARE\Classes\.xht\OpenWithProgids" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\.xhtml\OpenWithProgids" /v "YandexHTML.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe add "HKCU\SOFTWARE\Classes\.xhtml\OpenWithProgids" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\.xml\OpenWithProgids" /v "YandexXML.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe add "HKCU\SOFTWARE\Classes\.xml\OpenWithProgids" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\SystemFileAssociations\.bmp" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\SystemFileAssociations\.gif" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\SystemFileAssociations\.jpeg" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\SystemFileAssociations\.jpg" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\SystemFileAssociations\.png" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\SystemFileAssociations\.tif" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\SystemFileAssociations\.tiff" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\SystemFileAssociations\.webp" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\yabrowser" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\YandexBrowser.crx" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\YandexCRX.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\YandexCSS.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\YandexEPUB.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\YandexFB2.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\YandexGIF.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\YandexHTML.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\YandexINFE.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\YandexJPEG.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\YandexJS.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\YandexPDF.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\YandexPNG.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\YandexSVG.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\YandexSWF.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\YandexTIFF.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\YandexTXT.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\YandexWEBM.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\YandexWEBP.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\YandexXML.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe delete "HKCU\SOFTWARE\Clients\StartMenuInternet\Yandex.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe delete "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\browser.exe" /f
Reg.exe delete "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\FeatureUsage\AppBadgeUpdated" /v "Yandex.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe delete "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\FeatureUsage\AppBadgeUpdated" /v "Yandex.T2FVXDHUUCNR7T6RIY5A6G74.USERDATA.Default" /f
Reg.exe add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\FeatureUsage\AppBadgeUpdated" /f
Reg.exe delete "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\FeatureUsage\AppSwitched" /v "Yandex.T2FVXDHUUCNR7T6RIY5A6G74.USERDATA.Default" /f
Reg.exe delete "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\FeatureUsage\AppSwitched" /v "Yandex.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\FeatureUsage\AppSwitched" /f
Reg.exe delete "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" /v "YandexBrowserAutoLaunch_45886AE68CD319C7351FF54A1DBD4B87" /f
Reg.exe add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" /f
Reg.exe add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Search" /v "InstalledWin32AppsRevision" /t REG_SZ /d "{AAC40156-D28D-46F6-B10A-BC76174A321C}" /f
Reg.exe delete "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Search\JumplistData" /f
Reg.exe delete "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\YandexBrowser" /f
Reg.exe delete "HKCU\SOFTWARE\Policies\Yandex" /f
Reg.exe delete "HKCU\SOFTWARE\RegisteredApplications" /v "Yandex.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe add "HKCU\SOFTWARE\RegisteredApplications" /f
Reg.exe delete "HKCU\SOFTWARE\Yandex" /f
Reg.exe add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\BITS" /v "PerfMMFileName" /t REG_SZ /d "Global\MMF_BITS9ca438c6-fdd3-4c57-9c70-ee4909a7329a" /f
Reg.exe delete "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\CompatibilityAdapter\Signatures" /v "Восстановление сервиса обновлений Яндекс Браузера.job" /f
Reg.exe delete "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\CompatibilityAdapter\Signatures" /v "Восстановление сервиса обновлений Яндекс Браузера.job.fp" /f
Reg.exe delete "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\CompatibilityAdapter\Signatures" /v "Обновление Браузера Яндекс.job" /f
Reg.exe delete "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\CompatibilityAdapter\Signatures" /v "Обновление Браузера Яндекс.job.fp" /f
Reg.exe delete "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\CompatibilityAdapter\Signatures" /v "Системное обновление Браузера Яндекс.job" /f
Reg.exe delete "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\CompatibilityAdapter\Signatures" /v "Системное обновление Браузера Яндекс.job.fp" /f
Reg.exe add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\CompatibilityAdapter\Signatures" /f
Reg.exe delete "HKLM\SOFTWARE\WOW6432Node\Yandex" /f
Reg.exe delete "HKLM\SYSTEM\CurrentControlSet\Services\YandexBrowserService" /f
Reg.exe delete "HKCU\SOFTWARE\AppDataLow\Yandex" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\.crx" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\.css\OpenWithProgids" /v "YandexCSS.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe add "HKCU\SOFTWARE\Classes\.css\OpenWithProgids" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\.epub\OpenWithProgids" /v "YandexEPUB.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe add "HKCU\SOFTWARE\Classes\.epub\OpenWithProgids" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\.fb2\OpenWithProgids" /v "YandexFB2.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe add "HKCU\SOFTWARE\Classes\.fb2\OpenWithProgids" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\.gif\OpenWithProgids" /v "YandexGIF.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe add "HKCU\SOFTWARE\Classes\.gif\OpenWithProgids" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\.htm\OpenWithProgids" /v "YandexHTML.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe add "HKCU\SOFTWARE\Classes\.htm\OpenWithProgids" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\.html\OpenWithProgids" /v "YandexHTML.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe add "HKCU\SOFTWARE\Classes\.html\OpenWithProgids" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\.infected\OpenWithProgids" /v "YandexINFE.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe add "HKCU\SOFTWARE\Classes\.infected\OpenWithProgids" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\.jpeg\OpenWithProgids" /v "YandexJPEG.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe add "HKCU\SOFTWARE\Classes\.jpeg\OpenWithProgids" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\.jpg\OpenWithProgids" /v "YandexJPEG.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe add "HKCU\SOFTWARE\Classes\.jpg\OpenWithProgids" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\.js\OpenWithProgids" /v "YandexJS.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe add "HKCU\SOFTWARE\Classes\.js\OpenWithProgids" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\.mhtml\OpenWithProgids" /v "YandexHTML.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe add "HKCU\SOFTWARE\Classes\.mhtml\OpenWithProgids" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\.pdf\OpenWithProgids" /v "YandexPDF.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe add "HKCU\SOFTWARE\Classes\.pdf\OpenWithProgids" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\.png\OpenWithProgids" /v "YandexPNG.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe add "HKCU\SOFTWARE\Classes\.png\OpenWithProgids" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\.shtml\OpenWithProgids" /v "YandexHTML.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe add "HKCU\SOFTWARE\Classes\.shtml\OpenWithProgids" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\.svg\OpenWithProgids" /v "YandexSVG.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe add "HKCU\SOFTWARE\Classes\.svg\OpenWithProgids" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\.swf\OpenWithProgids" /v "YandexSWF.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe add "HKCU\SOFTWARE\Classes\.swf\OpenWithProgids" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\.tif\OpenWithProgids" /v "YandexTIFF.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe add "HKCU\SOFTWARE\Classes\.tif\OpenWithProgids" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\.tiff\OpenWithProgids" /v "YandexTIFF.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe add "HKCU\SOFTWARE\Classes\.tiff\OpenWithProgids" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\.txt\OpenWithProgids" /v "YandexTXT.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe add "HKCU\SOFTWARE\Classes\.txt\OpenWithProgids" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\.webm\OpenWithProgids" /v "YandexWEBM.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe add "HKCU\SOFTWARE\Classes\.webm\OpenWithProgids" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\.webp\OpenWithProgids" /v "YandexWEBP.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe add "HKCU\SOFTWARE\Classes\.webp\OpenWithProgids" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\.xht\OpenWithProgids" /v "YandexHTML.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe add "HKCU\SOFTWARE\Classes\.xht\OpenWithProgids" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\.xhtml\OpenWithProgids" /v "YandexHTML.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe add "HKCU\SOFTWARE\Classes\.xhtml\OpenWithProgids" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\.xml\OpenWithProgids" /v "YandexXML.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe add "HKCU\SOFTWARE\Classes\.xml\OpenWithProgids" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\yabrowser" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\YandexBrowser.crx" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\YandexCRX.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\YandexCSS.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\YandexEPUB.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\YandexFB2.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\YandexGIF.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\YandexHTML.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\YandexINFE.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\YandexJPEG.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\YandexJS.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\YandexPDF.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\YandexPNG.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\YandexSVG.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\YandexSWF.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\YandexTIFF.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\YandexTXT.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\YandexWEBM.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\YandexWEBP.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe delete "HKCU\SOFTWARE\Classes\YandexXML.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe delete "HKCU\SOFTWARE\Clients\StartMenuInternet\Yandex.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe delete "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\browser.exe" /f
Reg.exe delete "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.crx\UserChoice" /f
Reg.exe delete "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.css\UserChoice" /f
Reg.exe delete "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.epub\UserChoice" /f
Reg.exe delete "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.fb2\UserChoice" /f
Reg.exe delete "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.infected\UserChoice" /f
Reg.exe delete "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.js\UserChoice" /f
Reg.exe delete "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.mhtml\UserChoice" /f
Reg.exe add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.pdf\UserChoice" /v "Hash" /t REG_SZ /d "48XTwTC0twQ=" /f
Reg.exe add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.pdf\UserChoice" /v "ProgId" /t REG_SZ /d "MSEdgePDF" /f
Reg.exe delete "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.shtml\UserChoice" /f
Reg.exe delete "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.svg\UserChoice" /f
Reg.exe delete "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.swf\UserChoice" /f
Reg.exe delete "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.webp\UserChoice" /f
Reg.exe delete "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.xht\UserChoice" /f
Reg.exe delete "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.xhtml\UserChoice" /f
Reg.exe delete "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" /v "YandexBrowserAutoLaunch_45886AE68CD319C7351FF54A1DBD4B87" /f
Reg.exe add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" /f
Reg.exe add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Search" /v "InstalledWin32AppsRevision" /t REG_SZ /d "{F1886E63-EAD6-467A-AA82-62FCC7B7A91D}" /f
Reg.exe delete "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\YandexBrowser" /f
Reg.exe delete "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\YaPinLancher" /f
Reg.exe delete "HKCU\SOFTWARE\RegisteredApplications" /v "Yandex.T2FVXDHUMVUCNR7T6RIY5A6G74" /f
Reg.exe add "HKCU\SOFTWARE\RegisteredApplications" /f
Reg.exe delete "HKCU\SOFTWARE\Yandex" /f

rem Удаление файлов с "Yandex" в названиях в папках
C:
cd "%USERPROFILE%\AppData\Roaming\Microsoft\Internet Explorer\Quick Launch\User Pinned\TaskBar"
del *yandex*
cd "%USERPROFILE%\AppData\Roaming\Microsoft\Internet Explorer\Quick Launch\User Pinned"
del *yandex*

cd C:\Apps\Alices-Thong
start "" "PostInstall.exe"