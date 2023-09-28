from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
import cv2
import pandas as pd
from datetime import datetime
import os
import numpy as np
from PIL import Image

class Ui_mainWindow(object):
    def openEnroll(self):
        self.window = QtWidgets.QFrame()
        self.ui = Ui_enrollWindow()
        self.ui.setupUi(self.window)
        self.window.show()

    def openDetail(self):
        self.window = QtWidgets.QFrame()
        self.ui = Ui_detailWindow()
        self.ui.setupUi(self.window)
        self.window.show()

    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(480, 800)
        self.attendButton = QtWidgets.QPushButton(mainWindow)
        self.attendButton.setGeometry(QtCore.QRect(60, 410, 361, 71))
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.attendButton.setFont(font)
        self.attendButton.setObjectName("attendButton")
        self.attendButton.clicked.connect(self.openDetail)
        self.attendButton.clicked.connect(mainWindow.close)

        self.enrollButton = QtWidgets.QPushButton(mainWindow)
        self.enrollButton.setGeometry(QtCore.QRect(60, 300, 361, 71))
        self.enrollButton.setFont(font)
        self.enrollButton.setObjectName("enrollButton")
        self.enrollButton.clicked.connect(self.openEnroll)
        self.enrollButton.clicked.connect(mainWindow.close)

        self.logo = QtWidgets.QLabel(mainWindow)
        self.logo.setEnabled(True)
        self.logo.setGeometry(QtCore.QRect(145, 140, 191, 111))
        title = QtGui.QFont()
        title.setPointSize(60)
        self.logo.setFont(title)
        self.logo.setObjectName("logo")
        self.quitButton = QtWidgets.QPushButton(mainWindow)
        self.quitButton.setGeometry(QtCore.QRect(60, 520, 361, 71))
        self.quitButton.setFont(font)
        self.quitButton.setObjectName("quitButton")
        self.quitButton.clicked.connect(mainWindow.close)

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "Frame"))
        self.attendButton.setText(_translate("mainWindow", "Take Attendance"))
        self.enrollButton.setText(_translate("mainWindow", "Enroll"))
        self.logo.setText(_translate("mainWindow", "AMS"))
        self.quitButton.setText(_translate("mainWindow", "Quit"))

