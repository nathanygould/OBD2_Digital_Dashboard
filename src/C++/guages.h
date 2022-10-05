#ifndef GUAGES_H
#define GUAGES_H

#include <QMainWindow>

QT_BEGIN_NAMESPACE
namespace Ui { class Guages; }
QT_END_NAMESPACE

class Guages : public QMainWindow
{
    Q_OBJECT

public:
    Guages(QWidget *parent = nullptr);
    ~Guages();

private:
    Ui::Guages *ui;
};
#endif // GUAGES_H
