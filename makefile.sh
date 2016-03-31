#!/bin/sh

pyrcc4 -o resources_rc.py resources.qrc
pyuic4 -o route_ui.py ui/route.ui
pyuic4 -o zone_ui.py ui/zone.ui
pylupdate4  raz.py route.py ui/route.ui route_worker.py zone.py ui/zone.ui zone_worker.py -ts i18n/raz_ru_RU.ts
lrelease i18n/raz_ru_RU.ts