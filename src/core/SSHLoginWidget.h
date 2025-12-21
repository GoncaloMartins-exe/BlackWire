#pragma once
#include <QWidget>

QT_BEGIN_NAMESPACE
class QLineEdit;
class QPushButton;
QT_END_NAMESPACE

class SSHLoginWidget : public QWidget
{
    Q_OBJECT
public:
    explicit SSHLoginWidget(QWidget *parent = nullptr);

signals:
    void connectRequested(const QString &user, const QString &host);

private:
    QLineEdit *lineEditUser;
    QLineEdit *lineEditHost;
    QPushButton *btnConnect;

private slots:
    void onConnectClicked();
};
