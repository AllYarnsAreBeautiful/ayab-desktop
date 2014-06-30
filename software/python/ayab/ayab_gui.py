# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ayab_gui.ui'
#
# Created by: PyQt4 UI code generator 4.10.3
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(739, 581)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.knitting_options_dock = QtGui.QDockWidget(Form)
        self.knitting_options_dock.setObjectName(_fromUtf8("knitting_options_dock"))
        self.dockWidgetContents_2 = QtGui.QWidget()
        self.dockWidgetContents_2.setObjectName(_fromUtf8("dockWidgetContents_2"))
        self.knitting_options_dock.setWidget(self.dockWidgetContents_2)
        self.gridLayout.addWidget(self.knitting_options_dock, 2, 1, 2, 1)
        self.progressBar = QtGui.QProgressBar(Form)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout.addWidget(self.progressBar, 4, 0, 1, 1)
        self.assistant_dock = QtGui.QDockWidget(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.assistant_dock.sizePolicy().hasHeightForWidth())
        self.assistant_dock.setSizePolicy(sizePolicy)
        self.assistant_dock.setMinimumSize(QtCore.QSize(500, 254))
        self.assistant_dock.setAcceptDrops(True)
        self.assistant_dock.setObjectName(_fromUtf8("assistant_dock"))
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.dockWidgetContents)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.widget = QtGui.QWidget(self.dockWidgetContents)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_3 = QtGui.QLabel(self.widget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout.addWidget(self.label_3)
        self.module_dropdown = QtGui.QComboBox(self.widget)
        self.module_dropdown.setObjectName(_fromUtf8("module_dropdown"))
        self.verticalLayout.addWidget(self.module_dropdown)
        spacerItem = QtGui.QSpacerItem(20, 5, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addWidget(self.widget)
        self.widget_4 = QtGui.QWidget(self.dockWidgetContents)
        self.widget_4.setObjectName(_fromUtf8("widget_4"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.widget_4)
        self.verticalLayout_4.setMargin(0)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.label_2 = QtGui.QLabel(self.widget_4)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_4.addWidget(self.label_2)
        self.load_file_button = QtGui.QPushButton(self.widget_4)
        self.load_file_button.setObjectName(_fromUtf8("load_file_button"))
        self.verticalLayout_4.addWidget(self.load_file_button)
        self.filename_lineedit = QtGui.QLineEdit(self.widget_4)
        self.filename_lineedit.setText(_fromUtf8(""))
        self.filename_lineedit.setObjectName(_fromUtf8("filename_lineedit"))
        self.verticalLayout_4.addWidget(self.filename_lineedit)
        spacerItem1 = QtGui.QSpacerItem(20, 5, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem1)
        self.horizontalLayout.addWidget(self.widget_4)
        self.widget_3 = QtGui.QWidget(self.dockWidgetContents)
        self.widget_3.setObjectName(_fromUtf8("widget_3"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.widget_3)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.label_4 = QtGui.QLabel(self.widget_3)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout_3.addWidget(self.label_4)
        self.knit_button = QtGui.QPushButton(self.widget_3)
        self.knit_button.setObjectName(_fromUtf8("knit_button"))
        self.verticalLayout_3.addWidget(self.knit_button)
        spacerItem2 = QtGui.QSpacerItem(20, 5, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem2)
        self.horizontalLayout.addWidget(self.widget_3)
        self.assistant_dock.setWidget(self.dockWidgetContents)
        self.gridLayout.addWidget(self.assistant_dock, 2, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.image_pattern_view = QtGui.QGraphicsView(Form)
        self.image_pattern_view.setObjectName(_fromUtf8("image_pattern_view"))
        self.horizontalLayout_2.addWidget(self.image_pattern_view)
        self.gridLayout.addLayout(self.horizontalLayout_2, 3, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "All Yarns Are Beautiful", None))
        self.knitting_options_dock.setWindowTitle(_translate("Form", "Knitting Options", None))
        self.assistant_dock.setWindowTitle(_translate("Form", "Asistant", None))
        self.label_3.setText(_translate("Form", "Select Module", None))
        self.label_2.setText(_translate("Form", "Load File", None))
        self.load_file_button.setText(_translate("Form", "Load File", None))
        self.label_4.setText(_translate("Form", "Control", None))
        self.knit_button.setText(_translate("Form", "Knit!", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

