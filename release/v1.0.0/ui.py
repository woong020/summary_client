# import .py
import client

# import package
import time
import sys
import os.path
# GUI 관련
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap, QPalette, QFont, QPainter, QImage
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtGui import QOpenGLShader, QOpenGLShaderProgram, QOpenGLTexture
from PyQt5.QtCore import QSize, Qt, pyqtSignal, QThread, pyqtSlot, QMetaObject
# camera 관련
from picamera2 import Picamera2
from picamera2.previews.qt import QGlPicamera2

# Initialize picamera globally
picam2 = Picamera2()

# UI파일 연결
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path("summary.ui")
form_class = uic.loadUiType(form)[0]

# Worker thread for sending files
# Server 와 통신 및 StatusBar 에 표시를 위해 QThread 사용, 비동기 작업 수행
class Worker(QThread):
    finished = pyqtSignal(object)

    def __init__(self, send_func, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.send_func = send_func

    def run(self):
        result = self.send_func()
        self.finished.emit(result)


# 화면을 띄우는데 사용되는 Class 선언
class MainWindow(QMainWindow, form_class) :

    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.initUI()

        # 상태 변수 초기화 (프로그램 오동작 방지 변수)
        self.is_scan = False
        self.is_summary = False

        # Start camera preview
        self.start_camera_preview()

    # MainWindow 에 표시될 내용 및 객체 구현 메소드 호출
    def initUI(self):
        self.setWindowTitle('Summary King')
        icon_dir = resource_path("./.ico/icon.png")
        self.setWindowIcon(QIcon(icon_dir))
        self.initSTATUS()
        self.initMENU()
        self.initBTN()
        self.textEdit.clear()

    # Statusbar 초기값 적용
    def initSTATUS(self):
        self.statusBar().showMessage('================================== Ready ==================================')

    # PushButton 과 event 연결 구현부
    def initBTN(self):
        self.btn_scan.clicked.connect(self.handle_scan_button)
        self.btn_summary.clicked.connect(self.handle_summary_button)
        self.btn_reset.clicked.connect(self.handle_reset_button)

    # Menubar 내용 구현부
    def initMENU(self):
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

        # camera setting 관련 Modal 창 생성
        settingAction = QAction('Settings', self)

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)

        filemenu = menubar.addMenu('&File')
        filemenu.addAction(settingAction)
        filemenu.addAction(exitAction)
        helpmenu = menubar.addMenu('&Help')
        helpmenu.addAction(aboutAction)

        # 테스트 신호 전송 추가
        aboutAction.triggered.connect(self.handle_about_action)

    def handle_about_action(self):
        response = client.send_test_signal()
        print(response)  # 터미널에 출력


    # camera preview 구현부
    def start_camera_preview(self):
        preview_width = 379
        preview_height = 219

        raw_size = tuple([v // 2 for v in picam2.camera_properties['PixelArraySize']])
        preview_config = picam2.create_preview_configuration({"size": (preview_width, preview_height)}, raw={"size": raw_size})
        picam2.configure(preview_config)

        bg_colour = self.palette().color(QPalette.Background).getRgb()[:3]
        self.qpicamera2 = QGlPicamera2(picam2, width=preview_width, height=preview_height, bg_colour=bg_colour)
        self.qpicamera2.done_signal.connect(self.callback, type=QtCore.Qt.QueuedConnection)

        self.qpicamera2.setGeometry(QtCore.QRect(20, 20, preview_width, preview_height))
        self.qpicamera2.setObjectName("qpicamera2")
        # previewLayout(HBoxLayout) 객체에 picamera
        self.previewLayout.addWidget(self.qpicamera2)

        picam2.start()

    def callback(self, job):
        self.on_capture_complete()

    # picamera2 를 통한 현재 상태 still capture
    def capture_image(self):
        cfg = picam2.create_still_configuration()   # still capture 를 위한 설정 생성
        picam2.switch_mode_and_capture_file(cfg, "scan.jpg", signal_function=self.callback)
        # capture 후 line125 callback 호출 (

    # btn_scan 객체 클릭 시 호출
    def handle_scan_button(self):
        # if self.is_summary:
        #     QMessageBox.warning(self, 'Warning', 'Summary is in progress.')
        #     return

        # Disable buttons and update status bar
        self.set_controls_enabled(False)    # 버튼 비활성화
        self.statusBar().showMessage('============================================= 스캔 실행 중 =============================================')
        self.capture_image()    # line 128 captue_image 메소드 호출

    def on_capture_complete(self):
        scan_size = self.comboBox_size.currentText()    # combobox 현재 값 확인
        if scan_size == 'Size 1':
            send_file_func = client.send_file1
        elif scan_size == 'Size 2':
            send_file_func = client.send_file2
        elif scan_size == 'Size 3':
            send_file_func = client.send_file3
        else:
            self.set_controls_enabled(True) # 프로그램 오류 방지
            self.statusBar().showMessage('!!!!!!!!!!!!!!!!!!!!! 잘못된 크기 선택 !!!!!!!!!!!!!!!!!!!!!')
            return

        # Start worker thread to send file (on_scan_complete 실행)
        self.worker = Worker(send_file_func)
        self.worker.finished.connect(self.on_scan_complete)
        self.worker.start()

    def handle_summary_button(self):
        if not self.is_scan:
            self.show_warning('Scan is not complete.')
            return
        elif self.is_summary:
            self.show_warning('Summary already complete.')
            return


        # Disable buttons and update status bar
        self.set_controls_enabled(False)
        self.statusBar().showMessage('============================================= 요약 실행 중 =============================================')

        # Start worker thread to send summary signal
        self.worker = Worker(client.send_summary_signal)
        self.worker.finished.connect(self.on_summary_complete)
        self.worker.start()

    def handle_reset_button(self):
        if not self.is_scan and not self.is_summary:
            self.show_warning('No operation in progress to reset.')
            return


        self.set_controls_enabled(False)
        self.statusBar().showMessage('============================================= 초기화 실행 중 =============================================')

        client.send_delete_signal()
        self.textEdit.clear()
        self.is_scan = False
        self.is_summary = False
        self.statusBar().showMessage('================================== Ready ==================================')
        self.set_controls_enabled(True)

    # scan 완료 후 server 에서 'complete' 응답 시 스캔 완료 확인, 이외의 경우 버튼 활성화 및 스캔 실패 확인
    @pyqtSlot(object)
    def on_scan_complete(self, result):
        # Re-enable controls and update status bar based on success
        self.set_controls_enabled(True)
        if isinstance(result, str) and result == 'complete':
            self.is_scan = True
            self.statusBar().showMessage('============================================= 스캔 완료 =============================================')
        else:
            self.statusBar().showMessage('============================================= 스캔 실패 =============================================')

    # 요약 완료 후 server 에서 결과 응답 시 요약 완료 확인, 이외의 경우 버튼 활성화 및 스캔 실패 확인
    @pyqtSlot(object)
    def on_summary_complete(self, result):
        # Re-enable controls and update status bar based on success
        self.set_controls_enabled(True)
        if isinstance(result, str) and result:
            self.is_summary = True
            self.statusBar().showMessage('============================================= 요약 완료 =============================================')
            self.textEdit.setText(result)
        else:
            self.statusBar().showMessage('============================================= 요약 실패 =============================================')
            self.textEdit.clear()

    # 버튼 및 콤보박스 활성화 및 비활성화
    def set_controls_enabled(self, enabled):
        # Enable or disable buttons and combobox
        self.btn_scan.setEnabled(enabled)
        self.btn_summary.setEnabled(enabled)
        self.btn_reset.setEnabled(enabled)
        self.comboBox_size.setEnabled(enabled)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Exit', 'Are you sure to exit?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.cleanup()
            event.accept()
        else:
            event.ignore()

    # picamera preview 메모리 누수 방지 코드
    def cleanup(self):
        # Disconnect signals and stop camera preview
        if self.qpicamera2:
            self.qpicamera2.done_signal.disconnect(self.callback)
        if picam2:
            picam2.stop()

    # 예외처리를 포함한 경고 메시지 표시
    def show_warning(self, message):
        try:
            QMessageBox.warning(self, 'Warning', message, QMessageBox.Ok, QMessageBox.Ok)
        except Exception as e:
            print(f"Failed to show warning message: {e}")

picam2.stop()

