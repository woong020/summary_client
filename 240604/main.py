# Source import
import ui

# Pakage import
import sys
from PyQt5.QtWidgets import *
from gpiozero import Button


scan_button = Button(17)  # GPIO pin 17
summary_button = Button(22)  # GPIO pin 27
reset_button = Button(27)  # GPIO pin 22


# 스캔 버튼을 누르면 호출되는 함수
def scan_button_pressed():
    mainWindow.btn_scan.click()

# 요약 버튼을 누르면 호출되는 함수
def summary_button_pressed():
    mainWindow.btn_summary.click()

# 리셋 버튼을 누르면 호출되는 함수
def reset_button_pressed():
    mainWindow.btn_reset.click()



if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #인스턴스 생성
    mainWindow = ui.MainWindow()
    mainWindow.showMaximized()

    # 버튼에 기능 할당
    scan_button.when_pressed = scan_button_pressed
    summary_button.when_pressed = summary_button_pressed
    reset_button.when_pressed = reset_button_pressed


    # 프로그램 화면을 보여주는 코드
    # mainWindow.showMaximized()


    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()


