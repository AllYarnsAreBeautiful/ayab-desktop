#ifndef CAYABBACKEND_H
#define CAYABBACKEND_H


#include <QObject>
#include "cayabcommunication.h"
#include "cayabdataprocessing.h"
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
private:
    QQuickWindow *mWindow;
    cAYABCommunication *AYABCommunication;
    cAYABDataProcessing *AYABDataProcessing;
    
};

#endif // CAYABBACKEND_H
