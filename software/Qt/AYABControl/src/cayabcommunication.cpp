#include <QQuickWindow>

#include "cayabcommunication.h"

// Constructor ///////////////////////////////////////////////////////////////

cAYABCommunication::cAYABCommunication(QObject *parent) :
    QObject(parent)
{
    mSerialPortName = "ttyUSB0";

    mSerialPort = new QSerialPort(mSerialPortName, this);
}

// Destructor ////////////////////////////////////////////////////////////////

cAYABCommunication::~cAYABCommunication()
{
}

// set Window ////////////////////////////////////////////////////////////////

void cAYABCommunication::setWindow(QQuickWindow *window)
{
    // disconnect from previous window
    //if (mWindow != 0) mWindow->disconnect(this);

    mWindow = window;

    if (mWindow) {
        //mWindow->setIcon(QIcon(":/accessories-calculator.png"));

        // setup new connections
        //connect(mWindow, SIGNAL(aboutTriggered()), this, SLOT(getAvailablePorts()));
        //connect(mWindow, SIGNAL(keyClicked(int)), this, SLOT(keyClicked(int)));
        //connect(mWindow, SIGNAL(cutTriggered()), this, SLOT(editCut()));
        //connect(mWindow, SIGNAL(copyTriggered()), this, SLOT(editCopy()));
        //connect(mWindow, SIGNAL(pasteTriggered()), this, SLOT(editPaste()));
        //connect(mWindow, SIGNAL(cutTriggered()), this, SLOT(getAvailablePorts()));
        //connect(mWindow, SIGNAL(aboutTriggered()), this, SLOT(getAvailablePorts()));
        // set initial state
        //clearAll();
    }
}

// set Serial Port ///////////////////////////////////////////////////////////

void cAYABCommunication::setSerialPort(QString port)
{
    mSerialPortName = port;
    mSerialPort->setPortName(port);
}


// get Serial Port ///////////////////////////////////////////////////////////

QString cAYABCommunication::getSerialPort()
{
    return mSerialPortName;
}

// list available Ports //////////////////////////////////////////////////////

QStringList cAYABCommunication::getAvailablePorts()
{
    QStringList ports;
    foreach (const QSerialPortInfo &info, QSerialPortInfo::availablePorts()) {
        ports << info.portName();
    }
    return ports;
}
