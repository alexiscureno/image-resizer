from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QFileDialog, QLabel, QLineEdit, QMessageBox
from PyQt5.QtGui import QImage, QPixmap
from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtCore import QFileInfo
from PyQt5 import QtWidgets
import sys
import cv2


class Ui_res(QMainWindow):
    def __init__(self):
        super(Ui_res, self).__init__()
        uic.loadUi('img_res_01.ui', self)

        # Widgets
        self.label_img_original = self.findChild(QLabel, 'label_img_original')
        self.label_img_res = self.findChild(QLabel, 'label_img_res')

        self.label_img_height_res = self.findChild(QLabel, 'label_h_res')
        self.label_img_width_res = self.findChild(QLabel, 'label_w_res')
        self.label_num_height_orig = self.findChild(QLabel, 'label_h_o')
        self.label_num_width_orig = self.findChild(QLabel, 'label_w_o')

        self.open_button = self.findChild(QPushButton, 'pushButton_open')
        self.resize_button = self.findChild(QPushButton, 'pushButton_res')

        self.line_location = self.findChild(QLineEdit, 'lineEdit_open')
        self.line_height = self.findChild(QLineEdit, 'lineEdit_h_res')
        self.line_width = self.findChild(QLineEdit, 'lineEdit_w_res')

        # Clicked Buttons
        self.open_button.clicked.connect(self.open_img)
        self.resize_button.clicked.connect(self.res_img)
        self.show()

    def open_img(self):
        try:
            self.filepath = QFileDialog.getOpenFileName(self, 'Open Image', 'C:\\Users\\user\\Pictures',
                                                        'All files(*);;PNG(*.png);; JPEG(*.jpeg *.jpg)')
            self.location_orig = QFileInfo(self.filepath[0]).filePath()
            self.line_location.setText(self.location_orig)

            self.pixmap_original = QPixmap(self.filepath[0])
            self.pixmap_original = self.pixmap_original.scaled(601, 429, QtCore.Qt.KeepAspectRatio)
            self.label_img_original.setPixmap(self.pixmap_original)

            self.image_orig = cv2.imread(self.filepath[0], cv2.IMREAD_UNCHANGED)
            # setting labels of the image height and width
            self.label_num_height_orig.setText(f'{self.image_orig.shape[0]}')
            self.label_num_width_orig.setText(f'{self.image_orig.shape[1]}')

        except:
            self.error_name()

    def res_img(self):

        try:
            self.dim = int(self.line_width.text()), int(self.line_height.text())
            self.saving_path = QFileDialog.getSaveFileName(self, 'Save Image', '',
                                                                      "PNG(*.png);;;JPEG(*.jpeg *.jpg);;All Files(*.*) ")
            print(self.saving_path)
            self.location_res = QFileInfo(self.saving_path[0]).filePath()
            self.resized = cv2.resize(self.image_orig, self.dim)
            self.save_res = cv2.imwrite(self.saving_path[0], self.resized)
            print(self.location_res)
            self.saved_red = cv2.imread(self.location_res)

            self.label_img_height_res.setText(f'{self.saved_red.shape[0]}')
            self.label_img_width_res.setText(f'{self.saved_red.shape[1]}')

            self.pixmap_res = QPixmap(self.saving_path[0])
            self.pixmap_res = self.pixmap_res.scaled(601, 429, QtCore.Qt.KeepAspectRatio)
            self.label_img_res.setPixmap(self.pixmap_res)

            self.line_height.setText('')
            self.line_width.setText('')

        except ValueError:
            self.error_number()
            self.line_height.setText('')
            self.line_width.setText('')
        except:
            self.error_location()
            self.line_height.setText('')
            self.line_width.setText('')
        # self.name_res = QFileInfo(self.saving_path[0]).fileName()

    def error_location(self):
        msg = QMessageBox()
        msg.setWindowTitle('Location Error')
        msg.setText('Location not found')
        msg.setIcon(QMessageBox.Warning)
        x = msg.exec_()

    def error_name(self):
        msg = QMessageBox()
        msg.setWindowTitle('File not found Error')
        msg.setText('File not found')
        msg.setIcon(QMessageBox.Warning)
        x = msg.exec_()

    def error_number(self):
        msg = QMessageBox()
        msg.setWindowTitle('Value Error')
        msg.setText('Height and Width must be integer values')
        msg.setIcon(QMessageBox.Warning)
        x = msg.exec_()


app = QApplication(sys.argv)
UI_Window = Ui_res()
app.exec()
