# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ayab_dock_gui.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DockWidget(object):
    def setupUi(self, DockWidget):
        DockWidget.setObjectName("DockWidget")
        DockWidget.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        DockWidget.setWindowTitle("")
        self.dock_child = QtWidgets.QWidget()
        self.dock_child.setGeometry(QtCore.QRect(0, 0, 240, 581))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.dock_child.sizePolicy().hasHeightForWidth())
        self.dock_child.setSizePolicy(sizePolicy)
        self.dock_child.setMinimumSize(QtCore.QSize(240, 581))
        self.dock_child.setMaximumSize(QtCore.QSize(260, 581))
        self.dock_child.setObjectName("dock_child")
        self.ayab_config = QtWidgets.QWidget(self.dock_child)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.ayab_config.sizePolicy().hasHeightForWidth())
        self.ayab_config.setSizePolicy(sizePolicy)
        self.ayab_config.setObjectName("ayab_config")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.ayab_config)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.ayab_config)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QtCore.QSize(240, 0))
        self.groupBox.setMaximumSize(QtCore.QSize(240, 16777215))
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.serial_port_dropdown = QtWidgets.QComboBox(self.groupBox)
        self.serial_port_dropdown.setObjectName("serial_port_dropdown")
        self.horizontalLayout_3.addWidget(self.serial_port_dropdown)
        self.refresh_ports_button = QtWidgets.QPushButton(self.groupBox)
        self.refresh_ports_button.setObjectName("refresh_ports_button")
        self.horizontalLayout_3.addWidget(self.refresh_ports_button)
        self.verticalLayout.addWidget(self.groupBox)
        self.tab_widget = QtWidgets.QTabWidget(self.ayab_config)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.tab_widget.sizePolicy().hasHeightForWidth())
        self.tab_widget.setSizePolicy(sizePolicy)
        self.tab_widget.setMinimumSize(QtCore.QSize(220, 430))
        self.tab_widget.setMaximumSize(QtCore.QSize(1000000, 16777215))
        self.tab_widget.setDocumentMode(False)
        self.tab_widget.setTabBarAutoHide(False)
        self.tab_widget.setObjectName("tab_widget")
        self.verticalLayout.addWidget(self.tab_widget)
        DockWidget.setWidget(self.dock_child)

        self.retranslateUi(DockWidget)
        self.tab_widget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(DockWidget)

    def retranslateUi(self, DockWidget):
        _translate = QtCore.QCoreApplication.translate
        self.groupBox.setTitle(_translate("DockWidget", "Port Selection"))
        self.refresh_ports_button.setText(_translate("DockWidget", "Refresh"))
