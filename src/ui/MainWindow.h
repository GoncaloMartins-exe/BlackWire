#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QPixmap>
#include <QResizeEvent>
#include <QGraphicsDropShadowEffect>

#include "ui_MainWindow.h"

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

protected:
    /**
     * @brief Handles window resize events.
     *
     * Recalculates and updates visual elements that depend on the
     * window size, such as background scaling and positioning.
     *
     * @param event Resize event information provided by Qt.
     */
    void resizeEvent(QResizeEvent *event) override;

private:
    Ui::MainWindow *ui;
    QPixmap m_pixWire1;

    /**
     * @brief Configures the main window properties.
     *
     * Sets the initial size, minimum constraints and any
     * base window-level configuration required at startup.
     */
    void setupWindow();

    /**
     * @brief Initializes and configures the background image.
     *
     * Loads the background pixmap, applies it to the corresponding
     * label and prepares it for dynamic resizing while preserving
     * the aspect ratio.
     */
    void setupBackground();

    /**
     * @brief Applies visual effects to UI components.
     *
     * Configures graphical effects such as drop shadows for
     * specific widgets to improve visual depth and separation.
     */
    void setupShadows();

    /**
     * @brief Updates the background size and position.
     *
     * Recalculates the background dimensions based on the current
     * window size while preserving the original aspect ratio.
     * This method is typically called after resize events.
     */
    void updateBackgroundSize();

};

#endif // MAINWINDOW_H