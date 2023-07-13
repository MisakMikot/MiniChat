import sys

from PyQt5.QtCore import Qt, pyqtSignal, QEasingCurve, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout, QApplication, QFrame, QWidget

from qfluentwidgets import (NavigationBar, NavigationItemPosition, NavigationWidget, MessageBox,
                            isDarkTheme, setTheme, Theme, setThemeColor, SearchLineEdit, PopUpAniStackedWidget)
from qfluentwidgets import FluentIcon as FIF
from qframelesswindow import FramelessWindow, TitleBar


window_qss = '''Widget > QLabel {
    font: 24px 'Segoe UI', 'Microsoft YaHei';
}

StackedWidget {
    border: 1px solid rgb(229, 229, 229);
    border-right: none;
    border-bottom: none;
    border-top-left-radius: 10px;
    background-color: rgb(249, 249, 249);
}

Window {
    background-color: rgb(243, 243, 243);
}

CustomTitleBar>QLabel#titleLabel {
    color: black;
    background: transparent;
    font: 13px 'Segoe UI';
    padding: 0 10px
}

MinimizeButton {
    qproperty-normalColor: black;
    qproperty-normalBackgroundColor: transparent;
    qproperty-hoverColor: black;
    qproperty-hoverBackgroundColor: rgba(0, 0, 0, 26);
    qproperty-pressedColor: black;
    qproperty-pressedBackgroundColor: rgba(0, 0, 0, 51)
}


MaximizeButton {
    qproperty-normalColor: black;
    qproperty-normalBackgroundColor: transparent;
    qproperty-hoverColor: black;
    qproperty-hoverBackgroundColor: rgba(0, 0, 0, 26);
    qproperty-pressedColor: black;
    qproperty-pressedBackgroundColor: rgba(0, 0, 0, 51)
}

CloseButton {
    qproperty-normalColor: black;
    qproperty-normalBackgroundColor: transparent;
}
'''


#自定义控件组
class StackedWidget(QFrame):
    """ Stacked widget """

    currentChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.hBoxLayout = QHBoxLayout(self)
        self.view = PopUpAniStackedWidget(self)

        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.view)

        self.view.currentChanged.connect(self.currentChanged)

    def addWidget(self, widget):
        """ add widget to view """
        self.view.addWidget(widget)

    def widget(self, index: int):
        return self.view.widget(index)

    def setCurrentWidget(self, widget, popOut=False):
        if not popOut:
            self.view.setCurrentWidget(widget, duration=300)
        else:
            self.view.setCurrentWidget(
                widget, True, False, 200, QEasingCurve.InQuad)

    def setCurrentIndex(self, index, popOut=False):
        self.setCurrentWidget(self.view.widget(index), popOut)


