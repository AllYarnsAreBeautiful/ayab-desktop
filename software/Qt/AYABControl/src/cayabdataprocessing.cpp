#include "cayabdataprocessing.h"

// Constructor ///////////////////////////////////////////////////////////////

cAYABDataProcessing::cAYABDataProcessing(QObject *parent) :
    QObject(parent)
{
    mKnitData = new QVector<QBitArray*>(1, new QBitArray(200));
    mStartNeedle = 0;
    mStopNeedle = 0;
    mNumberOfLines = 1;
    mMainYarnColor = QColor::fromRgb(255,255,255);
    mContrastYarnColor = QColor::fromRgb(0,0,0);
}

// Destructor ////////////////////////////////////////////////////////////////

cAYABDataProcessing::~cAYABDataProcessing()
{
}

// Set Properties ////////////////////////////////////////////////////////////

void cAYABDataProcessing::setDataProperties(qint32 startNeedle, qint32 stopNeedle, qint32 numberOfLines, QColor mainYarnColor, QColor contrastYarnColor)
{
    mStartNeedle = startNeedle;
    mStopNeedle = stopNeedle;
    mNumberOfLines = numberOfLines;
    mMainYarnColor = mainYarnColor;
    mContrastYarnColor = contrastYarnColor;

    mKnitData->clear();
    mKnitData = new QVector<QBitArray*>(mNumberOfLines, new QBitArray(200));

    //Hier die qml Sachen rein
}

// Get Properties ////////////////////////////////////////////////////////////

qint32 cAYABDataProcessing::getStartNeedle()
{
    return mStartNeedle;
}

qint32 cAYABDataProcessing::getStopNeedle()
{
    return mStopNeedle;
}

qint32 cAYABDataProcessing::getNumberOfLines()
{
    return mNumberOfLines;
}

QColor cAYABDataProcessing::getMainYarnColor()
{
    return mMainYarnColor;
}

QColor cAYABDataProcessing::getContrastYarnColor()
{
    return mContrastYarnColor;
}

QBitArray *cAYABDataProcessing::getLine(qint32 line)
{
    if(mKnitData->at(line) != 0)
        return mKnitData->at(line);
    else
        return 0;
}

void cAYABDataProcessing::setPixel(qint32 needle, qint32 line, bool pixel)
{
    if(mKnitData->at(line) != 0 && needle < 200)
    {
        mKnitData->at(line)->setBit(needle, pixel);
    }
}

bool cAYABDataProcessing::getPixel(qint32 needle, qint32 line)
{
    if(mKnitData->at(line) != 0 && needle < 200)
        return mKnitData->at(line)->at(needle);
    else
        return false;
}
