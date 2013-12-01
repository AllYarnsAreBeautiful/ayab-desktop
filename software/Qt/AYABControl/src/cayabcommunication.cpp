#include <QQuickWindow>

#include "cayabcommunication.h"

// Constructor ///////////////////////////////////////////////////////////////

cAYABCommunication::cAYABCommunication(QObject *parent) :
    QObject(parent)
{
    mSerialPortName = "ttyUSB0";
    mKnitData = 0;
    mStartNeedle = 0;
    mStopNeedle = 0;
    mNumberOfLines = 1;
    mLastLine = 0;
    mBlockCount = 0;

    mSerialPort = new QSerialPort(mSerialPortName, this);
    connect(mSerialPort,SIGNAL(readyRead()),this,SLOT(processData()));
    connect(this,SIGNAL(sLineRequest(quint8)),this,SLOT(sendLine(quint8)));
    connect(this,SIGNAL(sInfoRequestAnswer(quint8)),this,SLOT(processInfoRequestAnswer(quint8)));
    connect(this,SIGNAL(sStartRequestAnswer(quint8)),this,SLOT(processStartRequestAnswer(quint8)));
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
    mSerialPort->open(QSerialPort::ReadWrite);
}


// get Serial Port ///////////////////////////////////////////////////////////

QString cAYABCommunication::getSerialPort()
{
    return mSerialPortName;
}

// get Serial Port ///////////////////////////////////////////////////////////
void cAYABCommunication::getKnitData(QVector<QBitArray*>* knitData, qint32 startNeedle,
                                     qint32 stopNeedle, qint32 numberOfLines)
{
    mKnitData = knitData;
    mStartNeedle = startNeedle;
    mStopNeedle = stopNeedle;
    mNumberOfLines = numberOfLines;
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
    mSerialPort->read(message, 1);
    quint8 messageID = message[0];
    if(1 /*mSerialPort->waitForReadyRead(50)*/)
    {
        switch( messageID )
        {
        case 0xC1:
            // Start Request Answer
            qDebug("Start Request Answer");
            mSerialPort->read(message, 1);
            emit sStartRequestAnswer(message[0]);
            break;
        case 0x82:
            // Line Request
            qDebug("Line Request");
            mSerialPort->read(message, 1);
            emit sLineRequest(message[0]);
            break;
        case 0xC3:
            // Info Request Answer
            qDebug("Info Request Answer");
            mSerialPort->read(message, 1);
            emit sInfoRequestAnswer(message[0]);
            break;
        case 0xFF:
            // Debug Message
            mSerialPort->readLine(message, 50);
            qDebug() << "Debug Message: " << message;
            break;
        default:
            break;
        }
    }
}

// send Line to Hardware //////////////////////////////////////////////////////

void cAYABCommunication::sendLine(quint8 lineNumber)
{
    if(lineNumber == 0 && mLastLine == 255)
        mBlockCount++;
    mLastLine = lineNumber;
    qint32 actLine = (mBlockCount*256) + lineNumber;
    if(actLine < mNumberOfLines)
    {
        //Line is Part of Array --> Send Line
        char serialBuffer[2];
        serialBuffer[0] = (0x42); // check if signed
        serialBuffer[1] = lineNumber;
        mSerialPort->write(serialBuffer, 2);
        // Convert from QBitArray to QByteArray

        mSerialPort->write(bitsToBytes(*mKnitData->at(actLine)));
        if(actLine == mNumberOfLines - 1)
            serialBuffer[0] = 1;
        else
            serialBuffer[0] = 0;
        serialBuffer[1] = 0;
        mSerialPort->write(serialBuffer, 2);
        qDebug() << "Line " << lineNumber << " written...";
    }
}

// get Version //////////////////////////////////////////////////////

void cAYABCommunication::getVersionData()
{
    char serialBuffer[1];
    serialBuffer[0] = 0x03;
    mSerialPort->write(serialBuffer, 1);
    qDebug() << "Get Version";
}

// process Version //////////////////////////////////////////////////////

void cAYABCommunication::processInfoRequestAnswer(quint8 value)
{
    mVersionNumber = value;
    qDebug() << "Version: " << mVersionNumber;
}

// send Start //////////////////////////////////////////////////////

void cAYABCommunication::sendStart()
{
    char serialBuffer[3];
    serialBuffer[0] = 0x01;
    serialBuffer[1] = mStartNeedle - 1;
    serialBuffer[2] = mStopNeedle - 1;
    mSerialPort->write(serialBuffer, 3);
    qDebug() << "Start Triggered. Start Needle " << mStartNeedle << "Stop Needle: " << mStopNeedle;
}

// process Start Answer //////////////////////////////////////////////////////

void cAYABCommunication::processStartRequestAnswer(quint8 value)
{
    qDebug() << "Start Request: " << value;
}

// Array conversion //////////////////////////////////////////////////////

QByteArray cAYABCommunication::bitsToBytes(QBitArray bits) {
    QByteArray bytes;
    bytes.resize(bits.count()/8+1);
    bytes.fill(0);
    // Convert from QBitArray to QByteArray
    for(int b=0; b<bits.count(); ++b)
        bytes[b/8] = ( bytes.at(b/8) | ((bits[b]?1:0)<<(b%8)));
    return bytes;
}
