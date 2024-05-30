# import .py
import client

# import package
import time
import sys
import os.path
# GUI 관련
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap, QPalette, QFont, QPainter, QImage
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5 import uic
# camera 관련
from picamera2 import Picamera2
from picamera2.previews.qt import QGlPicamera2

# Initialize the camera globally
picam2 = Picamera2()

# UI파일 연결
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path("summary.ui")
form_class = uic.loadUiType(form)[0]

# scan 페이지 수 전역변수
scan_cnt = 0


#화면을 띄우는데 사용되는 Class 선언
class MainWindow(QMainWindow, form_class) :

    # Main initial
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.initUI()

        # Start camera preview
        self.start_camera_preview()

    # AddUI initial
    def initUI(self):
        self.setWindowTitle('Summary King')
        icon_dir = resource_path("./.ico/icon.png")
        self.setWindowIcon(QIcon(icon_dir))
        self.initSTATUS()
        self.initMENU()
        self.initBTN()
        # self.initLOGO()

    # # Logo initial
    # def initLOGO(self):
    #     logo_dir = resource_path("./.ico/logo.png")
    #     logo = QPixmap(logo_dir)
    #     logo_img = logo.scaled(QSize(100, 100), aspectRatioMode=Qt.KeepAspectRatio)
    #     self.label_logo.setPixmap(logo_img)


    # StatusBar initial
    def initSTATUS(self):
        self.statusBar().showMessage('Ready')


    def initBTN(self):
        self.btn_scan.clicked.connect(lambda: self.initbtnscan())
        self.btn_summary.clicked.connect(lambda: self.initbtnssummary())
        self.btn_reset.clicked.connect(lambda: self.initbtnreset())


    # MenuBar initial
    def initMENU(self):
        # Menu Action initial
        exitAction = QAction('Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(lambda: self.close())

        abouttext = "This program is a hands-on program for 융종설 in the first semester of 2024 and was produced by Team SUMMARYKING.\n" \
                    "It cannot be copied or used without permission and requires the consent of the manufacturer.\n\n " \
                    "Powerd by 오픈 소스 소프트웨어 기반\n" \
                    " Copyright ⓒ 2024 Team SUMMARYKING"
        aboutAction = QAction('About', self)
        aboutAction.setShortcut('Ctrl+H')
        aboutAction.triggered.connect(lambda: QMessageBox.about(self, 'About', abouttext))

        settingAction = QAction('Settings', self)

        # Menu bar
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)

        filemenu = menubar.addMenu('&File')
        filemenu.addAction(settingAction)
        filemenu.addAction(exitAction)
        helpmenu = menubar.addMenu('&Help')
        helpmenu.addAction(aboutAction)

    # CameraPreview initial
    def start_camera_preview(self):
        # Adjust the preview size to match the sensor aspect ratio.
        preview_width = 481
        preview_height = 231
        # We also want a full FoV raw mode, this gives us the 2x2 binned mode.
        raw_size = tuple([v // 2 for v in picam2.camera_properties['PixelArraySize']])
        preview_config = picam2.create_preview_configuration({"size": (preview_width, preview_height)}, raw={"size": raw_size})
        picam2.configure(preview_config)

        # Create QGlPicamera2 widget for preview
        bg_colour = self.palette().color(QPalette.Background).getRgb()[:3]
        self.qpicamera2 = QGlPicamera2(picam2, width=preview_width, height=preview_height, bg_colour=bg_colour)
        self.qpicamera2.done_signal.connect(self.callback, type=QtCore.Qt.QueuedConnection)

        # Add preview widget to layout with specific position and size
        self.qpicamera2.setGeometry(QtCore.QRect(20, 20, preview_width, preview_height))
        self.qpicamera2.setObjectName("qpicamera2")
        self.previewLayout.addWidget(self.qpicamera2)

        # Start camera
        picam2.start()


    # camera capture 비동기 작동 위한 callback
    def callback(self, job):
        self.on_capture_complete()


    def capture_image(self):
        cfg = picam2.create_still_configuration()
        picam2.switch_mode_and_capture_file(cfg, "scan.jpg", signal_function=self.callback)


    def initbtnscan(self):
        # Handle capture completion
        self.capture_image()


    # capture_image, callback 메소드 실행 후 socket open, scan_cnt 1 증가
    def on_capture_complete(self):
        client.send_file()
        global scan_cnt
        scan_cnt += 1
        self.statusBar().showMessage(f'현재까지 스캔된 페이지: {scan_cnt} 장')


    def initbtnssummary(self):
        # response = server 에서 응답으로 받는 값
        response = ''
        response = client.send_summary_signal()
        self.label_summary.setFont(QFont('Arial', 12))
        self.label_summary.setText(str(response))

        self.statusBar().showMessage('요약 완료')
        global scan_cnt
        scan_cnt = 0


    def initbtnreset(self):
        client.send_delete_signal()
        self.label_summary.setText('')
        self.statusBar().showMessage('Ready')
        global scan_cnt
        scan_cnt = 0


    def closeEvent(self, event):
        # Handle close event
        reply = QMessageBox.question(self, 'Exit', 'Are you sure to exit?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


# Stop camera when application exits
picam2.stop()


