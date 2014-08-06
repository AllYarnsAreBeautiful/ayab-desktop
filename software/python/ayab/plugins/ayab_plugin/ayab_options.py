# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ayab_options.ui'
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

class Ui_DockWidget(object):
    def setupUi(self, DockWidget):
        DockWidget.setObjectName(_fromUtf8("DockWidget"))
        DockWidget.resize(237, 551)
        DockWidget.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)
        self.ayab_config = QtGui.QWidget()
        self.ayab_config.setObjectName(_fromUtf8("ayab_config"))
        self.verticalLayout = QtGui.QVBoxLayout(self.ayab_config)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(self.ayab_config)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.serial_port_dropdown = QtGui.QComboBox(self.groupBox)
        self.serial_port_dropdown.setObjectName(_fromUtf8("serial_port_dropdown"))
        self.horizontalLayout_3.addWidget(self.serial_port_dropdown)
        self.refresh_ports_button = QtGui.QPushButton(self.groupBox)
        self.refresh_ports_button.setObjectName(_fromUtf8("refresh_ports_button"))
        self.horizontalLayout_3.addWidget(self.refresh_ports_button)
        self.verticalLayout.addWidget(self.groupBox)
        self.label_6 = QtGui.QLabel(self.ayab_config)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.verticalLayout.addWidget(self.label_6)
        self.color_edit = QtGui.QSpinBox(self.ayab_config)
        self.color_edit.setMinimum(2)
        self.color_edit.setMaximum(6)
        self.color_edit.setObjectName(_fromUtf8("color_edit"))
        self.verticalLayout.addWidget(self.color_edit)
        self.label_5 = QtGui.QLabel(self.ayab_config)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.verticalLayout.addWidget(self.label_5)
        self.start_line_edit = QtGui.QSpinBox(self.ayab_config)
        self.start_line_edit.setSuffix(_fromUtf8(""))
        self.start_line_edit.setMinimum(0)
        self.start_line_edit.setMaximum(256)
        self.start_line_edit.setObjectName(_fromUtf8("start_line_edit"))
        self.verticalLayout.addWidget(self.start_line_edit)
        self.line = QtGui.QFrame(self.ayab_config)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.label = QtGui.QLabel(self.ayab_config)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.start_needle_edit = QtGui.QSpinBox(self.ayab_config)
        self.start_needle_edit.setMaximum(200)
        self.start_needle_edit.setObjectName(_fromUtf8("start_needle_edit"))
        self.verticalLayout.addWidget(self.start_needle_edit)
        self.label_2 = QtGui.QLabel(self.ayab_config)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.stop_needle_edit = QtGui.QSpinBox(self.ayab_config)
        self.stop_needle_edit.setSuffix(_fromUtf8(""))
        self.stop_needle_edit.setMaximum(200)
        self.stop_needle_edit.setObjectName(_fromUtf8("stop_needle_edit"))
        self.verticalLayout.addWidget(self.stop_needle_edit)
        self.label_3 = QtGui.QLabel(self.ayab_config)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout.addWidget(self.label_3)
        self.alignment_combo_box = QtGui.QComboBox(self.ayab_config)
        self.alignment_combo_box.setObjectName(_fromUtf8("alignment_combo_box"))
        self.alignment_combo_box.addItem(_fromUtf8(""))
        self.alignment_combo_box.addItem(_fromUtf8(""))
        self.alignment_combo_box.addItem(_fromUtf8(""))
        self.verticalLayout.addWidget(self.alignment_combo_box)
        self.label_4 = QtGui.QLabel(self.ayab_config)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout.addWidget(self.label_4)
        self.machine_type_box = QtGui.QComboBox(self.ayab_config)
        self.machine_type_box.setObjectName(_fromUtf8("machine_type_box"))
        self.machine_type_box.addItem(_fromUtf8(""))
        self.machine_type_box.addItem(_fromUtf8(""))
        self.verticalLayout.addWidget(self.machine_type_box)
        self.configure_button = QtGui.QPushButton(self.ayab_config)
        self.configure_button.setObjectName(_fromUtf8("configure_button"))
        self.verticalLayout.addWidget(self.configure_button)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        DockWidget.setWidget(self.ayab_config)

        self.retranslateUi(DockWidget)
        QtCore.QMetaObject.connectSlotsByName(DockWidget)

    def retranslateUi(self, DockWidget):
        DockWidget.setWindowTitle(_translate("DockWidget", "AYAB", None))
        self.groupBox.setTitle(_translate("DockWidget", "Port Selection", None))
        self.refresh_ports_button.setText(_translate("DockWidget", "Refresh Ports", None))
        self.label_6.setText(_translate("DockWidget", "Colors", None))
        self.label_5.setText(_translate("DockWidget", "Start Line", None))
        self.start_line_edit.setPrefix(_translate("DockWidget", "line ", None))
        self.label.setText(_translate("DockWidget", "Start Needle", None))
        self.start_needle_edit.setPrefix(_translate("DockWidget", "needle ", None))
        self.label_2.setText(_translate("DockWidget", "Stop Needle", None))
        self.stop_needle_edit.setPrefix(_translate("DockWidget", "needle ", None))
        self.label_3.setText(_translate("DockWidget", "Alignment", None))
        self.alignment_combo_box.setItemText(0, _translate("DockWidget", "left", None))
        self.alignment_combo_box.setItemText(1, _translate("DockWidget", "center", None))
        self.alignment_combo_box.setItemText(2, _translate("DockWidget", "right", None))
        self.label_4.setText(_translate("DockWidget", "Machine Type", None))
        self.machine_type_box.setItemText(0, _translate("DockWidget", "single", None))
        self.machine_type_box.setItemText(1, _translate("DockWidget", "double", None))
        self.configure_button.setText(_translate("DockWidget", "Configure", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    DockWidget = QtGui.QDockWidget()
    ui = Ui_DockWidget()
    ui.setupUi(DockWidget)
    DockWidget.show()
    sys.exit(app.exec_())

