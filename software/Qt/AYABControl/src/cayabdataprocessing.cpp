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

    /// DEBUG ///
    setTestPattern();
}

// Destructor ////////////////////////////////////////////////////////////////

cAYABDataProcessing::~cAYABDataProcessing()
{
}

// Set Properties ////////////////////////////////////////////////////////////

void cAYABDataProcessing::setDataProperties(qint32 startNeedle, qint32 stopNeedle,
                                            qint32 numberOfLines, QColor mainYarnColor,
                                            QColor contrastYarnColor, QString projectName)
{
    mStartNeedle = startNeedle;
    mStopNeedle = stopNeedle;
    mNumberOfLines = numberOfLines;
    mMainYarnColor = mainYarnColor;
    mContrastYarnColor = contrastYarnColor;
    mProjectName = projectName;

    mKnitData->~QVector();
    mKnitData = new QVector<QBitArray*>(0);
    for(int i = 0; i < mNumberOfLines; i++)
        mKnitData->append(new QBitArray(200));
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

QString cAYABDataProcessing::getProjectName()
{
    return mProjectName;
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

//// zum Debuggen ////

void cAYABDataProcessing::setTestPattern()
{
    setDataProperties(1, 200, 16, QColor::fromRgb(255,255,255),QColor::fromRgb(0,0,0), "Test Pattern");
    for(int i = 0; i < mNumberOfLines; i++)
    {
        for(int j = 0; j<200; j++)
        {
            if(((j % 16)-i) == 0)
                setPixel(j,i,true);
            else
                setPixel(j,i,false);
        }
    }

}
