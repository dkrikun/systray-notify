# This is only needed for Python v2 but is harmless for Python v3.

from PySide import QtCore, QtGui
import time

import zmq
from api_pb2 import *
import sys

import icon_rc


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
        icon = QtGui.QIcon(':/heart.svg')

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
        """Handle incoming api messages."""

        # recv zmq message, non-blocking
        try:
            zmsg = self.zsck.recv(zmq.NOBLOCK)
        except zmq.ZMQError as e:
            if e.errno != zmq.EAGAIN:
                raise
            return

        # parse as protobuf Api, see api.proto
        api_msg = Api()
        api_msg.ParseFromString(zmsg)

        # check if requested to shut down
        if api_msg.die == True:
            QtGui.qApp.quit()

        # select appropriate icon to display in the system tray message
        if api_msg.icon == Api.NO:
            icon = QtGui.QSystemTrayIcon.NoIcon
        elif api_msg.icon == Api.INFO:
            icon = QtGui.QSystemTrayIcon.Information
        elif api_msg.icon == Api.WARN:
            icon = QtGui.QSystemTrayIcon.Warning
        elif api_msg.icon == Api.CRIT:
            icon = QtGui.QSystemTrayIcon.Critical

        # display the balloon message in the system tray
        self.showTrayMessage(api_msg.title, api_msg.body, icon)


    def messageClicked(self):
        self.hideTrayMessage()

    def showTrayMessage(self, title, body, icon):
        self.trayIcon.showMessage(title, body, icon, 10)

    def hideTrayMessage(self):
        """Hides a balloon message being displayed, if there is one."""

        self.trayIcon.hide()
        self.trayIcon.show()



if __name__ == '__main__':

    import sys

    # test for systray functionality
    systray_ok = QtGui.QSystemTrayIcon.isSystemTrayAvailable() and QtGui.QSystemTrayIcon.supportsMessages()

    if not systray_ok:
        QtGui.QMessageBox.critical(None, "systray-notify",
                """Could not start systray-notify because the system tray
                messages are not supported""")
        sys.exit(1)


    app = QtGui.QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
