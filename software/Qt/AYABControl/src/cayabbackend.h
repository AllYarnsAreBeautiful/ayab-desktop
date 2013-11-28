#ifndef CAYABBACKEND_H
#define CAYABBACKEND_H


#include <QObject>
#include "cayabcommunication.h"
#include "cayabdataprocessing.h"
#include "cayabimageprocessing.h"
class QQuickWindow;

class cAYABBackend : public QObject
{
    Q_OBJECT
public:
    explicit cAYABBackend(QObject *parent = 0);
    ~cAYABBackend();
    void setWindow(QQuickWindow *window);
    cAYABCommunication* getAYABCommunication();
    
signals:
    
public slots:
    void helpAbout();
    void settingsDialog();
    void slotSettingsBoxOKTriggered();
    void newDialog();
    void slotNewBoxOKTriggered();
    void slotAboutTriggered();
private:
    QQuickWindow *mWindow;
    cAYABCommunication *AYABCommunication;
    cAYABDataProcessing *AYABDataProcessing;
    cAYABImageProcessing *AYABImageProcessing;
    
};

#endif // CAYABBACKEND_H
