#include "guages.h"

#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    Guages w;
    w.show();
    return a.exec();
}
