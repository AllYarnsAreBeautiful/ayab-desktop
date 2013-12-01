#ifndef CAYABCOMMUNICATION_H
#define CAYABCOMMUNICATION_H

#include <QObject>
#include <QtSerialPort/QSerialPort>
#include <QtSerialPort/QSerialPortInfo>
#include <QStringList>
#include <QVector>
#include <QBitArray>

#include <QtCore/QDebug>

class QQuickWindow;

class cAYABCommunication : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QString serialPort READ getSerialPort WRITE setSerialPort NOTIFY serialPortChanged)
public:
    explicit cAYABCommunication(QObject *parent = 0);
    ~cAYABCommunication();
    void setSerialPort(QString port);
    QString getSerialPort();
    QStringList getAvailablePorts();
    QByteArray bitsToBytes(QBitArray bits);

public slots:
    void processData();
    void sendLine(quint8 lineNumber);
    void getKnitData(QVector<QBitArray*>* knitData, qint32 startNeedle, qint32 stopNeedle,
                     qint32 numberOfLines);
    void getVersionData();
    void processInfoRequestAnswer(quint8 value);
    void processStartRequestAnswer(quint8 value);
    void sendStart();

    
signals:
    void serialPortChanged();
    void sStartRequestAnswer(quint8 value);
    void sLineRequest(quint8 value);
    void sInfoRequestAnswer(quint8 value);

    
    
private:
    QString mSerialPortName;
    QSerialPortInfo *mSerialPortInfo;
    QSerialPort *mSerialPort;
    QVector<QBitArray*>* mKnitData;
    qint32 mStartNeedle;
    qint32 mStopNeedle;
    qint32 mNumberOfLines;
    qint32 mLastLine;
    qint32 mBlockCount;
    qint32 mVersionNumber;
    char message[50];

};

#endif // CAYABCOMMUNICATION_H
