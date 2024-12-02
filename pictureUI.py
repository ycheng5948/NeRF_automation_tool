# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pictureUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import os
import shutil
from pathlib import Path
import json
import sys
import subprocess
from glob import glob
import re

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
SCRIPTS_FOLDER = os.path.join(ROOT_DIR, "scripts")

# project_name = input("Enter project name: ")
# PROJECT_FOLDER = os.path.join(ROOT_DIR, "data", "nerf", project_name)

# # check if project folder exists
# if not os.path.exists(PROJECT_FOLDER):
#     print("Project folder does not exist. Exiting...")
#     sys.exit(1)

# images_name = []
# images_folder = os.path.join(PROJECT_FOLDER, "images")
# images = os.listdir(images_folder)
# images_abs_path = [os.path.join(images_folder, i) for i in images]
# # add images to images_name list
# for i in images:
#     images_name.append(i)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.photo = QtWidgets.QLabel(self.centralwidget)
        self.photo.setGeometry(QtCore.QRect(30, 20, 271, 391))
        self.photo.setText("")

        # set up projrct name input and set button
        self.project_name_input = QtWidgets.QLineEdit(self.centralwidget)
        self.project_name_input.setGeometry(QtCore.QRect(350, 20, 271, 28))
        self.project_name_input.setObjectName("project_name")
        self.set = QtWidgets.QPushButton(self.centralwidget)
        self.set.setGeometry(QtCore.QRect(650, 20, 93, 28))
        self.set.setObjectName("set")

        # setup file browser
        self.file_name_line_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.file_name_line_edit.setGeometry(QtCore.QRect(350, 70, 271, 28))
        self.file_name_line_edit.setObjectName("file_name_line_edit")

        self.browse_button = QtWidgets.QPushButton(self.centralwidget)
        self.browse_button.setGeometry(QtCore.QRect(650, 70, 93, 28))
        self.browse_button.setObjectName("browse_button")

        # set up project name
        # self.project_name = None
        self.PROJECT_FOLDER = None
        self.images_name = []
        self.images_abs_path = []

        # set up image paths and the index
        self.image_paths = self.images_abs_path
        self.index = 0

        # self.photo.setPixmap(QtGui.QPixmap(self.images_abs_path[self.index]))
        self.photo.setPixmap(QtGui.QPixmap(''))
        self.photo.setScaledContents(True)
        self.photo.setObjectName("photo")
        self.previous = QtWidgets.QPushButton(self.centralwidget)
        self.previous.setGeometry(QtCore.QRect(30, 420, 93, 28))
        self.previous.setObjectName("previous")
        self.next = QtWidgets.QPushButton(self.centralwidget)
        self.next.setGeometry(QtCore.QRect(200, 420, 93, 28))
        self.next.setObjectName("next")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))

        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        
        self.statusbar = QtWidgets.QStatusBar(MainWindow)

        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # buttons functions
        # previous and next buttons
        self.previous.clicked.connect(self.show_previous)
        self.next.clicked.connect(self.show_next)
        # browse button
        self.browse_button.clicked.connect(self.browse_file)
        # set project name button
        self.set.clicked.connect(self.set_project)

# retranslateUi function
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.previous.setText(_translate("MainWindow", "Previous"))
        self.next.setText(_translate("MainWindow", "Next"))
        self.browse_button.setText(_translate("MainWindow", "Browse"))
        self.file_name_line_edit.setText(_translate("MainWindow", ""))
        self.set.setText(_translate("MainWindow", "Set"))

# show the previous image in the list when the previous button is clicked
    def show_previous(self):
        self.index = (self.index - 1) % len(self.images_abs_path)
        self.photo.setPixmap(QtGui.QPixmap(self.images_abs_path[self.index]))

    def show_next(self):
        self.index = (self.index + 1) % len(self.images_abs_path)
        self.photo.setPixmap(QtGui.QPixmap(self.images_abs_path[self.index]))

# browse file function
    def browse_file(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            self.file_name_line_edit.setText(folder_path)

# set up project name function and get images paths
    def set_project(self):
        self.project_name = self.project_name_input.text()

        if self.project_name:
            self.PROJECT_FOLDER = os.path.join(ROOT_DIR, "data", "nerf", self.project_name)
            print("project_name", self.project_name)
            print("folder path", self.PROJECT_FOLDER)

            # check if project folder exists
            if not os.path.exists(self.PROJECT_FOLDER):
                msg = QMessageBox()
                msg.setWindowTitle("Warning")
                msg.setText("Corresponding Project folder does not exist." + "\n" + "Please check project name")
                msg.setIcon(QMessageBox.Warning)
                msg.setDefaultButton(QMessageBox.Ok)
                x = msg.exec_()
            
            else:
                self.images_name = []
                self.images_folder = os.path.join(self.PROJECT_FOLDER, "images")
                if not os.path.exists(self.images_folder):
                    print('Running colmap2nerf.py to convert video into images...')
                    # get video absolute path
                    video = os.listdir(self.PROJECT_FOLDER)
                    video_abs_path = os.join(self.PROJECT_FOLDER, video)
                    os.system("colmap2nerf --video_in {0} --video_fps 2 --run_colmap".format(video_abs_path))
                else:
                    self.images = os.listdir(self.images_folder)
                    self.images_abs_path = [os.path.join(self.images_folder, i) for i in self.images]
                    # add images to images_name list
                    for i in self.images:
                        self.images_name.append(i)
                    
                    print("images_name", self.images_name)
                    self.photo.setPixmap(QtGui.QPixmap(self.images_abs_path[self.index]))

                    return self.images_abs_path
        
        if self.project_name.strip() == "":
            msg = QMessageBox()
            msg.setWindowTitle("Warning")
            msg.setText("Please set project name")
            msg.setIcon(QMessageBox.Warning)
            msg.setDefaultButton(QMessageBox.Ok)
            x = msg.exec_()

    def show_popup(self):
        msg = QMessageBox()
        msg.setWindowTitle("Tips")
        msg.setText("Please place the images based on the below structure")
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok|QMessageBox.Cancel|QMessageBox.Retry|QMessageBox.Ignore)
        msg.setDefaultButton(QMessageBox.Ok)

        msg.setInformativeText("Informative Text")
        msg.setDetailedText("|-Root-Folder" + "\n" +
                                "|  |-instant-ngp.exe" + "\n" +
                                "|  |-Scripts" + "\n" +
                                "|  |  |-nerf-automation.py" + "\n" +
                                "|  |  |-colmap2nerf.py" + "\n" +
                                "|  |  |-..." + "\n" +
                                "|  |"  + "\n" +
                                "|  |-data" + "\n" +
                                "|    |-nerf" + "\n" +
                                "|     |-transformed.json" + "\n" +
                                "|     |-Images" + "\n" +
                                "|       |-0001.jpg" + "\n" +
                                "|       |-0002.jpg" + "\n" +
                                "|       |-0003.jpg" + "\n" +
                                "|       |-...")
        msg.buttonClicked.connect(self.popup_button)
        x = msg.exec_()
    
    def popup_button(self, i):
        print(i.text())

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())