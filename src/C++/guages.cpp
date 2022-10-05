#include "guages.h"
#include "./ui_guages.h"

Guages::Guages(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::Guages)
{
    ui->setupUi(this);
}

Guages::~Guages()
{
    delete ui;
}

