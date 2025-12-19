#include "MainWindow.h"
#include "ui_MainWindow.h"
#include <QDateTime>
#include <QResizeEvent>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    this->setStyleSheet("#MainWindow { border-image: url(:/images/background.png) 0 0 0 0 stretch stretch; }");

    this->setWindowTitle("BlackWire");
    this->resize(1280, 720);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::resizeEvent(QResizeEvent *event)
{
    int w = event->size().width();
    int h = event->size().height();

    int idealH = w * 9 / 16;
    int idealW = h * 16 / 9;

    if (idealH <= h)
        QMainWindow::resizeEvent(new QResizeEvent(QSize(w, idealH), event->oldSize()));
    else
        QMainWindow::resizeEvent(new QResizeEvent(QSize(idealW, h), event->oldSize()));
}