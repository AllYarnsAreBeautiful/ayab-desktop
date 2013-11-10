#include <QDebug>
#include <QApplication>
#include <QQmlApplicationEngine>
#include <QQuickWindow>

#include "cayabbackend.h"

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    // load QML
    QQmlApplicationEngine engine;
    engine.load(QUrl("qrc:/qml/main.qml"));

    // get application window
    QObject *rootobject = engine.rootObjects().at(0);
    QQuickWindow *window = qobject_cast<QQuickWindow*>(rootobject);
    if (!window) {
        qCritical("Error: No window found");
        return -1;
    }

    // create Backend
    cAYABBackend AYABBackend;
    AYABBackend.setWindow(window);

    return app.exec();
}
