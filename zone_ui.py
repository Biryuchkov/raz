# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\zone.ui'
#
# Created: Wed Mar 30 16:15:39 2016
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_DialogZone(object):
    def setupUi(self, DialogZone):
        DialogZone.setObjectName(_fromUtf8("DialogZone"))
        DialogZone.setWindowModality(QtCore.Qt.NonModal)
        DialogZone.resize(281, 287)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/zone.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        DialogZone.setWindowIcon(icon)
        DialogZone.setSizeGripEnabled(True)
        DialogZone.setModal(False)
        self.gridLayout_2 = QtGui.QGridLayout(DialogZone)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.formLayout_2 = QtGui.QFormLayout()
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.label_2 = QtGui.QLabel(DialogZone)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_2)
        self.mMapLayerComboBoxRoad = QgsMapLayerComboBox(DialogZone)
        self.mMapLayerComboBoxRoad.setObjectName(_fromUtf8("mMapLayerComboBoxRoad"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.mMapLayerComboBoxRoad)
        self.label_5 = QtGui.QLabel(DialogZone)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_5)
        self.doubleSpinBox = QtGui.QDoubleSpinBox(DialogZone)
        self.doubleSpinBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBox.setDecimals(3)
        self.doubleSpinBox.setMaximum(100000.0)
        self.doubleSpinBox.setObjectName(_fromUtf8("doubleSpinBox"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.doubleSpinBox)
        self.label_7 = QtGui.QLabel(DialogZone)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_7)
        self.mMapLayerComboBoxCalculatedZone = QgsMapLayerComboBox(DialogZone)
        self.mMapLayerComboBoxCalculatedZone.setObjectName(_fromUtf8("mMapLayerComboBoxCalculatedZone"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.mMapLayerComboBoxCalculatedZone)
        self.gridLayout_2.addLayout(self.formLayout_2, 1, 0, 1, 1)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pushButtonStop = QtGui.QPushButton(DialogZone)
        self.pushButtonStop.setEnabled(False)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/stop.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonStop.setIcon(icon1)
        self.pushButtonStop.setObjectName(_fromUtf8("pushButtonStop"))
        self.gridLayout.addWidget(self.pushButtonStop, 0, 1, 1, 1)
        self.pushButtonStart = QtGui.QPushButton(DialogZone)
        self.pushButtonStart.setEnabled(False)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/start.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonStart.setIcon(icon2)
        self.pushButtonStart.setObjectName(_fromUtf8("pushButtonStart"))
        self.gridLayout.addWidget(self.pushButtonStart, 0, 0, 1, 1)
        self.pushButtonExit = QtGui.QPushButton(DialogZone)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/exit.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonExit.setIcon(icon3)
        self.pushButtonExit.setObjectName(_fromUtf8("pushButtonExit"))
        self.gridLayout.addWidget(self.pushButtonExit, 0, 2, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 2, 0, 1, 1)
        self.progressBar = QtGui.QProgressBar(DialogZone)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout_2.addWidget(self.progressBar, 3, 0, 1, 1)
        self.groupBoxPoints = QtGui.QGroupBox(DialogZone)
        self.groupBoxPoints.setObjectName(_fromUtf8("groupBoxPoints"))
        self.gridLayout_5 = QtGui.QGridLayout(self.groupBoxPoints)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.checkBoxSelectedPoints = QtGui.QCheckBox(self.groupBoxPoints)
        self.checkBoxSelectedPoints.setEnabled(False)
        self.checkBoxSelectedPoints.setChecked(False)
        self.checkBoxSelectedPoints.setObjectName(_fromUtf8("checkBoxSelectedPoints"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.checkBoxSelectedPoints)
        self.label = QtGui.QLabel(self.groupBoxPoints)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label)
        self.mMapLayerComboBoxPoints = QgsMapLayerComboBox(self.groupBoxPoints)
        self.mMapLayerComboBoxPoints.setObjectName(_fromUtf8("mMapLayerComboBoxPoints"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.mMapLayerComboBoxPoints)
        self.label_3 = QtGui.QLabel(self.groupBoxPoints)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.mFieldComboBoxPointsId = QgsFieldComboBox(self.groupBoxPoints)
        self.mFieldComboBoxPointsId.setObjectName(_fromUtf8("mFieldComboBoxPointsId"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.mFieldComboBoxPointsId)
        self.label_8 = QtGui.QLabel(self.groupBoxPoints)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_8)
        self.mFieldComboBoxPointsName = QgsFieldComboBox(self.groupBoxPoints)
        self.mFieldComboBoxPointsName.setObjectName(_fromUtf8("mFieldComboBoxPointsName"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.mFieldComboBoxPointsName)
        self.gridLayout_5.addLayout(self.formLayout, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBoxPoints, 0, 0, 1, 1)

        self.retranslateUi(DialogZone)
        QtCore.QObject.connect(self.mMapLayerComboBoxPoints, QtCore.SIGNAL(_fromUtf8("layerChanged(QgsMapLayer*)")), self.mFieldComboBoxPointsId.setLayer)
        QtCore.QObject.connect(self.mMapLayerComboBoxPoints, QtCore.SIGNAL(_fromUtf8("layerChanged(QgsMapLayer*)")), self.mFieldComboBoxPointsName.setLayer)
        QtCore.QMetaObject.connectSlotsByName(DialogZone)
        DialogZone.setTabOrder(self.checkBoxSelectedPoints, self.mMapLayerComboBoxPoints)
        DialogZone.setTabOrder(self.mMapLayerComboBoxPoints, self.mFieldComboBoxPointsId)
        DialogZone.setTabOrder(self.mFieldComboBoxPointsId, self.mFieldComboBoxPointsName)
        DialogZone.setTabOrder(self.mFieldComboBoxPointsName, self.mMapLayerComboBoxRoad)
        DialogZone.setTabOrder(self.mMapLayerComboBoxRoad, self.doubleSpinBox)
        DialogZone.setTabOrder(self.doubleSpinBox, self.mMapLayerComboBoxCalculatedZone)
        DialogZone.setTabOrder(self.mMapLayerComboBoxCalculatedZone, self.pushButtonStart)
        DialogZone.setTabOrder(self.pushButtonStart, self.pushButtonStop)
        DialogZone.setTabOrder(self.pushButtonStop, self.pushButtonExit)

    def retranslateUi(self, DialogZone):
        DialogZone.setWindowTitle(_translate("DialogZone", "Zones calculation", None))
        self.label_2.setText(_translate("DialogZone", "Map layer road network", None))
        self.label_5.setText(_translate("DialogZone", "Maximum route length (kilometers)", None))
        self.label_7.setText(_translate("DialogZone", "Map layer for calculated zones", None))
        self.pushButtonStop.setText(_translate("DialogZone", "Stop", None))
        self.pushButtonStart.setText(_translate("DialogZone", "Run", None))
        self.pushButtonExit.setText(_translate("DialogZone", "Close", None))
        self.groupBoxPoints.setTitle(_translate("DialogZone", "The central point of the zones", None))
        self.checkBoxSelectedPoints.setText(_translate("DialogZone", "Only selected points", None))
        self.label.setText(_translate("DialogZone", "Map layer central points", None))
        self.label_3.setText(_translate("DialogZone", "ID field", None))
        self.label_8.setText(_translate("DialogZone", "Name field", None))

from qgsfieldcombobox import QgsFieldComboBox
from qgsmaplayercombobox import QgsMapLayerComboBox
import resources_rc
