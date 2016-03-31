# -*- coding: utf-8 -*-
import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

from route_ui import Ui_DialogRoute
from route_worker import RouteWorker

class Route(QDialog, Ui_DialogRoute):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.iface = parent
        self.qgsMapCanvas = None
        self.worker = None
        self.thread = None

        self.mMapLayerComboBoxSourcePoints.setFilters(QgsMapLayerProxyModel.PointLayer)
        self.mMapLayerComboBoxTargetPoints.setFilters(QgsMapLayerProxyModel.PointLayer)
        self.mMapLayerComboBoxRoad.setFilters(QgsMapLayerProxyModel.LineLayer)
        self.mMapLayerComboBoxCalculatedRoute.setFilters(QgsMapLayerProxyModel.LineLayer)
        self.mMapLayerComboBoxManyLongPath.setFilters(QgsMapLayerProxyModel.NoGeometry)

        self.mFieldComboBoxSourcePointsId.setFilters(QgsFieldProxyModel.Int|QgsFieldProxyModel.LongLong)
        self.mFieldComboBoxSourcePointsName.setFilters(QgsFieldProxyModel.String)
        self.mFieldComboBoxTargetPointsId.setFilters(QgsFieldProxyModel.Int|QgsFieldProxyModel.LongLong)
        self.mFieldComboBoxTargetPointsName.setFilters(QgsFieldProxyModel.String)

        self.connect(self.mMapLayerComboBoxSourcePoints, SIGNAL("currentIndexChanged(int)"), 
                                                                self.checkSelectedEnable)
        self.connect(self.mMapLayerComboBoxTargetPoints, SIGNAL("currentIndexChanged(int)"), 
                                                                self.checkSelectedEnable)
        self.connect(self.mMapLayerComboBoxRoad, SIGNAL("currentIndexChanged(int)"), 
                                                        self.checkSelectedLayer)
        self.connect(self.mMapLayerComboBoxCalculatedRoute, SIGNAL("currentIndexChanged(int)"), 
                                                                   self.checkSelectedLayer)
        self.connect(self.mMapLayerComboBoxManyLongPath, SIGNAL("currentIndexChanged(int)"), 
                                                                self.checkSelectedLayer)
        self.connect(self.mFieldComboBoxSourcePointsId, SIGNAL("currentIndexChanged(int)"), 
                                                               self.checkSelectedLayer)
        self.connect(self.mFieldComboBoxSourcePointsName, SIGNAL("currentIndexChanged(int)"), 
                                                                 self.checkSelectedLayer)
        self.connect(self.mFieldComboBoxTargetPointsId, SIGNAL("currentIndexChanged(int)"), 
                                                               self.checkSelectedLayer)
        self.connect(self.mFieldComboBoxTargetPointsName, SIGNAL("currentIndexChanged(int)"), 
                                                                 self.checkSelectedLayer)
        self.connect(self.pushButtonExit, SIGNAL("clicked()"), self.closeDialog)        
        self.connect(self.pushButtonStart, SIGNAL("clicked()"), self.calculateRoute)        
        self.connect(self.pushButtonStop, SIGNAL("clicked()"), self.stopWork)        

        self.settings = QSettings("openLand", "Raz")
        
        self.readSettings()
        self.checkSelectedEnable()

    def readSettings(self):
        self.maxLength = self.settings.value('route/maxLength', 1500)
        self.doubleSpinBox.setProperty("value", self.maxLength)
        
    def writeSettings(self):
        self.settings.setValue('route/maxLength', self.doubleSpinBox.value())
        
    def checkSelectedEnable(self):
        self.source_point_layer = self.mMapLayerComboBoxSourcePoints.currentLayer()
        self.target_point_layer = self.mMapLayerComboBoxTargetPoints.currentLayer()

        if self.source_point_layer is not None:
            self.mFieldComboBoxSourcePointsId.setLayer(self.source_point_layer)
            self.mFieldComboBoxSourcePointsName.setLayer(self.source_point_layer)
            self.spl_selection = self.source_point_layer.selectedFeatures()
            if len(self.spl_selection) > 0:
                self.checkBoxSelectedSoucePoints.setEnabled(True)
            else:
                self.checkBoxSelectedSoucePoints.setEnabled(False)
                self.checkBoxSelectedSoucePoints.setChecked(False)
        
        if self.target_point_layer is not None:
            self.mFieldComboBoxTargetPointsId.setLayer(self.target_point_layer)
            self.mFieldComboBoxTargetPointsName.setLayer(self.target_point_layer)
            self.tpl_selection = self.target_point_layer.selectedFeatures()
            if len(self.tpl_selection) > 0:
                self.checkBoxSelectedTargetPoints.setEnabled(True)
            else:
                self.checkBoxSelectedTargetPoints.setEnabled(False)
                self.checkBoxSelectedTargetPoints.setChecked(False)
        
        self.checkSelectedLayer()

    def checkSelectedLayer(self):
        if (self.mMapLayerComboBoxSourcePoints.currentLayer() is not None and
            self.mMapLayerComboBoxTargetPoints.currentLayer() is not None and
            self.mMapLayerComboBoxRoad.currentLayer() is not None and
            self.mMapLayerComboBoxCalculatedRoute.currentLayer() is not None and
            self.mMapLayerComboBoxManyLongPath.currentLayer() is not None):
            
            if (self.mMapLayerComboBoxRoad.currentLayer() != 
                self.mMapLayerComboBoxCalculatedRoute.currentLayer()):
                
                if not self.pushButtonStop.isEnabled():
                    self.checkSelectedField()

                else:
                    self.pushButtonStart.setEnabled(False)
            else:
                self.pushButtonStart.setEnabled(False)
        else:
            self.pushButtonStart.setEnabled(False)


    def checkSelectedField(self):
        if (self.mFieldComboBoxSourcePointsId.currentField() is not None and
            self.mFieldComboBoxSourcePointsName.currentField() is not None and
            self.mFieldComboBoxTargetPointsId.currentField() is not None and
            self.mFieldComboBoxTargetPointsName.currentField() is not None and
            self.mFieldComboBoxSourcePointsId.currentField() != '' and
            self.mFieldComboBoxSourcePointsName.currentField() != '' and
            self.mFieldComboBoxTargetPointsId.currentField() != '' and
            self.mFieldComboBoxTargetPointsName.currentField() != ''):
            
            if not self.pushButtonStop.isEnabled():
                self.pushButtonStart.setEnabled(True)
            else:
                self.pushButtonStart.setEnabled(False)
        else:
            self.pushButtonStart.setEnabled(False)

    def calculateRoute(self):
        self.writeSettings()
        
        worker = RouteWorker(self.iface)
        worker.sourcePointLayer = self.source_point_layer
        if self.checkBoxSelectedSoucePoints.isChecked():
            iter = self.spl_selection
        else:
            iter = self.source_point_layer.getFeatures()
        for every in iter:
            idf = every.attribute(self.mFieldComboBoxSourcePointsId.currentField())
            name = every.attribute(self.mFieldComboBoxSourcePointsName.currentField())
            geom = every.geometry()
            if geom.isMultipart():
                point = geom.asMultiPoint()[0]
            else:
                point = geom.asPoint()

            worker.sourcePoint.append([idf, name, point])

        worker.targetPointLayer = self.target_point_layer
        if self.checkBoxSelectedTargetPoints.isChecked():
            iter = self.tpl_selection
        else:
            iter = self.target_point_layer.getFeatures()

        for every in iter:
            idt = every.attribute(self.mFieldComboBoxTargetPointsId.currentField())
            name = every.attribute(self.mFieldComboBoxTargetPointsName.currentField())
            geom = every.geometry()
            if geom.isMultipart():
                point = geom.asMultiPoint()[0]
            else:
                point = geom.asPoint()
            worker.targetPoint.append([idt, name, point])
        
        worker.road = self.mMapLayerComboBoxRoad.currentLayer()
        worker.calculatedRoute = self.mMapLayerComboBoxCalculatedRoute.currentLayer()
        worker.manyLongPath = self.mMapLayerComboBoxManyLongPath.currentLayer()
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

        '''
        self.iface.messageBar().pushMessage('RaZ',
            u'Ошибка выполнения. Возможно, указаны неверные параметры слоёв.',
            self.iface.messageBar().ERROR)
        '''

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
        