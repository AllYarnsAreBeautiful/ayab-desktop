#ifndef CAYABDATAPROCESSING_H
#define CAYABDATAPROCESSING_H

#include <QObject>
#include <QStringList>
#include <QVector>
#include <QBitArray>
#include <QColor>

#include <QtCore/QDebug>


class cAYABDataProcessing : public QObject
{
    Q_OBJECT
public:
    explicit cAYABDataProcessing(QObject *parent = 0);
    ~cAYABDataProcessing();
    void setDataProperties(qint32 startNeedle, qint32 stopNeedle, qint32 numberOfLines,
                           QColor mainYarnColor, QColor contrastYarnColor, QString projectName);
    qint32 getStartNeedle();
    qint32 getStopNeedle();
    qint32 getNumberOfLines();
    QColor getMainYarnColor();
    QColor getContrastYarnColor();
    QString getProjectName();
    QBitArray *getLine(qint32 line);

    bool getPixel(qint32 needle, qint32 line);

    ///DEBUG
    void setTestPattern();

signals:   
    void sKnitDataCreated(QVector<QBitArray*>* knitData, qint32 startNeedle, qint32 stopNeedle,
                          qint32 numberOfLines);
    
public slots:
    void setPixel(qint32 needle, qint32 line, bool pixel);

private:
    QVector<QBitArray*>* mKnitData;
    qint32 mStartNeedle;
    qint32 mStopNeedle;
    qint32 mNumberOfLines;
    QColor mMainYarnColor;
    QColor mContrastYarnColor;
    QString mProjectName;
    
};

#endif // CAYABDATAPROCESSING_H
