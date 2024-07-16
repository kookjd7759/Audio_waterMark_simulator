import os
import sys
import numpy as np
import soundfile
import torch
import wavmark
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import VoiceRecording as mic
import WaterMark as wm

SOUNDFILE_GB_NAME = 'Sound file'
WATERMARK_GB_NAME = 'Watermark'
SOUNDPATH = ''

class MyWindow(QWidget):

    def update_soundPath(self, path):
        self.SOUNDPATH = path
        self.lbl_filePath.setText(self.SOUNDPATH)
        print(self.SOUNDPATH)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def __init__(self):
        super().__init__()
        self.init()
        
        self.lbl_filePath = self.findChildren(QGroupBox)[0].findChildren(QLineEdit)[0]
        self.lbl_insert_Result = self.findChildren(QGroupBox)[1].findChildren(QLineEdit)[0]
        self.lbl_extract_Result = self.findChildren(QGroupBox)[1].findChildren(QLineEdit)[1]
        
        self.model = wavmark.load_model().to(torch.device('cuda:0' if torch.cuda.is_available() else 'cpu'))

    def init(self):
        self.setWindowTitle('WaterMarking Simulator')
        self.setMaximumSize(700, 250)
        self.setMinimumSize(700, 250)
        self.center()

        grid = QGridLayout()
        grid.addWidget(self.createGroup_soundFile(), 0, 0)
        grid.addWidget(self.createGroup_waterMark(), 1, 0)
        self.setLayout(grid)



    def createGroup_soundFile(self):
            groupbox = QGroupBox(SOUNDFILE_GB_NAME)

            lbl_filepath = QLineEdit(self)
            lbl_filepath.setReadOnly(True)
            vbox = QVBoxLayout()
            vbox.addWidget(lbl_filepath)

            btn_selectFile = QPushButton('Import sound file', self)
            btn_selectFile.clicked.connect(self.btn_selectSoundFile_function)
            btn_record = QPushButton('New recording (3 sec)', self)
            btn_record.clicked.connect(self.btn_record_function)
            hbox = QHBoxLayout()
            hbox.addWidget(btn_selectFile)
            hbox.addWidget(btn_record)

            vbox.addLayout(hbox)

            groupbox.setLayout(vbox)
            return groupbox

    def createGroup_waterMark(self):
            groupbox = QGroupBox(WATERMARK_GB_NAME)

            grid = QGridLayout()

            lbl_insert = QLabel('[Insert]', self)
            btn_WMcreate_insert = QPushButton('Create And insert', self)
            btn_WMcreate_insert.clicked.connect(self.btn_WMcreate_insert_function)
            lbl_insert_Result = QLineEdit(self)
            lbl_insert_Result.setText('(None)')
            lbl_insert_Result.setReadOnly(True)
            
            lbl_extract = QLabel('[Extract]', self)
            btn_WMextract = QPushButton('Extract', self)
            lbl_extract_Result = QLineEdit(self)
            lbl_extract_Result.setText('(None)')
            lbl_extract_Result.setReadOnly(True)
            btn_WMextract.clicked.connect(self.btn_WMextract_function)

            grid.addWidget(lbl_insert, 0, 0)
            grid.addWidget(lbl_extract, 0, 1)
            grid.addWidget(btn_WMcreate_insert, 1, 0)
            grid.addWidget(btn_WMextract, 1, 1)
            grid.addWidget(lbl_insert_Result, 2, 0)
            grid.addWidget(lbl_extract_Result, 2, 1)

            groupbox.setLayout(grid)
            return groupbox



    def btn_selectSoundFile_function(self):
        fname = QFileDialog.getOpenFileName(self, '파일선택', '', 'AllFiles(*.*)')
        self.update_soundPath(fname[0])

    def btn_record_function(self):
        mic.recording(3)
        self.update_soundPath(mic.getRecordpath())
        
    def btn_WMcreate_insert_function(self):
        payload = wm.create()
        print(f'Payload: {payload}, size: {len(payload)}')
        print("SOUNDPATH: ", self.SOUNDPATH)

        signal, sample_rate = soundfile.read(self.SOUNDPATH)

        watermarked_signal, _ = wavmark.encode_watermark(self.model, signal, payload, show_progress=True)

        soundfile.write(self.SOUNDPATH, watermarked_signal, 16000)

        payload_txt = ''.join(str(x) for x in payload)
        self.lbl_insert_Result.setText(payload_txt)

    def btn_WMextract_function(self):
        signal, sample_rate = soundfile.read(self.SOUNDPATH)
        payload_decoded, _ = wavmark.decode_watermark(self.model, signal, show_progress=True)

        payload_list = payload_decoded.tolist()
        payload_txt = ''.join(str(x) for x in payload_list)
        print(payload_txt)
        self.lbl_extract_Result.setText(payload_txt)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())