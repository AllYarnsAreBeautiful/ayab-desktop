# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ayab_menu_gui.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MenuBar(object):
    def setupUi(self, menubar):
        menubar.setObjectName("menubar")
        menubar.setGeometry(QtCore.QRect(0, 0, 1008, 22))
        self.menu_file = QtWidgets.QMenu(menubar)
        self.menu_file.setObjectName("menu_file")
        self.menu_help = QtWidgets.QMenu(menubar)
        self.menu_help.setObjectName("menu_help")
        self.menu_tools = QtWidgets.QMenu(menubar)
        self.menu_tools.setObjectName("menu_tools")
        self.menu_preferences = QtWidgets.QMenu(menubar)
        self.menu_preferences.setObjectName("menu_preferences")
        self.menu_image_actions = QtWidgets.QMenu(menubar)
        self.menu_image_actions.setObjectName("menu_image_actions")
        self.action_image_actions = QtWidgets.QAction(menubar)
        self.action_image_actions.setObjectName("action_image_actions")
        self.action_load_AYAB_firmware = QtWidgets.QAction(menubar)
        self.action_load_AYAB_firmware.setObjectName(
            "action_load_AYAB_firmware")
        self.action_quit = QtWidgets.QAction(menubar)
        self.action_quit.setShortcut("Ctrl+Q")
        self.action_quit.setObjectName("action_quit")
        self.action_open_knitting_project = QtWidgets.QAction(menubar)
        self.action_open_knitting_project.setObjectName(
            "action_open_knitting_project")
        self.action_about = QtWidgets.QAction(menubar)
        self.action_about.setObjectName("action_about")
        self.action_help = QtWidgets.QAction(menubar)
        self.action_help.setObjectName("action_help")
        self.action_invert = QtWidgets.QAction(menubar)
        self.action_invert.setShortcut("Ctrl+I")
        self.action_invert.setObjectName("action_invert")
        self.action_stretch = QtWidgets.QAction(menubar)
        self.action_stretch.setShortcut("Ctrl+S")
        self.action_stretch.setObjectName("action_stretch")
        self.action_repeat = QtWidgets.QAction(menubar)
        self.action_repeat.setShortcut("Ctrl+R")
        self.action_repeat.setObjectName("action_repeat")
        self.action_reflect = QtWidgets.QAction(menubar)
        self.action_reflect.setShortcut("Ctrl+M")
        self.action_reflect.setObjectName("action_reflect")
        self.action_hflip = QtWidgets.QAction(menubar)
        self.action_hflip.setShortcut("Ctrl+Up")
        self.action_hflip.setObjectName("action_hflip")
        self.action_vflip = QtWidgets.QAction(menubar)
        self.action_vflip.setShortcut("Ctrl+Down")
        self.action_vflip.setObjectName("action_vflip")
        self.action_rotate_left = QtWidgets.QAction(menubar)
        self.action_rotate_left.setShortcut("Ctrl+Left")
        self.action_rotate_left.setObjectName("action_rotate_left")
        self.action_rotate_right = QtWidgets.QAction(menubar)
        self.action_rotate_right.setShortcut("Ctrl+Right")
        self.action_rotate_right.setObjectName("action_rotate_right")
        self.action_set_preferences = QtWidgets.QAction(menubar)
        self.action_set_preferences.setObjectName("action_set_preferences")
        self.menu_file.addAction(self.action_quit)
        self.menu_help.addAction(self.action_about)
        self.menu_tools.addAction(self.action_load_AYAB_firmware)
        self.menu_preferences.addAction(self.action_set_preferences)
        self.menu_image_actions.addAction(self.action_invert)
        self.menu_image_actions.addAction(self.action_stretch)
        self.menu_image_actions.addAction(self.action_repeat)
        self.menu_image_actions.addAction(self.action_reflect)
        self.menu_image_actions.addSeparator()
        self.menu_image_actions.addAction(self.action_hflip)
        self.menu_image_actions.addAction(self.action_vflip)
        self.menu_image_actions.addSeparator()
        self.menu_image_actions.addAction(self.action_rotate_left)
        self.menu_image_actions.addAction(self.action_rotate_right)
        self.menu_image_actions.addSeparator()
        menubar.addAction(self.menu_file.menuAction())

        self.retranslateUi(menubar)
        QtCore.QMetaObject.connectSlotsByName(menubar)

    def retranslateUi(self, menubar):
        _translate = QtCore.QCoreApplication.translate
        self.menu_file.setTitle(_translate("MenuBar", "File"))
        self.menu_help.setTitle(_translate("MenuBar", "Help"))
        self.menu_tools.setTitle(_translate("MenuBar", "Tools"))
        self.menu_preferences.setTitle(_translate("MenuBar", "Preferences"))
        self.menu_image_actions.setTitle(_translate("MenuBar",
                                                    "Image Actions"))
        self.action_load_AYAB_firmware.setText(
            _translate("MenuBar", "Load AYAB Firmware"))
        self.action_quit.setText(_translate("MenuBar", "Quit"))
        self.action_open_knitting_project.setText(
            _translate("MenuBar", "Open Knitting Project"))
        self.action_about.setText(_translate("MenuBar", "Help – About"))
        self.action_help.setText(_translate("MenuBar", "Help"))
        self.action_invert.setText(_translate("MenuBar", "Invert"))
        self.action_stretch.setText(_translate("MenuBar", "Stretch"))
        self.action_repeat.setText(_translate("MenuBar", "Repeat"))
        self.action_reflect.setText(_translate("MenuBar", "Reflect"))
        self.action_hflip.setText(_translate("MenuBar", "Horizontal Flip"))
        self.action_vflip.setText(_translate("MenuBar", "Vertical Flip"))
        self.action_rotate_left.setText(_translate("MenuBar", "Rotate Left"))
        self.action_rotate_right.setText(_translate("MenuBar", "Rotate Right"))
        self.action_set_preferences.setText(
            _translate("MenuBar", "Set Preferences"))