class Ui_enrollWindow(object):
    def openMain(self):
        self.window = QtWidgets.QFrame()
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self.window)
        self.window.show()
        self.video_capture.release()
        self.timer.stop()

    def update_frame(self):
        ret, frame = self.video_capture.read()
        self.frame = frame
        if ret:
            frame = cv2.flip(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), 1)
            image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            self.liveCam.setPixmap(QPixmap.fromImage(image))

    def setupUi(self, enrollWindow):
        enrollWindow.setObjectName("enrollWindow")
        enrollWindow.resize(480, 800)
        self.enrollButton = QtWidgets.QPushButton(enrollWindow)
        self.enrollButton.setGeometry(QtCore.QRect(250, 710, 211, 71))
        self.font = QtGui.QFont()
        self.font.setFamily("Courier New")
        self.font.setPointSize(16)
        self.font.setBold(True)
        self.font.setWeight(75)
        self.enrollButton.setFont(self.font)
        self.enrollButton.setObjectName("startButton")
        self.enrollButton.clicked.connect(self.enrollFace)

        self.backButton = QtWidgets.QPushButton(enrollWindow)
        self.backButton.setGeometry(QtCore.QRect(20, 710, 211, 71))
        self.backButton.setFont(self.font)
        self.backButton.setObjectName("backButton")
        self.backButton.clicked.connect(self.openMain)
        self.backButton.clicked.connect(enrollWindow.close)

        self.mid = QtWidgets.QLabel(enrollWindow)
        self.mid.setGeometry(QtCore.QRect(50, 60, 101, 41))
        self.mid.setFont(self.font)
        self.mid.setObjectName("mid")

        self.midLine = QtWidgets.QLineEdit(enrollWindow)
        self.midLine.setGeometry(QtCore.QRect(190, 60, 241, 41))
        self.midLine.setFont(self.font)
        self.midLine.setObjectName("midLine")

        self.liveCam = QtWidgets.QLabel(enrollWindow)
        self.liveCam.setGeometry(QtCore.QRect(50, 140, 381, 381))
        self.liveCam.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.liveCam.setText("")
        self.liveCam.setObjectName("liveCam")
        self.infoLine = QtWidgets.QLabel(enrollWindow)
        self.infoLine.setGeometry(QtCore.QRect(50, 540, 381, 71))

        self.infoLine.setFont(self.font)
        self.infoLine.setObjectName("infoLine")

        self.result = QtWidgets.QLabel(enrollWindow)
        self.result.setGeometry(QtCore.QRect(145, 640, 191, 31))
        self.result.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.result.setText("")
        self.result.setObjectName("result")

        self.retranslateUi(enrollWindow)
        QtCore.QMetaObject.connectSlotsByName(enrollWindow)

    def retranslateUi(self, enrollWindow):
        _translate = QtCore.QCoreApplication.translate
        enrollWindow.setWindowTitle(_translate("enrollWindow", "Frame"))
        self.enrollButton.setText(_translate("enrollWindow", "Enroll"))
        self.backButton.setText(_translate("enrollWindow", "Back"))
        self.mid.setText(_translate("enrollWindow", "MID  :"))
        self.infoLine.setText(_translate("enrollWindow", "Press enroll button to \nstore your photo in DB"))

    def resetLabel(self):
        self.result.setText('')

    def enrollFace(self):
        try:
            mid = int(self.midLine.text())
            face_cascade = cv2.CascadeClassifier('C:/Users/Mi Notebook/Desktop/AMS/haarcascade_frontalface_alt2.xml')
            self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            face = face_cascade.detectMultiScale(self.frame, 1.1, 4)
            for (x, y, w, h) in face:
                face = self.frame[y:y + h, x:x + w] 
            face = cv2.equalizeHist(face)
            face = cv2.resize(face, (640, 640))
            cv2.imwrite("C:/Users/Mi Notebook/Desktop/AMS/Students/" + str(mid) + ".jpg", face)
            palette = QtGui.QPalette()
            brush = QtGui.QBrush(QtGui.QColor(0, 255, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
            self.result.setFont(self.font)
            self.result.setPalette(palette)
            self.result.setText("Successful !")
            self.delay = QTimer()
            self.delay.start(1500)
            self.delay.timeout.connect(self.resetLabel)

        except ValueError:
            palette = QtGui.QPalette()
            brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
            self.result.setFont(self.font)
            self.result.setPalette(palette)
            self.result.setText("  Failed !")
            self.delay = QTimer()
            self.delay.start(1500)
            self.delay.timeout.connect(self.resetLabel)
        except cv2.error:
            palette = QtGui.QPalette()
            brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
            self.result.setFont(self.font)
            self.result.setPalette(palette)
            self.result.setText("  Failed !")
            self.delay = QTimer()
            self.delay.start(1500)
            self.delay.timeout.connect(self.resetLabel)

    def __init__(self):
        super().__init__()
        self.video_capture = cv2.VideoCapture(0)
        self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 400)
        self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 420)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

