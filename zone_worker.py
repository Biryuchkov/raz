# -*- coding: utf-8 -*-
import os
import uuid

from PyQt4 import QtCore
from PyQt4 import QtGui
from qgis.gui import *
from qgis.core import *
from qgis.networkanalysis import *
from datetime import *


class ZoneWorker(QtCore.QObject):

    progressChanged = QtCore.pyqtSignal(int)
    runned = QtCore.pyqtSignal(bool)
    error = QtCore.pyqtSignal(str)

    def __init__(self, iface):
        QtCore.QObject.__init__(self)
        self.iface = iface
        self.qgsMapCanvas = None
        self.sourcePointLayer = None
        self.sourcePoint = []
        self.road = None
        self.calculatedZone = None
        self.maxLength = None
        self.isContinueWork = True
                           
    def run(self):
        try:
            self.progressChanged.emit(0)
            self.runned.emit(True)
            QgsMessageLog.logMessage(
                self.tr('Process zones calculation started'),
                self.tr('RaZ zone'),
                QgsMessageLog.INFO)

            director = QgsLineVectorLayerDirector(self.road, -1, '', '', '', 3)
            properter = QgsDistanceArcProperter()
            director.addProperter(properter)
            try:
                mcrs = self.qgsMapCanvas.mapSettings().destinationCrs()
            except:
                mcrs = self.qgsMapCanvas.mapRenderer().destinationCrs()

            countAll = len(self.sourcePoint)

            lcrs = self.sourcePointLayer.dataProvider().crs()
            trf = QgsCoordinateTransform(lcrs, mcrs)
            trf_back = QgsCoordinateTransform(mcrs, lcrs)

            progressCounter = 0
            for every in self.sourcePoint:
                if not self.isContinueWork:
                    break
                
                id_point = every[0]
                name_point = every[1]
                list_zone = self.search_by_id_distance(id_point, 
                                                       self.calculatedZone, 
                                                       self.maxLength)
                if list_zone.__len__() == 0:
                    guid = str(uuid.uuid4())                                                                         
                    geom_from = QgsGeometry.fromPoint(QgsPoint(every[2][0], every[2][1]))
            
                    if mcrs <> lcrs:
                        geom_from.transform(trf)

                    pStart = geom_from.asPoint()
                    x_from = pStart.x()
                    y_from = pStart.y()

                    builder = QgsGraphBuilder(mcrs, True, 1)
                    tiedPoints = director.makeGraph(builder, [pStart])
                    graph = builder.graph()
                    tStart = tiedPoints[0]
                    idStart = graph.findVertex(tStart)
                    (tree, cost) = QgsGraphAnalyzer.dijkstra(graph, idStart, 0)
             
                    list_index = []
                    i = 0
                    while i < len(cost):
                        if cost[i] > (self.maxLength * 1000) and tree[i] != -1:
                            out_vertex_id = graph.arc(tree[i]).outVertex()
                            if cost[out_vertex_id] <= (self.maxLength *1000):
                                list_index.append(i)
                        i = i + 1
 
                    list_lines = []
                    for i in list_index:
                        p = [] 
                        curPos = graph.arc(tree[i]).outVertex()
                        while curPos != idStart:
                            p.append(graph.vertex(graph.arc(tree[curPos]).inVertex()).point())
                            curPos = graph.arc(tree[curPos]).outVertex()
                        list_lines.append(p)

                    g_zone = QgsGeometry().fromMultiPolyline(list_lines)
                    g_zone.transform(trf_back)    
                    g_convex = g_zone.convexHull()
            
                    f = QgsFeature()
                    f.initAttributes(len(self.calculatedZone.dataProvider().attributeIndexes()))
                    f.setGeometry(g_convex)                        
                    f.setAttribute(0, guid)
                    f.setAttribute(1, id_point)
                    f.setAttribute(2, name_point)
                    f.setAttribute(3, self.maxLength)

                    if self.calculatedZone.dataProvider().addFeatures([f])[0]:
                        self.calculatedZone.commitChanges()
                        QgsMessageLog.logMessage(
                            self.tr('Calculated zone around {} distance of {}')
                                    .format(name_point, self.maxLength),
                            self.tr('RaZ zone'),
                            QgsMessageLog.INFO)
                    else:
                        self.calculatedZone.rollBack()
                        QgsMessageLog.logMessage(
                            self.tr('Error saving zone around {} distance of {}')
                                    .format(name_point, self.maxLength),
                            self.tr('RaZ zone'),
                            QgsMessageLog.CRITICAL)
                else:
                    for eve in list_zone:
                        if (eve['id'] == id_point) and (eve['path'] == self.maxLength):
                            QgsMessageLog.logMessage(
                                self.tr('Zone around {} distance of {} has been calculated previously')
                                        .format(name_point, self.maxLength),
                                self.tr('RaZ zone'),
                                QgsMessageLog.INFO)

                progressCounter += 1
                self.progressChanged.emit(progressCounter * 100 / countAll)

            if self.isContinueWork:
                self.progressChanged.emit(100)
                QgsMessageLog.logMessage(
                    self.tr('Process zones calculation finished'),
                    self.tr('RaZ zone'),
                    QgsMessageLog.INFO)

            else:
                QgsMessageLog.logMessage(
                    self.tr('Process zones calculation stopped by the user'),
                    self.tr('RaZ zone'),
                    QgsMessageLog.WARNING)

        except:
            import traceback
            QgsMessageLog.logMessage(traceback.format_exc(),
                self.tr('RaZ zone'),
                QgsMessageLog.CRITICAL)
            self.runned.emit(False)
        else:
            self.runned.emit(False)

    def search_by_id_distance(self, id_from, l, distance):
        list_a = []

        p = l.dataProvider()
        search_value = u'id={} AND path={}'.format(id_from, 
                                                         distance)
        l.setSubsetString(search_value)
        request = QgsFeatureRequest()

        for feat in p.getFeatures(request):
            one_path = {}
            one_path['id'] = feat.attribute('id')
            one_path['path'] = feat.attribute('path')
            
            list_a.append(one_path)

        l.setSubsetString('')
        return list_a
