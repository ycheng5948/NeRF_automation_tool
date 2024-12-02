import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

# if __name__ == '__main__':
#     app = QApplication(sys.argv)

#     model = QDirModel()
#     tree = QTreeView()
#     tree.setModel(model)
#     tree.setWindowTitle("QTreeView")
#     tree.resize(640, 480)

#     tree.show()
#     sys.exit(app.exec_())


# class WindowA(QDialog):
#     def __init__(self, controller):
#         super(WindowA, self).__init__()
#         self.controller = controller
#         layout = QVBoxLayout()
#         self.button = QPushButton('Launch B')
#         self.button.clicked.connect(self.controller.launchB)
#         layout.addWidget(self.button)
#         self.setLayout(layout)
#         self.show()

######################################################################################3
# QTreeWidget Browse File
class FileBrowserWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.file_name_line_edit = QLineEdit()
        self.browse_button = QPushButton("Browse")
        self.button = QPushButton("Submit")
        self.button.clicked.connect(self.submit)
        self.folder_path = None

        layout = QVBoxLayout()
        layout.addWidget(self.file_name_line_edit)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.button)
        self.setLayout(layout)

        self.browse_button.clicked.connect(self.browse_file)

    # def browse_file(self):
    #     self.folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
    #     if self.folder_path:
    #         self.file_name_line_edit.setText(self.folder_path)
        
    def submit(self):
        if self.folder_path:
            print(self.folder_path)
        else:
            print("No folder selected")

    def browse_file(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg);;Videos (*.mp4 *.avi *.mov)")

        file_path, _ = file_dialog.getOpenFileName(self, "Select File or Folder")
        if file_path:
            self.line_edit.setText(file_path)

    # def browse_file(self):
    #     file_dialog = QFileDialog()
    #     file_dialog.setFileMode(QFileDialog.AnyFile)

    #     if file_dialog.exec_():
    #         selected_files = file_dialog.selectedFiles()
    #         if len(selected_files) > 0:
    #             file_path = selected_files[0]
    #             self.line_edit.setText(file_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileBrowserWindow()
    window.show()
    sys.exit(app.exec_())
######################################################################################
# combining input with ROOT path
# import os

# ROOT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
# SCRIPTS_FOLDER = os.path.join(ROOT_DIR, "scripts")

# class MyWidget(QWidget):
#     def __init__(self):
#         super().__init__()

#         self.line_edit = QLineEdit()
#         self.button = QPushButton("Submit")

#         layout = QVBoxLayout()
#         layout.addWidget(self.line_edit)
#         layout.addWidget(self.button)
#         self.setLayout(layout)

#         self.button.clicked.connect(self.handle_button_click)

#     def handle_button_click(self):
#         input_text = self.line_edit.text()
#         new_path = os.path.join(ROOT_DIR, "data", "nerf", input_text)
#         print(input_text)
#         print(new_path)

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MyWidget()
#     window.show()
#     sys.exit(app.exec_())
######################################################################################
# Input empty warning
# class MyWidget(QWidget):
#     def __init__(self):
#         super().__init__()

#         self.line_edit = QLineEdit()
#         self.button = QPushButton("Set")

#         layout = QVBoxLayout()
#         layout.addWidget(self.line_edit)
#         layout.addWidget(self.button)
#         self.setLayout(layout)

#         self.button.clicked.connect(self.handle_button_click)

#     def handle_button_click(self):
#         input_text = self.line_edit.text()
#         if input_text.strip() == "":
#             QMessageBox.warning(self, "Warning", "Input field cannot be empty.")
#         else:
#             # Your code to process the input text here
#             print("Input text:", input_text)

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MyWidget()
#     window.show()
#     sys.exit(app.exec_())