# # import .py
# import ui
#
# # import package
# import sys
# from PyQt5.QtWidgets import *
# # from qasync import QEventLoop, asyncSlot
# from gpiozero import Button
#
# # GPIO Pin 번호 할당
# scan_button = Button(17)  # GPIO pin 17
# summary_button = Button(27)  # GPIO pin 27
# reset_button = Button(22)  # GPIO pin 22
#
# # 스캔 버튼을 누르면 호출되는 함수
# def scan_button_pressed():
#     mainWindow.btn_scan.click()
#
# # 요약 버튼을 누르면 호출되는 함수
# def summary_button_pressed():
#     mainWindow.btn_summary.click()
#
# # 리셋 버튼을 누르면 호출되는 함수
# def reset_button_pressed():
#     mainWindow.btn_reset.click()
#
#
# if __name__ == "__main__":
#     # QApplication : 프로그램을 실행시켜주는 클래스
#     app = QApplication(sys.argv)
#
#     # 인스턴스 생성 및 최대화
#     mainWindow = ui.MainWindow()
#     mainWindow.showMaximized()
#
#     # GPIO 버튼에 기능 할당
#     scan_button.when_pressed = scan_button_pressed
#     summary_button.when_pressed = summary_button_pressed
#     reset_button.when_pressed = reset_button_pressed
#
#     # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
#     app.exec_()

import ui
import sys
from PyQt5.QtWidgets import *
from gpiozero import Button
import threading
import time

# GPIO Pin 번호 할당
scan_button = Button(17)  # GPIO pin 17
summary_button = Button(27)  # GPIO pin 27
reset_button = Button(22)  # GPIO pin 22

# 버튼 활성화 여부를 저장하는 딕셔너리
button_enabled = {
    scan_button: True,
    summary_button: True,
    reset_button: True
}

# 스캔 버튼을 누르면 호출되는 함수
def scan_button_pressed():
    if button_enabled[scan_button]:
        mainWindow.btn_scan.click()
        disable_button(scan_button)

# 요약 버튼을 누르면 호출되는 함수
def summary_button_pressed():
    if button_enabled[summary_button]:
        mainWindow.btn_summary.click()
        disable_button(summary_button)

# 리셋 버튼을 누르면 호출되는 함수
def reset_button_pressed():
    if button_enabled[reset_button]:
        mainWindow.btn_reset.click()
        disable_button(reset_button)

# 버튼을 비활성화하는 함수
def disable_button(button):
    button_enabled[button] = False
    threading.Thread(target=enable_button_after_delay, args=(button,)).start()

# 일정 시간이 지난 후 버튼을 다시 활성화하는 함수
def enable_button_after_delay(button):
    time.sleep(3)  # 3초 지연
    button_enabled[button] = True

if __name__ == "__main__":
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    # 인스턴스 생성 및 최대화
    mainWindow = ui.MainWindow()
    mainWindow.showMaximized()

    # GPIO 버튼에 기능 할당
    scan_button.when_pressed = scan_button_pressed
    summary_button.when_pressed = summary_button_pressed
    reset_button.when_pressed = reset_button_pressed

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()