# This is only needed for Python v2 but is harmless for Python v3.
#import sip
#sip.setapi('QVariant', 2)

from PySide import QtCore, QtGui
import time

import zmq
from api_pb2 import *
import sys

import systray_rc


class Window(QtGui.QDialog):
    def __init__(self):
        super(Window, self).__init__()

        # hide the window
        self.hide()

        # actions
        self.quitAction = QtGui.QAction("&Quit", self,
                triggered=QtGui.qApp.quit)

        # tray icon menu
        self.trayIconMenu = QtGui.QMenu(self)
        self.trayIconMenu.addAction(self.quitAction)

        # tray icon
        self.trayIcon = QtGui.QSystemTrayIcon(self)
        self.trayIcon.setContextMenu(self.trayIconMenu)
        icon = QtGui.QIcon(':/images/heart.svg')

        self.trayIcon.setIcon(icon)
        self.trayIcon.setToolTip("atooltip")
        self.trayIcon.messageClicked.connect(self.messageClicked)
        self.trayIcon.show()

        # timer to check incoming messages
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.recvMessages)
        self.timer.start(1)

        self.zctx = zmq.Context()
        self.zsck = self.zctx.socket(zmq.PULL)
        self.zsck.bind("tcp://*:7272")


    def recvMessages(self):
        try:
            zmsg = self.zsck.recv(zmq.NOBLOCK)
        except zmq.ZMQError as e:
            if e.errno != zmq.EAGAIN:
                raise
            return

        api_msg = Api()
        api_msg.ParseFromString(zmsg)

        if api_msg.icon == Api.NO:
            icon = QtGui.QSystemTrayIcon.NoIcon
        elif api_msg.icon == Api.INFO:
            icon = QtGui.QSystemTrayIcon.Information
        elif api_msg.icon == Api.WARN:
            icon = QtGui.QSystemTrayIcon.Warning
        elif api_msg.icon == Api.CRIT:
            icon = QtGui.QSystemTrayIcon.Critical

        self.showMessageText(api_msg.title, api_msg.body, icon)


    def showMessageText(self, title, body, icon):
        self.trayIcon.showMessage(title, body, icon, 10)


    def messageClicked(self):
        QtGui.QMessageBox.information(None, "Systray",
                "Sorry, I already gave what help I could.\nMaybe you should "
                "try asking a human?")



if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)

    if not QtGui.QSystemTrayIcon.isSystemTrayAvailable():
        QtGui.QMessageBox.critical(None, "Systray",
                "No system tray available.")
        sys.exit(1)

    QtGui.QApplication.setQuitOnLastWindowClosed(False)


    window = Window()
    sys.exit(app.exec_())
