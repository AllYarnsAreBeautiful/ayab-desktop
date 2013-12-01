#include "cayabimageprocessing.h"

// Constructor ///////////////////////////////////////////////////////////////

cAYABImageProcessing::cAYABImageProcessing(QObject *parent) :
    QObject(parent)
{
    //Set Standard Variables
    mStartNeedle = 1;
    mStopNeedle = 200;
    mNumberOfLines = 1;
    mMainYarnColor = QColor::fromRgb(0,0,0);
    mContrastYarnColor = QColor::fromRgb(255,255,255);

    mPreviewImage = new QImage(200,1,QImage::Format_RGB32);
}

// Destructor ////////////////////////////////////////////////////////////////

cAYABImageProcessing::~cAYABImageProcessing()
{
}

// SetNewImageData ////////////////////////////////////////////////////////////////

void cAYABImageProcessing::setImageProperties(qint32 startNeedle, qint32 stopNeedle,
                                            qint32 numberOfLines, QColor mainYarnColor,
                                            QColor contrastYarnColor)
{
    mStartNeedle = startNeedle;
    mStopNeedle = stopNeedle;
    mNumberOfLines = numberOfLines;
    mMainYarnColor = mainYarnColor;
    mContrastYarnColor = contrastYarnColor;

    mPreviewImage->~QImage();
    mPreviewImage = new QImage(200,mNumberOfLines,QImage::Format_RGB32);
    drawFrame();
}

// get Knit Data ///////////////////////////////////////////////////////////
void cAYABImageProcessing::getKnitData(QVector<QBitArray*>* knitData, qint32 startNeedle,
                                     qint32 stopNeedle, qint32 numberOfLines)
{
    //mKnitData = knitData;
    mStartNeedle = startNeedle;
    mStopNeedle = stopNeedle;
    mNumberOfLines = numberOfLines;
}

// Draw Frame ////////////////////////////////////////////////////////////////
void cAYABImageProcessing::drawFrame()
{
    for(int i = 0; i < mNumberOfLines; i++)
    {
        for(int j = 0; j < 200; j++)
        {
            if(j < mStartNeedle-1 && j > mStopNeedle-1)
            {
                mPreviewImage->setPixel(j,i,0xff777777);
            }
            else
            {
                mPreviewImage->setPixel(j,i,mMainYarnColor.value());
            }
        }
    }
}

// get Image ////////////////////////////////////////////////////////////////
QImage * cAYABImageProcessing::getPreviewImage()
{
    return mPreviewImage;
}