#自定义标题栏
class CustomTitleBar(TitleBar):
    """ Title bar with icon and title """

    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedHeight(48)
        self.hBoxLayout.removeWidget(self.minBtn)
        self.hBoxLayout.removeWidget(self.maxBtn)
        self.hBoxLayout.removeWidget(self.closeBtn)

        # add window icon
        self.iconLabel = QLabel(self)
        self.iconLabel.setFixedSize(18, 18)
        self.hBoxLayout.insertSpacing(0, 20)
        self.hBoxLayout.insertWidget(
            1, self.iconLabel, 0, Qt.AlignLeft | Qt.AlignVCenter)
        self.window().windowIconChanged.connect(self.setIcon)

        # add title label
        self.titleLabel = QLabel(self)
        self.hBoxLayout.insertWidget(
            2, self.titleLabel, 0, Qt.AlignLeft | Qt.AlignVCenter)
        self.titleLabel.setObjectName('titleLabel')
        self.window().windowTitleChanged.connect(self.setTitle)

        # add search line edit
        self.searchLineEdit = SearchLineEdit(self)
        self.searchLineEdit.setPlaceholderText('搜索应用、游戏、电影、设备等')
        self.searchLineEdit.setFixedWidth(400)
        self.searchLineEdit.setClearButtonEnabled(True)

        self.vBoxLayout = QVBoxLayout()
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.setSpacing(0)
        self.buttonLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonLayout.setAlignment(Qt.AlignTop)
        self.buttonLayout.addWidget(self.minBtn)
        self.buttonLayout.addWidget(self.maxBtn)
        self.buttonLayout.addWidget(self.closeBtn)
        self.vBoxLayout.addLayout(self.buttonLayout)
        self.vBoxLayout.addStretch(1)
        self.hBoxLayout.addLayout(self.vBoxLayout, 0)

    def setTitle(self, title):
        self.titleLabel.setText(title)
        self.titleLabel.adjustSize()

    def setIcon(self, icon):
        self.iconLabel.setPixmap(QIcon(icon).pixmap(18, 18))

    def resizeEvent(self, e):
        self.searchLineEdit.move((self.width() - self.searchLineEdit.width()) //2, 8)

class Window(FramelessWindow):

    def __init__(self):
        super().__init__()
        self.titleBar = CustomTitleBar(self)
        self.setTitleBar(self.titleBar)

        # use dark theme mode
        # setTheme(Theme.DARK)

        # change the theme color
        # setThemeColor('#0078d4')

        self.hBoxLayout = QHBoxLayout(self)
        self.navigationBar = NavigationBar(self)
        self.stackWidget = StackedWidget(self)

        self.initLayout()
        self.initWindow()
        self.initNavigation()


    #初始化导航栏
    def initNavigation(self):
        #self.addSubInterface(self.homeInterface, FIF.HOME, '主页', selectedIcon=FIF.HOME_FILL)
        #self.addSubInterface(self.appInterface, FIF.APPLICATION, '应用')
        #self.addSubInterface(self.videoInterface, FIF.VIDEO, '视频')

        #self.addSubInterface(self.libraryInterface, FIF.BOOK_SHELF, '库', NavigationItemPosition.BOTTOM, FIF.LIBRARY_FILL)
        self.navigationBar.addItem(
            routeKey='Help',
            icon=FIF.HELP,
            text='帮助',
            onClick=self.showMessageBox,
            selectable=False,
            position=NavigationItemPosition.BOTTOM,
        )

        self.stackWidget.currentChanged.connect(self.onCurrentInterfaceChanged)
        #self.navigationBar.setCurrentItem(self.homeInterface.objectName())

    #初始化布局
    def initLayout(self):
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 48, 0, 0)
        self.hBoxLayout.addWidget(self.navigationBar)
        self.hBoxLayout.addWidget(self.stackWidget)
        self.hBoxLayout.setStretchFactor(self.stackWidget, 1)


    #初始化样式
    def initWindow(self):
        self.resize(900, 700)
        #self.setWindowIcon(QIcon(':/qfluentwidgets/images/logo.png'))
        self.setWindowTitle('MiniChat')
        self.titleBar.setAttribute(Qt.WA_StyledBackground)

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

        self.setStyleSheet(window_qss)


    #向导航栏增加控件
    def addSubInterface(self, interface, icon, text: str, position=NavigationItemPosition.TOP, selectedIcon=None):
        """ add sub interface """
        self.stackWidget.addWidget(interface)
        self.navigationBar.addItem(
            routeKey=interface.objectName(),
            icon=icon,
            text=text,
            onClick=lambda: self.switchTo(interface),
            selectedIcon=selectedIcon,
            position=position,
        )


    #切换到控件
    def switchTo(self, widget):
        self.stackWidget.setCurrentWidget(widget)


    #显示帮助信息
    def showMessageBox(self):
        w = MessageBox(
            '帮助',
            '如果你发现了Bug，或者想要为项目做出贡献，欢迎前往项目GitHub页面',
            self
        )
        w.yesButton.setText('前往项目页面')
        w.cancelButton.setText('取消')

        if w.exec():
            QDesktopServices.openUrl(QUrl("https://github.com/MisakMikot/MiniChat"))


    #切换控件时导航栏自动跟随
    def onCurrentInterfaceChanged(self, index):
        widget = self.stackWidget.widget(index)
        self.navigationBar.setCurrentItem(widget.objectName())



if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec_()