class Ui_detailWindow(object):
    def openAttend(self):
        self.window = QtWidgets.QFrame()
        self.ui = Ui_attendWindow()
        self.ui.setupUi(self.window)
        self.window.show()
    
    def openMain(self):
        self.window = QtWidgets.QFrame()
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self.window)
        self.window.show()
    
    def getDetail(self):
        sub = self.subMenu.currentText().replace(' ','')
        time = self.timeMenu.currentText().replace(' ','')
        day = str(datetime.now().day)
        month = str(datetime.now().month)
        match month:
            case '1':
                month = 'Jan'
            case '2':
                month = 'Feb'
            case '3':
                month = 'Mar'
            case '4':
                month = 'Apr'
            case '5':
                month = 'May'
            case '6':
                month = 'Jun'
            case '7':
                month = 'Jul'
            case '8':
                month = 'Aug'
            case '9':
                month = 'Sep'
            case '10':
                month = 'Oct'
            case '11':
                month = 'Nov'
            case '12':
                month = 'Dec'
        date = day +'-'+ month
        col = date +' '+ time
        path = 'C:/Users/Mi Notebook/Desktop/AMS/Attendance/' + sub + '.xlsx'
        df = pd.read_csv('C:/Users/Mi Notebook/Desktop/AMS/Shared/tableData.csv')
        df.iloc[0, 0] = sub
        df.iloc[0, 1] = path
        df.iloc[0, 2] = col
        df.to_csv('C:/Users/Mi Notebook/Desktop/AMS/Shared/tableData.csv',index=False)

    def setupUi(self, detailWindow):
        detailWindow.setObjectName("detailWindow")
        detailWindow.resize(480, 800)
        self.subMenu = QtWidgets.QComboBox(detailWindow)
        self.subMenu.setGeometry(QtCore.QRect(190, 270, 241, 51))
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.subMenu.setFont(font)
        self.subMenu.setObjectName("subMenu")
        self.subMenu.addItem("")
        self.subMenu.addItem("")
        self.subMenu.addItem("")
        self.subMenu.addItem("")
        self.subMenu.addItem("")
        self.subLine = QtWidgets.QLabel(detailWindow)
        self.subLine.setGeometry(QtCore.QRect(50, 280, 101, 31))
        self.subLine.setFont(font)
        self.subLine.setObjectName("subLine")
        self.timeLine = QtWidgets.QLabel(detailWindow)
        self.timeLine.setGeometry(QtCore.QRect(50, 370, 101, 31))
        self.timeLine.setFont(font)
        self.timeLine.setObjectName("timeLine")
        self.timeMenu = QtWidgets.QComboBox(detailWindow)
        self.timeMenu.setGeometry(QtCore.QRect(190, 360, 241, 51))
        self.timeMenu.setFont(font)
        self.timeMenu.setObjectName("timeMenu")
        self.timeMenu.addItem("")
        self.timeMenu.addItem("")
        self.timeMenu.addItem("")
        self.timeMenu.addItem("")
        self.titleLine = QtWidgets.QLabel(detailWindow)
        self.titleLine.setGeometry(QtCore.QRect(50, 160, 341, 61))
        self.titleLine.setFont(font)
        self.titleLine.setObjectName("titleLine")
        self.backButton = QtWidgets.QPushButton(detailWindow)
        self.backButton.setGeometry(QtCore.QRect(20, 710, 211, 71))
        self.backButton.setFont(font)
        self.backButton.setObjectName("backButton")
        self.backButton.clicked.connect(self.openMain)
        self.backButton.clicked.connect(detailWindow.close)

        self.doneButton = QtWidgets.QPushButton(detailWindow)
        self.doneButton.setGeometry(QtCore.QRect(250, 710, 211, 71))
        self.doneButton.setFont(font)
        self.doneButton.setObjectName("doneButton")
        self.doneButton.clicked.connect(self.getDetail)
        self.doneButton.clicked.connect(self.openAttend)
        self.doneButton.clicked.connect(detailWindow.close)
        self.retranslateUi(detailWindow)
        QtCore.QMetaObject.connectSlotsByName(detailWindow)

    def retranslateUi(self, detailWindow):
        _translate = QtCore.QCoreApplication.translate
        detailWindow.setWindowTitle(_translate("detailWindow", "Frame"))
        self.subMenu.setItemText(0, _translate("detailWindow", " ME"))
        self.subMenu.setItemText(1, _translate("detailWindow", " MCS"))
        self.subMenu.setItemText(2, _translate("detailWindow", " ICE"))
        self.subMenu.setItemText(3, _translate("detailWindow", " CCS"))
        self.subMenu.setItemText(4, _translate("detailWindow", " MIS"))
        self.subLine.setText(_translate("detailWindow", "Sub  :"))
        self.timeLine.setText(_translate("detailWindow", "Time : "))
        self.timeMenu.setItemText(0, _translate("detailWindow", " 11:00"))
        self.timeMenu.setItemText(1, _translate("detailWindow", " 11:55"))
        self.timeMenu.setItemText(2, _translate("detailWindow", " 1:20"))
        self.timeMenu.setItemText(3, _translate("detailWindow", " 2:15"))
        self.titleLine.setText(_translate("detailWindow", "Select from drop down \nmenu"))
        self.backButton.setText(_translate("detailWindow", "Back"))
        self.doneButton.setText(_translate("detailWindow", "Done"))

