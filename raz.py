# -*- coding: utf-8 -*-

import os
import resources_rc

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
from route import Route
from zone import Zone


class Raz:
    def __init__(self, iface):
        self.iface = iface
        pluginPath = os.path.dirname(__file__)

        overrideLocale = QSettings().value('locale/overrideFlag', False, type=bool)
        if not overrideLocale:
            localeFullName = QLocale.system().name()
        else:
            localeFullName = QSettings().value('locale/userLocale', '')

        self.localePath = os.path.join(pluginPath, 'i18n', 
                                       'raz_{}.qm'.format(localeFullName))
        if QFileInfo(self.localePath).exists():
            self.translator = QTranslator()
            self.translator.load(self.localePath)
            QCoreApplication.installTranslator(self.translator)

        self.__name = QCoreApplication.translate('Plugin','Routes and zones calculate tool')

        self.dialogRoute = Route(self.iface.mainWindow())
        self.dialogRoute.qgsMapCanvas = self.iface.mapCanvas()

        self.dialogZone = Zone(self.iface.mainWindow())
        self.dialogZone.qgsMapCanvas = self.iface.mapCanvas()

    def initGui(self):
        self.action_route = QAction(QIcon(':/icons/route.png'),
            QCoreApplication.translate('Plugin', 'Route calculate tool'),
            self.iface.mainWindow())
        self.iface.addPluginToMenu(self.__name, self.action_route)
        self.iface.addToolBarIcon(self.action_route)
        self.action_route.triggered.connect(self.run_route)

        self.action_zone = QAction(QIcon(':/icons/zone.png'),
            QCoreApplication.translate('Plugin', 'Zone calculate tool'),
            self.iface.mainWindow())
        self.iface.addPluginToMenu(self.__name, self.action_zone)
        self.iface.addToolBarIcon(self.action_zone)
        self.action_zone.triggered.connect(self.run_zone)
    
    def run_route(self):
        self.dialogRoute.checkSelectedEnable()
        result = self.dialogRoute.show()

    def run_zone(self):
        self.dialogZone.checkSelectedEnable()
        result = self.dialogZone.show()

    def unload(self):
        self.iface.removePluginMenu(self.__name, self.action_route)
        self.iface.removeToolBarIcon(self.action_route)

        self.iface.removePluginMenu(self.__name, self.action_zone)
        self.iface.removeToolBarIcon(self.action_zone)
