#include "MainWindow.h"
#include "ui_MainWindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    setMinimumSize(1080, 608);
    resize(1280, 720);

    m_pixWire1.load(":/images/Wire1.png");

    ui->lblWire1->setScaledContents(true);
    ui->lblWire1->setPixmap(m_pixWire1);
    ui->lblWire1->move(0, 0);

    auto shadow = new QGraphicsDropShadowEffect(this);
    shadow->setBlurRadius(25);
    shadow->setOffset(-6, 6);
    shadow->setColor(QColor(0, 0, 0, 120));

    ui->containerDynamic->setGraphicsEffect(shadow);
    
    updateImageSize();
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::resizeEvent(QResizeEvent *event)
{
    QMainWindow::resizeEvent(event);
    updateImageSize();
}

void MainWindow::updateImageSize()
{
    QSize windowSize = size();
    
    qreal aspectRatio = 1920.0 / 1080.0;
    
    int newWidth = windowSize.width();
    int newHeight = static_cast<int>(newWidth / aspectRatio);
    
    if (newHeight > windowSize.height()) {
        newHeight = windowSize.height();
        newWidth = static_cast<int>(newHeight * aspectRatio);
    }
    
    ui->lblWire1->setFixedSize(newWidth, newHeight);
    ui->lblWire1->move(0, 0);
}