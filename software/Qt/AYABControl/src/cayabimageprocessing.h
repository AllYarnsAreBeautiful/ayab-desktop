#ifndef CAYABIMAGEPROCESSING_H
#define CAYABIMAGEPROCESSING_H

#include <QObject>
#include <QBitArray>
#include <QColor>
#include <QImage>


class cAYABImageProcessing : public QObject
{
    Q_OBJECT
public:
    explicit cAYABImageProcessing(QObject *parent = 0);
    ~cAYABImageProcessing();

    void setImageProperties(qint32 startNeedle, qint32 stopNeedle, qint32 numberOfLines, QColor mainYarnColor, QColor contrastYarnColor);
    void drawFrame();
    QImage *getPreviewImage();

signals:
    
public slots:
    void getKnitData(QVector<QBitArray*>* knitData, qint32 startNeedle, qint32 stopNeedle,
                     qint32 numberOfLines);

private:
    qint32 mStartNeedle;
    qint32 mStopNeedle;
    qint32 mNumberOfLines;
    QColor mMainYarnColor;
    QColor mContrastYarnColor;

    QImage *mPreviewImage;
    
};

#endif // CAYABIMAGEPROCESSING_H
