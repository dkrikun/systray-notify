#!/usr/bin/env python
# coding: utf-8

"""
Micro-service to display user-friendly notifications using the system tray.
"""

__version__ = '0.1.0'
__author__ = 'Daniel Krikun'
__license__= 'MIT'

import time
import sys
import argparse

from PySide import QtCore, QtGui
import zmq
from api_pb2 import *

import icon_rc

# icon resource selector
# note that currently the icon cannot be selected dynamically, but rather
# it has to be processed by the resource compiler first,
# run `build.bat` to do that
#
ICON_SELECTOR = ':/icon.png'
CAPTION = 'Notifications service'

class Window(QtGui.QDialog):
    def __init__(self, address, tooltip):
        super(Window, self).__init__()

        # hide the window
        self.hide()

        # actions
        self.quitAction = QtGui.QAction("&Exit", self,
                triggered=QtGui.qApp.quit)

        # tray icon menu
        self.trayIconMenu = QtGui.QMenu(self)
        self.trayIconMenu.addAction(self.quitAction)

        # tray icon
        self.trayIcon = QtGui.QSystemTrayIcon(self)
        self.trayIcon.setContextMenu(self.trayIconMenu)
        icon = QtGui.QIcon(':/icon.png')

        self.trayIcon.setIcon(icon)
        self.trayIcon.setToolTip(tooltip)
        self.trayIcon.messageClicked.connect(self.messageClicked)
        self.trayIcon.show()

        # timer to check incoming messages
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.recvMessages)
        self.timer.start(1)

        self.zctx = zmq.Context()
        self.zsck = self.zctx.socket(zmq.PULL)
        self.zsck.bind(address)


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
        if api_msg.die:
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

        # save last recved Api message so that it can be used in
        # `messageClicked` handler
        self.api_msg = api_msg

        # if a message has extended info, it will be shown in a message box
        # provided the user clicks on the balloon message
        #
        # add a hint that the baloon message is clickable
        has_extended_info = api_msg.HasField('extended_info')
        body = api_msg.body
        if has_extended_info:
            body = body + '\n\nClick for detailed info'

        # display the balloon message in the system tray
        self.showTrayMessage(api_msg.title, body, icon)

    def messageClicked(self):
        """On click handler for the balloon message tooltip.

        If `extended_info` has not been set, does nothing.
        Otherwise, displays a message box containing title, body and extened
        info."""

        has_extended_info = self.api_msg.HasField('extended_info')
        if not has_extended_info:
            return

        title = self.api_msg.title
        body = self.api_msg.body + '\n\n' + self.api_msg.extended_info

        if self.api_msg.icon == Api.NO or self.api_msg.icon == Api.INFO:
            QtGui.QMessageBox.information(None, title, body)
        elif self.api_msg.icon == Api.WARN:
            QtGui.QMessageBox.warning(None, title, body)
        elif self.api_msg.icon == Api.CRIT:
            QtGui.QMessageBox.critical(None, title, body)

    def showTrayMessage(self, title, body, icon):
        self.trayIcon.showMessage(title, body, icon, 10)

def parse_cmdline_args():
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(description='Micro-service to display'
                                     ' user-friendly notifications using the '
                                     'system tray')
    parser.add_argument('--version', action='version',
                        version='%(prog)s {}'.format(__version__))

    parser.add_argument('-a', '--address', default='tcp://*:7272',
            help='endpoint address to listen to for incoming requests')
    parser.add_argument('-t', '--tooltip', default=CAPTION,
            help='tooltip text to display')
    return parser.parse_args()


def main():
    """Main here."""

    args = parse_cmdline_args()
    app = QtGui.QApplication(sys.argv)

    # test for systray functionality
    systray_ok = QtGui.QSystemTrayIcon.isSystemTrayAvailable() and QtGui.QSystemTrayIcon.supportsMessages()

    if not systray_ok:
        QtGui.QMessageBox.critical(None, CAPTION,
                """Could not start systray-notify because the system tray
                messages are not supported""")
        sys.exit(1)

    # must set this, otherwise, will close upon click on a message box ok
    # button (why so? dunno!)
    QtGui.QApplication.setQuitOnLastWindowClosed(False)

    window = Window(args.address, args.tooltip)
    sys.exit(app.exec_())

if __name__ == '__main__':
    sys.exit(main())
