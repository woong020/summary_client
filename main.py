# Source import
import ui

# Pakage import
import sys
from PyQt5.QtWidgets import *



if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #인스턴스 생성
    mainWindow = ui.MainWindow()

    # 프로그램 화면을 보여주는 코드
    mainWindow.showMaximized()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()