class Ui_authWindow(object):
    def openAttend(self):
        self.window = QtWidgets.QFrame()
        self.ui = Ui_attendWindow()
        self.ui.setupUi(self.window)
        self.window.show()

    def openMain(self):
        self.window = QtWidgets.QFrame()
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self.window)
        self.window.show()

    def setupUi(self, authWindow):
        self.authWindow = authWindow
        authWindow.setObjectName("authWindow")
        authWindow.resize(480, 800)
        self.backButton = QtWidgets.QPushButton(authWindow)
        self.backButton.setGeometry(QtCore.QRect(20, 710, 211, 71))
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.backButton.setFont(font)
        self.backButton.setObjectName("backButton")
        self.backButton.clicked.connect(self.openAttend)
        self.backButton.clicked.connect(authWindow.close)

        self.doneButton = QtWidgets.QPushButton(authWindow)
        self.doneButton.setGeometry(QtCore.QRect(250, 710, 211, 71))
        self.doneButton.setFont(font)
        self.doneButton.setObjectName("doneButton")
        self.font = font

        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        self.palette = palette

        self.label_1 = QtWidgets.QLabel(authWindow)
        self.label_1.setGeometry(QtCore.QRect(55, 240, 371, 51))
        self.label_1.setFont(font)
        self.label_1.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(authWindow)
        self.label_2.setGeometry(QtCore.QRect(50, 320, 101, 41))
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_3")
        self.keyLine = QtWidgets.QLineEdit(authWindow)
        self.keyLine.setGeometry(QtCore.QRect(150, 320, 281, 41))
        self.keyLine.setObjectName("keyLine")
        self.keyLine.setFont(font)
        self.result = QtWidgets.QLabel(authWindow)
        self.result.setGeometry(QtCore.QRect(160, 400, 171, 41))
        self.result.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.result.setText("")
        self.result.setObjectName("result")

        self.retranslateUi(authWindow)
        QtCore.QMetaObject.connectSlotsByName(authWindow)
        self.doneButton.clicked.connect(self.storeAuth)
    
    def resetLabel(self):
        self.result.setText('')

    def storeAuth(self):
        if self.keyLine.text() == '12345':
            self.openMain()
            self.authWindow.close()
        else:
            self.result.setFont(self.font)
            self.result.setPalette(self.palette)
            self.result.setText("Wrong key!")
            self.delay = QTimer()
            self.delay.start(1500)
            self.delay.timeout.connect(self.resetLabel)


    def retranslateUi(self, authWindow):
        _translate = QtCore.QCoreApplication.translate
        authWindow.setWindowTitle(_translate("authWindow", "Frame"))
        self.backButton.setText(_translate("authWindow", "Back"))
        self.doneButton.setText(_translate("authWindow", "Done"))
        self.label_1.setText(_translate("authWindow", "Authentication Required"))
        self.label_2.setText(_translate("authWindow", "Key :"))

