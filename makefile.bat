@echo off
cd C:\Users\d.biryuchkov\.qgis2\python\plugins\raz
SET PYTHONPATH=C:\PROGRA~1\QGISES~1\apps\Python27\Lib
SET PYTHONHOME=C:\PROGRA~1\QGISES~1\apps\Python27
SET PATH=C:\PROGRA~1\QGISES~1\apps\Python27\Scripts;C:\PROGRA~1\QGISES~1\bin\
pyrcc4 -o resources_rc.py resources.qrc
REM call pyuic4.bat -d -o route_ui.py ui\route.ui
call pyuic4.bat -o route_ui.py ui\route.ui
call pyuic4.bat -o zone_ui.py ui\zone.ui
pylupdate4  raz.py route.py ui\route.ui route_worker.py zone.py ui\zone.ui zone_worker.py -ts i18n\raz_ru_RU.ts
lrelease i18n\raz_ru_RU.ts