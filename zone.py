# -*- coding: utf-8 -*-
import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

from zone_ui import Ui_DialogZone
from zone_worker import ZoneWorker

class Zone(QDialog, Ui_DialogZone):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.iface = parent
        self.qgsMapCanvas = None
        self.worker = None
        self.thread = None

        self.mMapLayerComboBoxPoints.setFilters(QgsMapLayerProxyModel.PointLayer)
        self.mMapLayerComboBoxRoad.setFilters(QgsMapLayerProxyModel.LineLayer)

        self.mFieldComboBoxPointsId.setFilters(QgsFieldProxyModel.Int|QgsFieldProxyModel.LongLong)
        self.mFieldComboBoxPointsName.setFilters(QgsFieldProxyModel.String)
        
        self.mMapLayerComboBoxCalculatedZone.setFilters(QgsMapLayerProxyModel.PolygonLayer)
        self.connect(self.mMapLayerComboBoxPoints, SIGNAL("currentIndexChanged(int)"), 
                                                          self.checkSelectedEnable)        
        self.connect(self.mMapLayerComboBoxRoad, SIGNAL("currentIndexChanged(int)"), 
                                                        self.checkSelectedLayer)        
        self.connect(self.mMapLayerComboBoxCalculatedZone, SIGNAL("currentIndexChanged(int)"), 
                                                                  self.checkSelectedLayer)        
        self.connect(self.mFieldComboBoxPointsId, SIGNAL("currentIndexChanged(int)"), 
                                                         self.checkSelectedLayer)
        self.connect(self.mFieldComboBoxPointsName, SIGNAL("currentIndexChanged(int)"), 
                                                           self.checkSelectedLayer)
        self.connect(self.pushButtonExit, SIGNAL("clicked()"), self.closeDialog)        
        self.connect(self.pushButtonStart, SIGNAL("clicked()"), self.calculateZone)        
        self.connect(self.pushButtonStop, SIGNAL("clicked()"), self.stopWork)        

        self.settings = QSettings("openLand", "Raz")
        
        self.readSettings()
        self.checkSelectedEnable()

    def readSettings(self):
        self.maxLength = self.settings.value('zone/maxLength', 100)
        self.doubleSpinBox.setProperty("value", self.maxLength)
        
    def writeSettings(self):
        self.settings.setValue('zone/maxLength', self.doubleSpinBox.value())
        
    def checkSelectedEnable(self):
        self.source_point_layer = self.mMapLayerComboBoxPoints.currentLayer()

        if self.source_point_layer is not None:
            self.mFieldComboBoxPointsId.setLayer(self.source_point_layer)
            self.mFieldComboBoxPointsName.setLayer(self.source_point_layer)
            self.spl_selection = self.source_point_layer.selectedFeatures()
            if len(self.spl_selection) > 0:
                self.checkBoxSelectedPoints.setEnabled(True)
            else:
                self.checkBoxSelectedPoints.setEnabled(False)
                self.checkBoxSelectedPoints.setChecked(False)
        
        self.checkSelectedLayer()

    def checkSelectedLayer(self):
        if (self.mMapLayerComboBoxPoints.currentLayer() is not None and
            self.mMapLayerComboBoxRoad.currentLayer() is not None and
            self.mMapLayerComboBoxCalculatedZone.currentLayer() is not None):
            
            if not self.pushButtonStop.isEnabled():
#                self.pushButtonStart.setEnabled(True)
                self.checkSelectedField()
            else:
                self.pushButtonStart.setEnabled(False)
        else:
            self.pushButtonStart.setEnabled(False)

    def checkSelectedField(self):
        if (self.mFieldComboBoxPointsId.currentField() is not None and
            self.mFieldComboBoxPointsName.currentField() is not None and
            self.mFieldComboBoxPointsId.currentField() != '' and
            self.mFieldComboBoxPointsName.currentField() != ''):
            
            if not self.pushButtonStop.isEnabled():
                self.pushButtonStart.setEnabled(True)
            else:
                self.pushButtonStart.setEnabled(False)
        else:
            self.pushButtonStart.setEnabled(False)


    def calculateZone(self):
        self.writeSettings()
        
        worker = ZoneWorker(self.iface)

        worker.sourcePointLayer = self.source_point_layer
        if self.checkBoxSelectedPoints.isChecked():
            iter = self.spl_selection
        else:
            iter = self.source_point_layer.getFeatures()
        for every in iter:
            idf = every.attribute(self.mFieldComboBoxPointsId.currentField())
            name = every.attribute(self.mFieldComboBoxPointsName.currentField())
            geom = every.geometry()
            if geom.isMultipart():
                point = geom.asMultiPoint()[0]
            else:
                point = geom.asPoint()

            worker.sourcePoint.append([idf, name, point])

        worker.road = self.mMapLayerComboBoxRoad.currentLayer()
        worker.calculatedZone = self.mMapLayerComboBoxCalculatedZone.currentLayer()
        worker.maxLength = self.doubleSpinBox.value()
        worker.qgsMapCanvas = self.qgsMapCanvas
        worker.isContinueWork = True

        thread = QThread(self)
        worker.moveToThread(thread)
        thread.started.connect(worker.run)

        worker.progressChanged.connect(self.progressBar.setValue)
        worker.runned.connect(self.showButtons)
        
        thread.start()

        self.thread = thread
        self.worker = worker

    def showButtons(self, isRunned):
        self.pushButtonStart.setEnabled(not isRunned)
        self.pushButtonStop.setEnabled(isRunned)
        if not isRunned:
            self.worker.deleteLater()
            self.thread.quit()
            self.thread.wait()
            self.thread.deleteLater()

    def stopWork(self):
        self.worker.isContinueWork = False

    def closeDialog(self):
        self.close()
