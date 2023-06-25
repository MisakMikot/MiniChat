# coding:utf-8
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout

from qfluentwidgets import InfoBarIcon, InfoBar, PushButton, setTheme, Theme, FluentIcon, InfoBarPosition


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        # setTheme(Theme.DARK)

        self.hBoxLayout = QHBoxLayout(self)
        self.button1 = PushButton('Information', self)
        self.button2 = PushButton('Success', self)
        self.button3 = PushButton('Warning', self)
        self.button4 = PushButton('Error', self)
        self.button5 = PushButton('Custom', self)

        self.button1.clicked.connect(self.createInfoInfoBar)
        self.button2.clicked.connect(self.createSuccessInfoBar)
        self.button3.clicked.connect(self.createWarningInfoBar)
        self.button4.clicked.connect(self.createErrorInfoBar)
        self.button5.clicked.connect(self.createCustomInfoBar)

        self.hBoxLayout.addWidget(self.button1)
        self.hBoxLayout.addWidget(self.button2)
        self.hBoxLayout.addWidget(self.button3)
        self.hBoxLayout.addWidget(self.button4)
        self.hBoxLayout.addWidget(self.button5)
        self.hBoxLayout.setContentsMargins(30, 0, 30, 0)

        self.resize(700, 700)

    def createInfoInfoBar(self):
        content = "My name is kira yoshikake, 33 years old. Living in the villa area northeast of duwangting, unmarried. I work in Guiyou chain store. Every day I have to work overtime until 8 p.m. to go home. I don't smoke. The wine is only for a taste. Sleep at 11 p.m. for 8 hours a day. Before I go to bed, I must drink a cup of warm milk, then do 20 minutes of soft exercise, get on the bed, and immediately fall asleep. Never leave fatigue and stress until the next day. Doctors say I'm normal."
        w = InfoBar(
            icon=InfoBarIcon.INFORMATION,
            title='Title',
            content=content,
            orient=Qt.Vertical,    # vertical layout
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=self
        )
        w.addWidget(PushButton('Action'))
        w.show()

    def createSuccessInfoBar(self):
        # convenient class mothod
        InfoBar.success(
            title='Lesson 4',
            content="With respect, let's advance towards a new stage of the spin.",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self
        )

    def createWarningInfoBar(self):
        InfoBar.warning(
            title='Lesson 3',
            content="Believe in the spin, just keep believing!",
            orient=Qt.Horizontal,
            isClosable=False,   # disable close button
            position=InfoBarPosition.TOP_LEFT,
            duration=2000,
            parent=self
        )

    def createErrorInfoBar(self):
        InfoBar.error(
            title='Lesson 5',
            content="迂回路を行けば最短ルート。",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=-1,    # won't disappear automatically
            parent=self
        )

    def createCustomInfoBar(self):
        w = InfoBar.new(
            icon=FluentIcon.GITHUB,
            title='Zeppeli',
            content="人間讃歌は「勇気」の讃歌ッ！！ 人間のすばらしさは勇気のすばらしさ！！",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM,
            duration=2000,
            parent=self
        )
        w.setCustomBackgroundColor('white', '#202020')


if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec_()