# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ayab_gui.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, Ui_MainWindow):
        Ui_MainWindow.setObjectName("Ui_MainWindow")
        Ui_MainWindow.setGeometry(QtCore.QRect(0, 0, 1008, 900))
        self.central_widget = QtWidgets.QWidget(Ui_MainWindow)
        self.central_widget.setObjectName("central_widget")
        self.grid_layout = QtWidgets.QGridLayout(self.central_widget)
        self.grid_layout.setObjectName("grid_layout")
        self.image_side_panel = QtWidgets.QVBoxLayout()
        self.image_side_panel.setSpacing(6)
        self.image_side_panel.setObjectName("image_side_panel")
        self.graphics_splitter = QtWidgets.QSplitter(self.central_widget)
        self.graphics_splitter.setOrientation(QtCore.Qt.Vertical)
        self.graphics_splitter.setObjectName("graphics_splitter")
        self.image_pattern_view = QtWidgets.QGraphicsView(
            self.graphics_splitter)
        self.image_pattern_view.setGeometry(QtCore.QRect(0, 0, 700, 686))
        self.image_pattern_view.setObjectName("image_pattern_view")
        self.area = QtWidgets.QScrollArea(self.graphics_splitter)
        self.area.setGeometry(QtCore.QRect(0, 0, 700, 220))
        self.area.setObjectName("area")
        self.image_side_panel.addWidget(self.graphics_splitter)
        self.progress_layout = QtWidgets.QHBoxLayout()
        self.progress_layout.setSpacing(2)
        self.progress_layout.setObjectName("progress_layout")
        self.horizontal_layout = QtWidgets.QHBoxLayout()
        self.horizontal_layout.setObjectName("horizontal_layout")
        self.label_current_color = QtWidgets.QLabel(self.central_widget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        self.label_current_color.setFont(font)
        self.label_current_color.setText("")
        self.label_current_color.setObjectName("label_current_color")
        self.horizontal_layout.addWidget(
            self.label_current_color, 0,
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.progress_layout.addLayout(self.horizontal_layout)
        self.label_current_row = QtWidgets.QLabel(self.central_widget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_current_row.setFont(font)
        self.label_current_row.setText("")
        self.label_current_row.setObjectName("label_current_row")
        self.progress_layout.addWidget(
            self.label_current_row, 0,
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.image_side_panel.addLayout(self.progress_layout)
        self.label_notifications = QtWidgets.QLabel(self.central_widget)
        self.label_notifications.setText("")
        self.label_notifications.setAlignment(QtCore.Qt.AlignCenter)
        self.label_notifications.setObjectName("label_notifications")
        self.image_side_panel.addWidget(self.label_notifications)
        self.grid_layout.addLayout(self.image_side_panel, 0, 0, 3, 1)
        self.assistant_dock = QtWidgets.QScrollArea(self.central_widget)
        self.assistant_dock.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.assistant_dock.sizePolicy().hasHeightForWidth())
        self.assistant_dock.setSizePolicy(sizePolicy)
        self.assistant_dock.setMinimumSize(QtCore.QSize(280, 0))
        self.assistant_dock.setMaximumSize(QtCore.QSize(280, 16777215))
        self.assistant_dock.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.assistant_dock.setFrameShadow(QtWidgets.QFrame.Plain)
        self.assistant_dock.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.assistant_dock.setWidgetResizable(False)
        self.assistant_dock.setObjectName("assistant_dock")
        self.dockWidget_contents = QtWidgets.QWidget()
        self.dockWidget_contents.setGeometry(QtCore.QRect(0, 0, 500, 700))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.dockWidget_contents.sizePolicy().hasHeightForWidth())
        self.dockWidget_contents.setSizePolicy(sizePolicy)
        self.dockWidget_contents.setObjectName("dockWidget_contents")
        self.vertical_layout_5 = QtWidgets.QVBoxLayout(
            self.dockWidget_contents)
        self.vertical_layout_5.setSizeConstraint(
            QtWidgets.QLayout.SetFixedSize)
        self.vertical_layout_5.setObjectName("vertical_layout_5")
        self.widget_imgload = QtWidgets.QVBoxLayout()
        self.widget_imgload.setObjectName("widget_imgload")
        self.horizontal_layout1 = QtWidgets.QHBoxLayout()
        self.horizontal_layout1.setObjectName("horizontal_layout1")
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Minimum)
        self.horizontal_layout1.addItem(spacerItem)
        self.filename_lineedit = QtWidgets.QLineEdit(self.dockWidget_contents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.filename_lineedit.sizePolicy().hasHeightForWidth())
        self.filename_lineedit.setSizePolicy(sizePolicy)
        self.filename_lineedit.setText("")
        self.filename_lineedit.setObjectName("filename_lineedit")
        self.horizontal_layout1.addWidget(self.filename_lineedit)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20,
                                            QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontal_layout1.addItem(spacerItem1)
        self.widget_imgload.addLayout(self.horizontal_layout1)
        self.load_file_button = QtWidgets.QPushButton(self.dockWidget_contents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.load_file_button.sizePolicy().hasHeightForWidth())
        self.load_file_button.setSizePolicy(sizePolicy)
        self.load_file_button.setShortcut("Ctrl+O")
        self.load_file_button.setObjectName("load_file_button")
        self.widget_imgload.addWidget(self.load_file_button, 0,
                                      QtCore.Qt.AlignHCenter)
        self.vertical_layout_5.addLayout(self.widget_imgload)
        self.widget_optionsdock = QtWidgets.QWidget(self.dockWidget_contents)
        self.widget_optionsdock.setObjectName("widget_optionsdock")
        self.vertical_layout_2 = QtWidgets.QVBoxLayout(self.widget_optionsdock)
        self.vertical_layout_2.setSizeConstraint(
            QtWidgets.QLayout.SetMaximumSize)
        self.vertical_layout_2.setObjectName("vertical_layout_2")
        self.line = QtWidgets.QFrame(self.widget_optionsdock)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.vertical_layout_2.addWidget(self.line)
        self.knitting_options_dock = QtWidgets.QDockWidget(
            self.widget_optionsdock)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.knitting_options_dock.sizePolicy().hasHeightForWidth())
        self.knitting_options_dock.setSizePolicy(sizePolicy)
        self.knitting_options_dock.setObjectName("knitting_options_dock")
        self.dockWidget_contents_2 = QtWidgets.QWidget()
        self.dockWidget_contents_2.setObjectName("dockWidget_contents_2")
        self.knitting_options_dock.setWidget(self.dockWidget_contents_2)
        self.vertical_layout_2.addWidget(self.knitting_options_dock)
        self.vertical_layout_5.addWidget(self.widget_optionsdock, 0,
                                         QtCore.Qt.AlignHCenter)
        self.line_2 = QtWidgets.QFrame(self.dockWidget_contents)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.vertical_layout_5.addWidget(self.line_2)
        self.widget_knitcontrol = QtWidgets.QWidget(self.dockWidget_contents)
        self.widget_knitcontrol.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.widget_knitcontrol.sizePolicy().hasHeightForWidth())
        self.widget_knitcontrol.setSizePolicy(sizePolicy)
        self.widget_knitcontrol.setObjectName("widget_knitcontrol")
        self.vertical_layout_3 = QtWidgets.QVBoxLayout(self.widget_knitcontrol)
        self.vertical_layout_3.setSizeConstraint(
            QtWidgets.QLayout.SetMaximumSize)
        self.vertical_layout_3.setObjectName("vertical_layout_3")
        self.knit_button = QtWidgets.QPushButton(self.widget_knitcontrol)
        self.knit_button.setShortcut("Ctrl+Return")
        self.knit_button.setObjectName("knit_button")
        self.vertical_layout_3.addWidget(self.knit_button)
        self.cancel_button = QtWidgets.QPushButton(self.widget_knitcontrol)
        self.cancel_button.setShortcut("Esc")
        self.cancel_button.setObjectName("cancel_button")
        self.vertical_layout_3.addWidget(self.cancel_button)
        self.vertical_layout_5.addWidget(self.widget_knitcontrol, 0,
                                         QtCore.Qt.AlignHCenter)
        self.assistant_dock.setWidget(self.dockWidget_contents)
        self.grid_layout.addWidget(self.assistant_dock, 0, 1, 3, 1)
        Ui_MainWindow.setCentralWidget(self.central_widget)
        self.statusbar = QtWidgets.QStatusBar(Ui_MainWindow)
        self.statusbar.setObjectName("statusbar")
        Ui_MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(Ui_MainWindow)
        QtCore.QMetaObject.connectSlotsByName(Ui_MainWindow)

    def retranslateUi(self, Ui_MainWindow):
        _translate = QtCore.QCoreApplication.translate
        Ui_MainWindow.setWindowTitle(
            _translate("MainWindow", "All Yarns Are Beautiful"))
        self.assistant_dock.setWindowTitle(
            _translate("MainWindow", "Assistant"))
        self.load_file_button.setText(
            _translate("MainWindow", "1. Load Image File"))
        self.knitting_options_dock.setWindowTitle(
            _translate("MainWindow", "Knitting Options"))
        self.knit_button.setText(_translate("MainWindow", "2. Knit"))
        self.cancel_button.setText(_translate("MainWindow", "Cancel Knitting"))
