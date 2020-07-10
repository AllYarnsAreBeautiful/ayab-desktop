# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ayab_status_gui.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_StatusWidget(object):
    def setupUi(self, status_tab):
        status_tab.setObjectName("status_tab")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(status_tab)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(0, -1, 211, 333))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(
            self.verticalLayoutWidget_2)
        self.verticalLayout_4.setContentsMargins(6, 16, 12, 6)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_8 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_4.addWidget(self.label_8, 0,
                                        QtCore.Qt.AlignHCenter)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.progress_hall_l = QtWidgets.QProgressBar(
            self.verticalLayoutWidget_2)
        self.progress_hall_l.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.progress_hall_l.sizePolicy().hasHeightForWidth())
        self.progress_hall_l.setSizePolicy(sizePolicy)
        self.progress_hall_l.setMaximum(1024)
        self.progress_hall_l.setProperty("value", 0)
        self.progress_hall_l.setAlignment(QtCore.Qt.AlignCenter)
        self.progress_hall_l.setOrientation(QtCore.Qt.Vertical)
        self.progress_hall_l.setObjectName("progress_hall_l")
        self.verticalLayout_6.addWidget(self.progress_hall_l, 0,
                                        QtCore.Qt.AlignHCenter)
        self.label_hall_l = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_hall_l.sizePolicy().hasHeightForWidth())
        self.label_hall_l.setSizePolicy(sizePolicy)
        self.label_hall_l.setAlignment(QtCore.Qt.AlignCenter)
        self.label_hall_l.setObjectName("label_hall_l")
        self.verticalLayout_6.addWidget(self.label_hall_l)
        self.horizontalLayout.addLayout(self.verticalLayout_6)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.progress_hall_r = QtWidgets.QProgressBar(
            self.verticalLayoutWidget_2)
        self.progress_hall_r.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.progress_hall_r.sizePolicy().hasHeightForWidth())
        self.progress_hall_r.setSizePolicy(sizePolicy)
        self.progress_hall_r.setMaximum(1024)
        self.progress_hall_r.setProperty("value", 0)
        self.progress_hall_r.setAlignment(QtCore.Qt.AlignCenter)
        self.progress_hall_r.setOrientation(QtCore.Qt.Vertical)
        self.progress_hall_r.setObjectName("progress_hall_r")
        self.verticalLayout_7.addWidget(self.progress_hall_r, 0,
                                        QtCore.Qt.AlignHCenter)
        self.label_hall_r = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_hall_r.sizePolicy().hasHeightForWidth())
        self.label_hall_r.setSizePolicy(sizePolicy)
        self.label_hall_r.setAlignment(QtCore.Qt.AlignCenter)
        self.label_hall_r.setObjectName("label_hall_r")
        self.verticalLayout_7.addWidget(self.label_hall_r)
        self.horizontalLayout.addLayout(self.verticalLayout_7)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.line_2 = QtWidgets.QFrame(self.verticalLayoutWidget_2)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_4.addWidget(self.line_2)
        self.label_7 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_4.addWidget(self.label_7, 0,
                                        QtCore.Qt.AlignHCenter)
        self.label_carriage = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_carriage.sizePolicy().hasHeightForWidth())
        self.label_carriage.setSizePolicy(sizePolicy)
        self.label_carriage.setObjectName("label_carriage")
        self.verticalLayout_4.addWidget(self.label_carriage, 0,
                                        QtCore.Qt.AlignHCenter)
        self.slider_position = QtWidgets.QSlider(self.verticalLayoutWidget_2)
        self.slider_position.setEnabled(False)
        self.slider_position.setMaximum(199)
        self.slider_position.setOrientation(QtCore.Qt.Horizontal)
        self.slider_position.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.slider_position.setObjectName("slider_position")
        self.verticalLayout_4.addWidget(self.slider_position)
        self.label_direction = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_direction.sizePolicy().hasHeightForWidth())
        self.label_direction.setSizePolicy(sizePolicy)
        self.label_direction.setAlignment(QtCore.Qt.AlignCenter)
        self.label_direction.setObjectName("label_direction")
        self.verticalLayout_4.addWidget(self.label_direction, 0,
                                        QtCore.Qt.AlignHCenter)
        self.line_3 = QtWidgets.QFrame(self.verticalLayoutWidget_2)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout_4.addWidget(self.line_3)
        self.label_9 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_4.addWidget(self.label_9, 0,
                                        QtCore.Qt.AlignHCenter)
        self.label_progress = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Sans")
        font.setPointSize(22)
        self.label_progress.setFont(font)
        self.label_progress.setMouseTracking(False)
        self.label_progress.setObjectName("label_progress")
        self.verticalLayout_4.addWidget(self.label_progress, 0,
                                        QtCore.Qt.AlignHCenter)

        self.retranslateUi(status_tab)
        QtCore.QMetaObject.connectSlotsByName(status_tab)

    def retranslateUi(self, status_tab):
        _translate = QtCore.QCoreApplication.translate
        self.label_8.setText(_translate("StatusWidget", "Hall Sensors"))
        self.progress_hall_l.setFormat(_translate("StatusWidget", "%p%"))
        self.label_hall_l.setText(_translate("StatusWidget", "Hall Left"))
        self.progress_hall_r.setFormat(_translate("StatusWidget", "%p%"))
        self.label_hall_r.setText(_translate("StatusWidget", "Hall Right"))
        self.label_7.setText(_translate("StatusWidget", "Carriage"))
        self.label_carriage.setText(
            _translate("StatusWidget", "No carriage detected"))
        self.label_direction.setText(_translate("StatusWidget", "direction"))
        self.label_9.setText(_translate("StatusWidget", "Progress"))
        self.label_progress.setText(_translate("StatusWidget", "progress"))
