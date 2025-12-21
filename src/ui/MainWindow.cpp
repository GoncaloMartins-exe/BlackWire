#include "MainWindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    setupWindow();
    setupBackground();
    ui->containerContent->raise();

    updateBackgroundSize();
}

// ====================================
// === Construction and destruction ===
// ====================================

MainWindow::~MainWindow()
{
    delete ui;
}

// ============================
// === Initial window setup ===
// ============================

void MainWindow::setupWindow()
{
    setMinimumSize(1080, 608);
    resize(1280, 720);
}

// =============================
// === Background management ===
// === (images and scaling)  ===
// =============================

void MainWindow::setupBackground()
{
    m_pixWire1.load(":/images/Wire1.png");

    ui->lblWire1->setScaledContents(true);
    ui->lblWire1->setPixmap(m_pixWire1);
    ui->lblWire1->move(0, 0);
}

// =============================================
// === Event Management and Dynamic Behavior ===
// =============================================

void MainWindow::resizeEvent(QResizeEvent *event)
{
    QMainWindow::resizeEvent(event);
    updateBackgroundSize();
}

void MainWindow::updateBackgroundSize()
{
    const QSize windowSize = size();
    constexpr qreal aspectRatio = 1920.0 / 1080.0;

    int newWidth = windowSize.width();
    int newHeight = static_cast<int>(newWidth / aspectRatio);

    if (newHeight > windowSize.height()) {
        newHeight = windowSize.height();
        newWidth = static_cast<int>(newHeight * aspectRatio);
    }

    ui->lblWire1->setFixedSize(newWidth, newHeight);
    ui->lblWire1->move(0, 0);
}


void MainWindow::on_btnAddDevice_clicked()
{
    QDialog dialog(this);
    dialog.setWindowFlags(Qt::FramelessWindowHint | Qt::Dialog);
    dialog.setAttribute(Qt::WA_TranslucentBackground);

    QVBoxLayout *layout = new QVBoxLayout(&dialog);
    layout->setContentsMargins(20, 20, 20, 20);

    QWidget *contentContainer = new QWidget(&dialog);
    contentContainer->setStyleSheet(
        "background-color: #FFFFFF;"
        "color: #000000;"
        "border-radius: 15px;"
    );

    QGraphicsDropShadowEffect *shadow = new QGraphicsDropShadowEffect;
    shadow->setBlurRadius(30);
    shadow->setColor(QColor(0,0,0,100));
    shadow->setOffset(0, 0);
    contentContainer->setGraphicsEffect(shadow);

    QVBoxLayout *containerLayout = new QVBoxLayout(contentContainer);
    SSHLoginWidget *loginWidget = new SSHLoginWidget(contentContainer);
    
    loginWidget->setStyleSheet("QLabel { color: black; } QLineEdit { color: black; border: 1px solid #CCC; }");
    
    containerLayout->addWidget(loginWidget);

    connect(loginWidget, &SSHLoginWidget::connectRequested, [&](const QString &u, const QString &h){
        dialog.accept();
        startSSHConnection(u, h);
    });

    layout->addWidget(contentContainer);
    dialog.exec(); 
}

void MainWindow::startSSHConnection(const QString &user, const QString &host)
{
    qDebug() << "A iniciar terminal SSH para:" << user << "@" << host;
    QString sshCommand = "ssh " + user + "@" + host;
    QString program = "cmd.exe";
    QStringList arguments;
    arguments << "/c" << "start" << "BlackWire SSH" << "cmd" << "/k" << sshCommand;

    QProcess::startDetached(program, arguments);
}