#include <stdexcept>

#include <QApplication>
#include <QClipboard>
#include <QDebug>
#include <QQuickWindow>
#include <QVariant>

#include "cayabbackend.h"


// Constructor ///////////////////////////////////////////////////////////////
cAYABBackend::cAYABBackend(QObject *parent) :
    QObject(parent)
{
    AYABCommunication = new cAYABCommunication(this);
    AYABDataProcessing = new cAYABDataProcessing(this);
    AYABImageProcessing = new cAYABImageProcessing(this);
    connect(AYABDataProcessing, SIGNAL(sKnitDataCreated(QVector<QBitArray*>*,qint32,qint32,qint32)),
            AYABCommunication, SLOT(getKnitData(QVector<QBitArray*>*,qint32,qint32,qint32)));
}

// Destructor ////////////////////////////////////////////////////////////////

cAYABBackend::~cAYABBackend()
{
}

// get Communication Object //////////////////////////////////////////////////
cAYABCommunication* cAYABBackend::getAYABCommunication()
{
    return AYABCommunication;
}

void cAYABBackend::setWindow(QQuickWindow *window)
{
    // disconnect from previous window
    //if (mWindow != 0) mWindow->disconnect(this);

    mWindow = window;
    if (mWindow) {
        //mWindow->setIcon(QIcon(":/accessories-calculator.png"));

        // setup new connections
        connect(mWindow, SIGNAL(settingsTriggered()), this, SLOT(settingsDialog()));
        connect(mWindow, SIGNAL(settingsOKTriggered()), this, SLOT(slotSettingsBoxOKTriggered()));
        connect(mWindow, SIGNAL(newTriggered()), this, SLOT(newDialog()));
        connect(mWindow, SIGNAL(newOKTriggered()), this, SLOT(slotNewBoxOKTriggered()));
        connect(mWindow, SIGNAL(aboutTriggered()), this, SLOT(slotAboutTriggered()));
        connect(mWindow, SIGNAL(sendStartTriggered()), AYABCommunication, SLOT(sendStart()));
        connect(mWindow, SIGNAL(setPixelFromDesigner(int, int, bool)), AYABDataProcessing, SLOT(setPixel(qint32,qint32,bool)));
        connect(mWindow, SIGNAL(getVersionTriggered()),AYABCommunication, SLOT(getVersionData()));
        // set initial state
        //clearAll();
    }
}

void cAYABBackend::helpAbout()
{
    QMetaObject::invokeMethod(mWindow, "showAboutDialog");
}

void cAYABBackend::settingsDialog()
{
    if (mWindow) mWindow->setProperty("serialPortComboboxModel", AYABCommunication->getAvailablePorts());
    QMetaObject::invokeMethod(mWindow, "showSettingsDialog");
}

void cAYABBackend::slotSettingsBoxOKTriggered()
{
    if (mWindow) AYABCommunication->setSerialPort(mWindow->property("settingsSerialPortComboboxText").toString());
}

void cAYABBackend::slotAboutTriggered()
{
    if (mWindow) QMetaObject::invokeMethod(mWindow, "showAboutDialog");
}


void cAYABBackend::newDialog()
{
    //if (mWindow) mWindow->setProperty("serialPortComboboxModel", AYABCommunication->getAvailablePorts());
    QMetaObject::invokeMethod(mWindow, "showNewDialog");
}

void cAYABBackend::slotNewBoxOKTriggered()
{
    if (mWindow){
        AYABDataProcessing->setDataProperties(
                    mWindow->property("newStartNeedle").toInt(),
                    mWindow->property("newStopNeedle").toInt(),
                    mWindow->property("newNumberOfLines").toInt(),
                    QColor::fromRgb(255,255,255),
                    QColor::fromRgb(0,0,0),
                    mWindow->property("newProjectName").toString());
        mWindow->setProperty("designerStartNeedle", AYABDataProcessing->getStartNeedle());
        mWindow->setProperty("designerStopNeedle", AYABDataProcessing->getStopNeedle());
        mWindow->setProperty("designerNumberOfLines", AYABDataProcessing->getNumberOfLines());
        mWindow->setProperty("designerProjectName", AYABDataProcessing->getProjectName());
        mWindow->setProperty("debugTestImage", QVariant::fromValue(*AYABImageProcessing->getPreviewImage()));
    }
}

