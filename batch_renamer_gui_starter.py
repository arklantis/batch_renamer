import sys
import os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
# You'll need to make this ui in QtDesigner
# And convert it to a .py file using the MakeUIPy.bat file
from batch_renamer_ui import Ui_MainWindow 
# Recommend you rename this
import batch_renamer_lib




class BatchRenamerWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        # UI Setup
        super().__init__()
        super(Ui_MainWindow).__init__()
        self.setupUi(self)
        # Connect button to function
        self.pushButtonBrowse.clicked.connect(self.get_filepath)
        # Connect your new "Run" button to self.run_renamer
        self.pushButtonRun.clicked.connect(self.run_renamer)
        # Copy or rename check
        self.radioButtonRename.toggled.connect(self.get_mode)
        # Instance the "back end"
        self.batch_renamer = batch_renamer_lib.BatchRenamer()
        
        # Show UI normal vs maximized
        self.showNormal()

    def get_filepath(self):
        """
        Open a file dialog for browsing to a folder
        """
        self.folder_check = QFileDialog().getExistingDirectory()
        # check tuple or not
        if isinstance(self.folder_check, tuple):
            self.folder_check = self.folder_check[0]
        # check user select folder or canel 
        if self.folder_check: 
            self.filepath = self.folder_check
            self.filepathEdit.setText(self.filepath)
            self.set_filepath()
        else:
            self.filepathEdit.clear()
            self.listWidget.clear()
            
    def set_filepath(self):
        """
        Set lineEdit text for filepath
        """
        self.filepathEdit.setText(self.filepath)
        self.update_list()

    def update_list(self):
        """
        Clear listwidget
        read files in filepath with os.walk
        Add files as new items
        """
        self.listWidget.clear()
        for root, dirs, files in os.walk(self.filepath):
            self.listWidget.addItems(files)
        self.listWidget.itemSelectionChanged.connect(self.get_file_data)
    
    def get_file_data(self):
        # clear line edit
        self.findStringEdit.setText('') 
        self.ExtTypeEdit.setText('')

        # get file name and extension 
        self.selected_items = self.listWidget.selectedItems() 
        # selet list item
        if self.selected_items:
            self.full_filename = self.selected_items[0].text()
            self.filename, self.extension = os.path.splitext(self.full_filename)
            # set name and extension in line edit
            self.findStringEdit.setText(self.filename)  
            self.ExtTypeEdit.setText(self.extension)
    
    # Add a function to gather and set parameters based upon UI
    # e.g. lineEdit.text() or radioButton.isChecked
    # remember that you may need to check to see if the result
    # was a tuple and correct like so:
    # self.filepath = self.filepathEdit.text()
    # if type(self.filepath) is tuple:
    #     self.filepath = self.filepath[0]

    # check copy or rename
    def get_mode(self):
        if self.radioButtonRename.isChecked():
            return False
        elif self.radioButtonCopy.isChecked():
            return True
        
    def run_renamer(self):
        
        # check already selet the folder
        if not hasattr(self, 'filepath') or not self.filepath:
            QMessageBox.warning(self, "Warning", "No folder selected.")
            return
        # check already selet the file to run
        if not self.listWidget.selectedItems():
            QMessageBox.warning(self, "Warning", "No file selected.")
            return
        # get original fil name
        old_name = f"{self.filename}{self.extension}"
        # get prefix / suffix / extension
        self.prefix = self.prefixEdit.text()
        self.suffix = self.suffixEdit.text()
        self.file_type = self.ExtTypeEdit.text()
        # in case no text input to rename 
        if self.replaceStringEdit.text().strip() == "":
           self.edit_name = self.findStringEdit.text()
        else:
           self.edit_name = self.replaceStringEdit.text()
        
        # in case no text input in prefix or suffix
        empty_prefix = not self.prefixEdit.text().strip()
        empty_suffix = not self.suffixEdit.text().strip()
        if empty_prefix and empty_suffix:
            new_name = f"{self.edit_name}{self.file_type}"
        elif empty_prefix:
            new_name = f"{self.edit_name}_{self.suffix}{self.file_type}"
        elif empty_suffix:
            new_name = f"{self.prefix}_{self.edit_name}{self.file_type}"
        else:
            new_name = f"{self.prefix}_{self.edit_name}_{self.suffix}{self.file_type}"
        # in case copy same name error
        if self.get_mode() and new_name == old_name:
           QMessageBox.warning(self, "Warning", "File name exists. Cannot copy.")
           return
           # self.labelResult.setText('Cant copy the file with the same name')
        # rename or copy fuction
        existing_path = os.path.join(self.filepath, self.full_filename)
        new_path = os.path.join(self.filepath, new_name)

        if self.batch_renamer.rename_file(existing_path, new_path, 
                                          self.get_mode()):
           # clear select item and update the list
           self.update_list()
           self.listWidget.clearSelection()
           # get rename or copy result message
           if self.get_mode():
              tip_text = f"Success copy file: {old_name} to {new_name}"
           else:
              tip_text = f"Success rename file: {old_name} to {new_name}"
           self.labelResult.setText(tip_text)           
        
        """
        Run back end batch renamer using self.batch_renamer
        self.batch_renamer is an instance of the BatchRenamer class
        """
        #pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BatchRenamerWindow()
    sys.exit(app.exec())
 