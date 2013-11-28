#ifndef CAYABCOMMUNICATION_H
#define CAYABCOMMUNICATION_H

#include <QObject>
#include <QtSerialPort/QSerialPort>
#include <QtSerialPort/QSerialPortInfo>
#include <QStringList>

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
    //bool writeLineToAYAB(QBitArray *line, qint16 lineNumber);

public slots:
    void processData();
    void sendLine(quint8 lineNumber);

    
signals:
    void serialPortChanged();

    void sInitRequestAnswer(quint8 value);
    void sStartRequestAnswer(quint8 value);
    void sLineRequest(quint8 value);
    void sStopRequestAnswer(quint8 value);
    void sInfoRequestAnswer(quint8 value);
    
    
private:
    QString mSerialPortName;
    QSerialPortInfo *mSerialPortInfo;
    QSerialPort *mSerialPort;

};

#endif // CAYABCOMMUNICATION_H