class Ui_attendWindow(object):
    def openAuth(self):
        self.window = QtWidgets.QFrame()
        self.ui = Ui_authWindow()
        self.ui.setupUi(self.window)
        self.window.show()
        self.video_capture.release()
        self.timer.stop()

    def setupUi(self, attendWindow):
        attendWindow.setObjectName("attendWindow")
        attendWindow.resize(480, 800)
        self.font = QtGui.QFont()
        self.font.setFamily("Courier New")
        self.font.setPointSize(16)
        self.font.setBold(True)
        self.font.setWeight(75)
        attendWindow.setFont(self.font)
        self.label = QtWidgets.QLabel(attendWindow)
        self.label.setGeometry(QtCore.QRect(40, 60, 401, 71))

        self.label.setFont(self.font)
        self.label.setObjectName("label")
        self.liveCam = QtWidgets.QLabel(attendWindow)
        self.liveCam.setGeometry(QtCore.QRect(40, 150, 401, 401))
        self.liveCam.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.liveCam.setText("")
        self.liveCam.setObjectName("liveCam")
        self.result = QtWidgets.QLabel(attendWindow)
        self.result.setGeometry(QtCore.QRect(85, 580, 311, 91))
        self.result.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.result.setText("")
        self.result.setObjectName("result")

        self.verifyButton = QtWidgets.QPushButton(attendWindow)
        self.verifyButton.setGeometry(QtCore.QRect(250, 710, 211, 71))
        self.verifyButton.setFont(self.font)
        self.verifyButton.setObjectName("backButton")
        self.verifyButton.clicked.connect(self.verifyFace)

        self.quitButton = QtWidgets.QPushButton(attendWindow)
        self.quitButton.setGeometry(QtCore.QRect(20, 710, 211, 71))
        self.quitButton.setFont(self.font)
        self.quitButton.setObjectName("quitButton")
        self.quitButton.clicked.connect(self.openAuth)
        self.quitButton.clicked.connect(attendWindow.close)

        self.retranslateUi(attendWindow)
        QtCore.QMetaObject.connectSlotsByName(attendWindow)

    def retranslateUi(self, attendWindow):
        _translate = QtCore.QCoreApplication.translate
        attendWindow.setWindowTitle(_translate("attendWindow", "Frame"))
        self.label.setText(_translate("attendWindow", "Show your face and press \nverify"))
        self.quitButton.setText(_translate("attendWindow", "Quit"))
        self.verifyButton.setText(_translate("attendWindow", "Verify"))
    
    def resetLabel(self):
        self.result.setText('')

    def __init__(self):
        super().__init__()
        self.video_capture = cv2.VideoCapture(0)
        self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 400)
        self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 420)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)
        df = pd.read_csv('C:/Users/Mi Notebook/Desktop/AMS/Shared/tableData.csv')
        sub = df.iloc[0, 0]
        path = df.iloc[0, 1]
        col = df.iloc[0, 2]
        df = pd.read_excel(path)
        df.set_index('MID', drop=False, inplace=True)
        df.loc[:, col] = 0
        df.loc['Total lec', col] = 1
        df.to_excel(path,index=False)

    def update_frame(self):
        ret, frame = self.video_capture.read()
        self.frame = frame
        if ret:
            frame = cv2.flip(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), 1)
            image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            self.liveCam.setPixmap(QPixmap.fromImage(image))

    def verifyFace(self):
        try:
            train_folder = 'C:/Users/Mi Notebook/Desktop/AMS/Students/'
            test_file = 'C:/Users/Mi Notebook/Desktop/AMS/Temp/temp.jpg'
            face_cascade = cv2.CascadeClassifier('C:/Users/Mi Notebook/Desktop/AMS/haarcascade_frontalface_alt2.xml')
            faces = []
            uids = []
            for file in os.listdir(train_folder):
                path = train_folder + file
                uid = int(file.strip('.jpg'))
                img = Image.open(path).convert('L')
                img_np = np.array(img, 'uint8')
                faces.append(img_np)
                uids.append(uid)
            
            self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            face = face_cascade.detectMultiScale(self.frame, 1.1, 4)
            for (x, y, w, h) in face:
                face = self.frame[y:y + h, x:x + w] 
            face = cv2.equalizeHist(face)
            face = cv2.resize(face, (640, 640))
            cv2.imwrite(test_file, face)
            model = cv2.face.LBPHFaceRecognizer_create()
            model.train(faces, np.array(uids))
            test_img = Image.open(test_file).convert('L')
            test_np = np.array(test_img, 'uint8')
            prediction = model.predict(test_np)

            palette = QtGui.QPalette()
            brush = QtGui.QBrush(QtGui.QColor(0, 255, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
            self.result.setFont(self.font)
            self.result.setPalette(palette)
            self.result.setText("Successfully marked \n" + "     " + str(prediction[0]) + ' !')
            self.delay = QTimer()
            self.delay.start(1500)
            self.delay.timeout.connect(self.resetLabel)
            df = pd.read_csv('C:/Users/Mi Notebook/Desktop/AMS/Shared/tableData.csv')
            sub = df.iloc[0, 0]
            path = df.iloc[0, 1]
            col = df.iloc[0, 2]
            df = pd.read_excel(path)
            df.set_index('MID', drop=False, inplace=True)
            for mid in df['MID']:
                if str(prediction[0]) == str(mid):
                    df.loc[mid, col] = 1
            df.to_excel(path,index=False)
        except cv2.error:
            palette = QtGui.QPalette()
            brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
            self.result.setFont(self.font)
            self.result.setPalette(palette)
            self.result.setText("  Failed to mark !")
            self.delay = QTimer()
            self.delay.start(1500)
            self.delay.timeout.connect(self.resetLabel)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QFrame()
    ui = Ui_mainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
