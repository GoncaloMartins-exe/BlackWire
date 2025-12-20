#include "MainWindow.h"
#include "ui_MainWindow.h"
#include <QPixmap>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    const int minW = 1080;
    const int minH = 608;
    
    setMinimumSize(minW, minH);
    resize(1280, 720);

    QPixmap p1(":/images/Wire1.png");
    QPixmap p1Fixed = p1.scaled(minW, minH, Qt::KeepAspectRatioByExpanding, Qt::SmoothTransformation);
    ui->lblWire1->setPixmap(p1Fixed);
    ui->lblWire1->setFixedSize(minW, minH);
}

MainWindow::~MainWindow()
{
    delete ui;
}