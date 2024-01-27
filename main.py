import os
import subprocess
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel, QPushButton


class DWGConverter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DWG to DXF Converter")
        self.setGeometry(300, 300, 400, 150)

        default_folder_file = "Default_Input_Folder.txt"
        if os.path.isfile(default_folder_file):
            with open(default_folder_file, "r") as file:
                self.folder_path = file.read().strip()
        else:
            self.folder_path = None

        self.lbl_instructions = QLabel("Select a folder containing DWG files:", self)
        self.lbl_instructions.setGeometry(20, 20, 360, 20)

        self.btn_select_folder = QPushButton("Select Folder", self)
        self.btn_select_folder.setGeometry(20, 50, 100, 30)
        self.btn_select_folder.clicked.connect(self.select_folder)

        self.lbl_selected_folder = QLabel("", self)
        self.lbl_selected_folder.setGeometry(130, 55, 250, 20)

        self.btn_convert = QPushButton("Convert to DXF", self)
        self.btn_convert.setGeometry(20, 90, 100, 30)
        self.btn_convert.clicked.connect(self.convert)

    def select_folder(self):
        folder_dialog = QFileDialog()
        folder_path = folder_dialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            self.folder_path = folder_path
            self.lbl_selected_folder.setText(self.folder_path)
            self.save_default_folder()

    def save_default_folder(self):
        default_folder_file = "Default_Input_Folder.txt"
        with open(default_folder_file, "w") as file:
            file.write(self.folder_path)

    def convert(self):
        if self.folder_path:
            os.makedirs(self.folder_path + r'\dxf', exist_ok=True)
            cmd = [
                r'ODA\ODAFileConverter 24.4.0\ODAFileConverter.exe',
                self.folder_path,
                self.folder_path + r'\dxf',
                "ACAD2018",
                "DXF",
                "0",
                "1",
                "*.DWG"
            ]
            subprocess.run(cmd, shell=True)
            self.lbl_selected_folder.setText("Conversion complete.")
        else:
            self.lbl_selected_folder.setText("Please select a folder.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    converter = DWGConverter()
    converter.show()
    sys.exit(app.exec())
