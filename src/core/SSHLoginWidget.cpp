#include "SSHLoginWidget.h"
#include <QLineEdit>
#include <QPushButton>
#include <QVBoxLayout>

SSHLoginWidget::SSHLoginWidget(QWidget *parent)
    : QWidget(parent)
{
    lineEditUser = new QLineEdit(this);
    lineEditUser->setPlaceholderText("Username");

    lineEditHost = new QLineEdit(this);
    lineEditHost->setPlaceholderText("Host / IP");

    btnConnect = new QPushButton("Connect", this);

    QVBoxLayout *layout = new QVBoxLayout(this);
    layout->addWidget(lineEditUser);
    layout->addWidget(lineEditHost);
    layout->addWidget(btnConnect);
    layout->setAlignment(Qt::AlignHCenter | Qt::AlignVCenter);

    connect(btnConnect, &QPushButton::clicked, this, &SSHLoginWidget::onConnectClicked);
}

void SSHLoginWidget::onConnectClicked()
{
    emit connectRequested(lineEditUser->text(), lineEditHost->text());
}
