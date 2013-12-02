lessThan(QT_MAJOR_VERSION, 5): error(This project requires Qt 5 or later)

# Needed for C++11 support.
CONFIG += c++11

TEMPLATE = app
TARGET = qmlc++
QT += qml quick widgets
QT += serialport
QT += testlib
HEADERS += \
    src/cayabcommunication.h \
    src/cayabbackend.h \
    src/cayabdataprocessing.h \
    src/cayabimageprocessing.h
SOURCES += src/main.cpp \
    src/cayabcommunication.cpp \
    src/cayabbackend.cpp \
    src/cayabdataprocessing.cpp \
    src/cayabimageprocessing.cpp
OTHER_FILES += qml/main.qml \
    qml/content/DebugTab.qml \
    qml/content/LeftLayout.qml \
    qml/content/DesignerTab.qml

RESOURCES += \
    resources.qrc
