# -*- coding: utf-8 -*-
import os
import uuid
import traceback

from PyQt4 import QtCore
from PyQt4 import QtGui
from qgis.gui import *
from qgis.core import *
from qgis.networkanalysis import *
from datetime import *


class RouteWorker(QtCore.QObject):

    progressChanged = QtCore.pyqtSignal(int)
    runned = QtCore.pyqtSignal(bool)
    error = QtCore.pyqtSignal(str)

    def __init__(self, iface):
        QtCore.QObject.__init__(self)
        self.iface = iface
        self.qgsMapCanvas = None
        self.sourcePointLayer = None
        self.sourcePoint = []
        self.targetPointLayer = None
        self.targetPoint = []
        self.road = None
        self.calculatedRoute = None
        self.manyLongPath = None
        self.maxLength = None
        self.isContinueWork = True
        self.error = QtCore.pyqtSignal(Exception, basestring)
               
    def run(self):
        try:
            self.progressChanged.emit(0)
            self.runned.emit(True)
        
            QgsMessageLog.logMessage(
                self.tr('Process routes calculation started'),
                self.tr('RaZ route'),
                QgsMessageLog.INFO)

            director = QgsLineVectorLayerDirector(self.road, -1, '', '', '', 3)
            properter = QgsDistanceArcProperter()
            director.addProperter(properter)
            try:
                mcrs = self.qgsMapCanvas.mapSettings().destinationCrs()
            except:
                mcrs = self.qgsMapCanvas.mapRenderer().destinationCrs()

            measure = QgsDistanceArea()
            measure.setEllipsoid('WGS84')
            measure.setEllipsoidalMode(True)
            measure.setSourceCrs(3857)

            countFrom = len(self.sourcePoint)
            countTo = len(self.targetPoint)
            countAll = countFrom * countTo

            lcrs = self.sourcePointLayer.dataProvider().crs()
            trf = QgsCoordinateTransform(lcrs, mcrs)
            trf_back = QgsCoordinateTransform(mcrs, lcrs)
        
            progressCounter = 0
            for every in self.sourcePoint:
                if not self.isContinueWork:
                    break

                id_from = every[0]
                name_from = every[1]
                geom_from = QgsGeometry.fromPoint(QgsPoint(every[2][0], every[2][1]))
                if mcrs <> lcrs:
                    geom_from.transform(trf)

                pStart = geom_from.asPoint()
                x_from = pStart.x()
                y_from = pStart.y()

                for ever in self.targetPoint:
                    if not self.isContinueWork:
                        break

                    id_to = ever[0]
                    name_to = ever[1]

                    list_long = self.search_by_id(id_from, id_to, self.manyLongPath, False, True)
                    if len(list_long) > 0:
                        QgsMessageLog.logMessage(
                            self.tr('Route from {} to {} ignored previously')
                                    .format(name_from, name_to),
                            self.tr('RaZ route'),
                            QgsMessageLog.INFO)
                        continue
            
                    geom_to = QgsGeometry.fromPoint(QgsPoint(ever[2][0], ever[2][1]))
                    if mcrs <> lcrs:
                        geom_to.transform(trf)
            
                    pStop = geom_to.asPoint()
                    x_to = pStop.x()
                    y_to = pStop.y()

                    if (x_from <> x_to) and (y_from <> y_to):
                        list_path = self.search_by_id(id_from, id_to, self.calculatedRoute, True)
                
                        if list_path.__len__() == 0:
                            builder = QgsGraphBuilder(mcrs, True, 1)
                            tiedPoints = director.makeGraph(builder, [pStart, pStop])
                            graph = builder.graph()
 
                            tStart = tiedPoints[0]
                            tStop = tiedPoints[1]
 
                            idStart = graph.findVertex(tStart)
                            idStop = graph.findVertex(tStop)
 
                            (tree, cost) = QgsGraphAnalyzer.dijkstra(graph, idStart, 0)
             
                            if tree[ idStop ] == -1:
                                QgsMessageLog.logMessage(
                                    self.tr('Route from {} to {} NOT found')
                                            .format(name_from, name_to),
                                    self.tr('RaZ route'),
                                    QgsMessageLog.WARNING)
                            else:
                                p = [] 
                                curPos = idStop
                                while curPos != idStart:
                                    p.append(graph.vertex(graph.arc(tree[curPos]).inVertex()).point())
                                    curPos = graph.arc(tree[curPos]).outVertex();
 
                                p.append(tStart)
 
                                g_line = QgsGeometry.fromPolyline(p)
                                l_line = measure.measureLength(g_line) / 1000
                                if l_line > self.maxLength:
                                    QgsMessageLog.logMessage(
                                        self.tr('Route from {} to {} = {} more maximum {}')
                                                .format(name_from, name_to, l_line, self.maxLength),
                                        self.tr('RaZ route'),
                                        QgsMessageLog.INFO)

                                    list_f = []

                                    guid = str(uuid.uuid4())                                                                         
                                    f = QgsFeature()
                                    f.initAttributes(len(self.manyLongPath.dataProvider().attributeIndexes()))
                                    f.setAttribute(0, guid)
                                    f.setAttribute(1, id_from)
                                    f.setAttribute(2, id_to)
                                    f.setAttribute(3, l_line)
                                    list_f.append(f)

                                    guid = str(uuid.uuid4())                                                                         
                                    f = QgsFeature()
                                    f.initAttributes(len(self.manyLongPath.dataProvider().attributeIndexes()))
                                    f.setAttribute(0, guid)
                                    f.setAttribute(1, id_to)
                                    f.setAttribute(2, id_from)
                                    f.setAttribute(3, l_line)
                                    list_f.append(f)

                                    if self.manyLongPath.dataProvider().addFeatures(list_f)[0]:
                                        self.manyLongPath.commitChanges()
                                    else:
                                        self.manyLongPath.rollBack()
                                        QgsMessageLog.logMessage(
                                            self.tr('Error saving route from {} to {}')
                                                    .format(name_from, name_to),
                                            self.tr('RaZ route'),
                                            QgsMessageLog.CRITICAL)
                                else:
                                    g_line.transform(trf_back)
                                    guid = str(uuid.uuid4())                                                                         

                                    QgsMessageLog.logMessage(
                                        self.tr('Route from {} to {} = {}')
                                                .format(name_from, name_to, l_line),
                                        self.tr('RaZ route'),
                                        QgsMessageLog.INFO)

                                    f = QgsFeature()
                                    f.initAttributes(len(self.calculatedRoute.dataProvider().attributeIndexes()))
                                    f.setGeometry(g_line)                        
                                    f.setAttribute(0, guid)
                                    f.setAttribute(1, name_from)
                                    f.setAttribute(2, name_to)
                                    f.setAttribute(3, l_line)
                                    f.setAttribute(4, id_from)
                                    f.setAttribute(5, id_to)

                                    if self.calculatedRoute.dataProvider().addFeatures([f])[0]:
                                        self.calculatedRoute.commitChanges()
                                    else:
                                        self.calculatedRoute.rollBack()
                                        QgsMessageLog.logMessage(
                                            self.tr('Error saving route from {} to {}')
                                                    .format(name_from, name_to),
                                            self.tr('RaZ route'),
                                            QgsMessageLog.CRITICAL)

                        else:
                            for eve in list_path:
                                if (eve['idfrom'] == id_from) and (eve['idto'] == id_to):
                                    QgsMessageLog.logMessage(
                                        self.tr('Route from {} to {} has been calculated previously')
                                                .format(name_from, name_to),
                                        self.tr('RaZ route'),
                                        QgsMessageLog.INFO)

                                    is_create_object = False
                                    break
                                elif (eve['idfrom'] == id_to) and (eve['idto'] == id_from):
                            
                                    if eve['is_multi']:
                                        g_line = QgsGeometry().fromMultiPolyline(eve['geom'])
                                    else:
                                        g_line = QgsGeometry().fromPolyline(eve['geom'])
                                    guid = str(uuid.uuid4())                                                                         
                                    l_line = eve['path']

                                    f = QgsFeature()
                                    f.initAttributes(len(self.calculatedRoute.dataProvider().attributeIndexes()))
                                    f.setGeometry(g_line)                        
                                    f.setAttribute(0, guid)
                                    f.setAttribute(1, name_from)
                                    f.setAttribute(2, name_to)
                                    f.setAttribute(3, l_line)
                                    f.setAttribute(4, id_from)
                                    f.setAttribute(5, id_to)

                                    is_create_object = True
                            
                                else:
                                    QgsMessageLog.logMessage(
                                        self.tr('An error occurred while processing identity {} - {}')
                                                .format(id_to, id_from),
                                        self.tr('RaZ route'),
                                        QgsMessageLog.CRITICAL)

                                    is_create_object = False

                            if is_create_object:
                                QgsMessageLog.logMessage(
                                    self.tr('Route from {} to {} is defined by the return, calculated previously')
                                            .format(name_from, name_to),
                                    self.tr('RaZ route'),
                                    QgsMessageLog.INFO)

                                if self.calculatedRoute.dataProvider().addFeatures([f])[0]:
                                    self.calculatedRoute.commitChanges()
                                else:
                                    self.calculatedRoute.rollBack()
                                    QgsMessageLog.logMessage(
                                        self.tr('Error saving route from {} to {}')
                                                .format(name_from, name_to),
                                        self.tr('RaZ route'),
                                        QgsMessageLog.CRITICAL)

                    progressCounter += 1
                    self.progressChanged.emit(progressCounter * 100 / countAll)

            if self.isContinueWork:
                self.progressChanged.emit(100)
                QgsMessageLog.logMessage(
                    self.tr('Process routes calculation finished'),
                    self.tr('RaZ route'),
                    QgsMessageLog.INFO)

            else:
                QgsMessageLog.logMessage(
                    self.tr('Process routes calculation stopped by the user'),
                    self.tr('RaZ route'),
                    QgsMessageLog.WARNING)
        
        except:
            import traceback
            QgsMessageLog.logMessage(traceback.format_exc(),
                self.tr('RaZ route'),
                QgsMessageLog.CRITICAL)
            self.runned.emit(False)
        else:
            self.runned.emit(False)

    def search_by_id(self, id_from, id_to, l, isgeo, ismax=False):
        list_a = []

        p = l.dataProvider()
        if ismax:
            search_value = u'(((idfrom={} AND idto={}) OR (idfrom={} AND idto={})) AND path > {})'.format(id_from, 
                                                                                                          id_to, 
                                                                                                          id_to, 
                                                                                                          id_from, 
                                                                                                          self.maxLength)
        else:
            search_value = u'((idfrom={} AND idto={}) OR (idfrom={} AND idto={}))'.format(id_from, 
                                                                                          id_to, 
                                                                                          id_to, 
                                                                                          id_from)
        l.setSubsetString(search_value)
        request = QgsFeatureRequest()

        for feat in p.getFeatures(request):
            one_path = {}
            one_path['idfrom'] = feat.attribute('idfrom')
            one_path['idto'] = feat.attribute('idto')
            one_path['path'] = feat.attribute('path')
            if isgeo:
                if feat.geometry().isMultipart():
                    one_path['geom'] = feat.geometry().asMultiPolyline()
                    one_path['is_multi'] = True
                else:
                    one_path['geom'] = feat.geometry().asPolyline()
                    one_path['is_multi'] = False
            
            list_a.append(one_path)

        l.setSubsetString('')
        return list_a

