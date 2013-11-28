#include <QQuickWindow>

#include "cayabcommunication.h"

// Constructor ///////////////////////////////////////////////////////////////

cAYABCommunication::cAYABCommunication(QObject *parent) :
    QObject(parent)
{
    mSerialPortName = "ttyUSB0";

    mSerialPort = new QSerialPort(mSerialPortName, this);
    connect(mSerialPort,SIGNAL(readyRead()),this,SLOT(processData()));
    connect(this,SIGNAL(sLineRequest(quint8)),this,SLOT(sendLine(quint8)));
}

// Destructor ////////////////////////////////////////////////////////////////

cAYABCommunication::~cAYABCommunication()
{

}

// set Serial Port ///////////////////////////////////////////////////////////

void cAYABCommunication::setSerialPort(QString port)
{
    mSerialPortName = port;
    mSerialPort->setPortName(port);
    mSerialPort->setBaudRate(115200);
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
// process serial receive Data //////////////////////////////////////////////////////

void cAYABCommunication::processData()
{
    char message[2];
    mSerialPort->read(message, 2);
    quint8 messageID = message[0];
    quint8 messagePayload = message[1];
    switch( messageID )
    {
    case 0xC1:
        // Init Request Answer
        qDebug("Init Request Answer");
        emit sInitRequestAnswer(messagePayload);
        break;
    case 0xC2:
        // Start Request Answer
        qDebug("Start Request Answer");
        emit sStartRequestAnswer(messagePayload);
        break;
    case 0x83:
        // Line Request
        qDebug("Line Request");
        emit sLineRequest(messagePayload);
        break;
    case 0xC4:
        // Stop Request Answer
        qDebug("Stop Request Answer");
        emit sStopRequestAnswer(messagePayload);
        break;
    case 0xC5:
        // Info Request Answer
        qDebug("Info Request Answer");
        emit sInfoRequestAnswer(messagePayload);
        break;
    default:
        break;
    }
}

// send Line to Hardware //////////////////////////////////////////////////////

void cAYABCommunication::sendLine(quint8 lineNumber)
{
    //toDo

}
