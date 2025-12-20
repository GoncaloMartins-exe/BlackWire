#include "MainWindow.h"
#include "ui_MainWindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    setWindowTitle("BlackWire");

    resize(1280, 720);
    setMinimumSize(1080, 600);
}

MainWindow::~MainWindow()
{
    delete ui;
}