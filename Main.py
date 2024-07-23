import os
import sys
import time
import numpy as np
import soundfile
import Path
import torch
import wavmark
import threading
from datetime import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import Audio as audio
import WaterMark as wm

SOUNDFILE_GB_NAME = 'Sound file'
WATERMARK_GB_NAME = 'Watermark'
REALTIMESETTING_GB_NAME = 'Real Time Simulation (Setting)'
REALTIMEEXCUTION_GB_NAME = 'Real Time Simulation (Excution)'


class DetectThread(threading.Thread):

    def __init__(self, path, model):
        super().__init__()
        self.path = path
        self.model = model
        self.result = None

    def run(self):
        signal, sample_rate = soundfile.read(self.path)
        payload_decoded, _ = wavmark.decode_watermark(self.model, signal, show_progress=False)

        try:
            payload_list = payload_decoded.tolist()
            payload_txt = ''.join(str(x) for x in payload_list)
            self.result = payload_txt
        except:
            self.result = 'None'

    def get_result(self):
        return self.result



class LoadingDialog(QDialog):

    def __init__(self, title = 'Loading', lbl = 'Loading ...'):
        super().__init__()

        vbox = QVBoxLayout()

        self.setWindowTitle(title)
        self.setMinimumSize(250, 70)
        self.setMaximumSize(250, 70)
        self.label = QLabel(lbl, self)

        vbox.addWidget(self.label)

        self.progress = QProgressBar(self)
        self.progress.setMinimum(0)
        self.progress.setMaximum(100)
        self.progress.setValue(0)
        vbox.addWidget(self.progress)
        
        self.setLayout(vbox)

    def setProgress(self, string, num):
        self.label.setText(string)
        self.progress.setValue(num)



class MyWindow(QWidget):
    SOUNDPATH = ''
    CALLTIME_SEC = 0
    CALL_START = 0
    CALL_END = 0

    def update_audioDetail(self):
        fs, length = audio.getAudioDetail(self.SOUNDPATH)
        self.lbl_audioDetail.setText(f'Sampling Frequency (fs) : {fs}\t Audio Length (sec) : {length}')

    def update_soundPath(self, path):
        if os.path.exists(path):
            self.SOUNDPATH = path
            self.line_filePath.setText(self.SOUNDPATH)
        else:
            self.SOUNDPATH = ''
            self.line_filePath.setText('')
        
        self.update_audioDetail()

    def update_callerInfo(self):
        line = ''
        if self.rbtn_institution.isChecked():
            line = '[Caller : Institution], Make a Call with a Watermarked wave'
        else:
            line = '[Caller : Attacker], Make a Call with a None Watermarked wave'
        
        self.lbl_callerInfo.setText(line)

    def update_detectTime(self):
        if self.CALL_END == 0 and self.CALL_START == 0:
            self.lbl_dectectTime.setText('\tDetect Time - 0:00:00.000000')
            return
        
        delta = self.CALL_END - self.CALL_START

        line = '\tDetect Time - ' + str(delta)
        self.lbl_dectectTime.setText(line)

    def update_detectResult(self, result):
        if result == 1:
            self.line_detectResult.setText('It is safe call (Watermarked wave)')
        elif result == -1:
            self.line_detectResult.setText('It is dangerous call (None watermarked wave)')
        else:
            self.line_detectResult.setText('')



    def getMSsec(sef):
        dt = datetime.now()
        dt.microsecond
        return dt

    def getrecordTime(self):
        string = self.cb_recordTime.currentText()
        return int(string)

    def emptyRecievedFolder(self):
        path = Path.getRecievedFoler()
        for f in os.listdir(path):
            os.remove(os.path.join(path, f))

    def realtimeRecording(self, stop_recording, watermark):
        print('start Real time recording')
        idx = 0
        while True:
            idx += 1
            targetPath = Path.getRecievedFoler() + f'sound{idx}.wav'
            
            if watermark: # Create waterMarked wave 
                tempPath = Path.getTempFoler() + f'sound{idx}.wav'
                payload = wm.create()
                audio.recording(1.1, tempPath)
                signal, sample_rate = soundfile.read(tempPath)

                watermarked_signal, _ = wavmark.encode_watermark(self.model, signal, payload, show_progress=False)

                soundfile.write(targetPath, watermarked_signal, 16000)
                os.remove(tempPath)
            else: # Create None waterMarked wave 
                targetPath = Path.getRecievedFoler() + f'sound{idx}.wav'
                audio.recording(1.1, targetPath)
            
            if stop_recording.is_set():
                break
        
        print('Real time recording ended')

    def realtimeDetecting(self):
        path1 = Path.getRecievedFoler() + 'sound1.wav'
        path2 = Path.getRecievedFoler() + 'sound2.wav'

        while os.path.exists(path1) == False:
            time.sleep(0.2)
        
        self.check1 = DetectThread(path1, self.model)
        self.check1.start()
            
        while os.path.exists(path2) == False:
            time.sleep(0.2)

        self.check2 = DetectThread(path2, self.model)
        self.check2.start()
        
        self.check1.join()
        result1 = self.check1.get_result()
        print(f'Detect sound1 Result : {result1}')

        if result1 != 'None':
            return True
        
        self.check2.join()
        result2 = self.check2.get_result()
        print(f'Detect sound2 Result : {result2}')

        if result1 != 'None':
            return True
        else:
            return False



    def load_findChildren(self):
        self.gb_sound = self.findChildren(QGroupBox)[0]
        self.gb_waterMark = self.findChildren(QGroupBox)[1]
        self.gb_realTimeSetting = self.findChildren(QGroupBox)[2]
        self.gb_realTimeExcution = self.findChildren(QGroupBox)[3]

        self.line_filePath = self.gb_sound.findChildren(QLineEdit)[0]
        self.cb_recordTime = self.gb_sound.findChildren(QComboBox)[0]
        self.lbl_audioDetail = self.gb_sound.findChildren(QLabel)[0]

        self.line_insert_Result = self.gb_waterMark.findChildren(QLineEdit)[0]
        self.line_extract_Result = self.gb_waterMark.findChildren(QLineEdit)[1]

        self.rbtn_institution = self.gb_realTimeSetting.findChildren(QRadioButton)[0]
        self.rbtn_attacker = self.gb_realTimeSetting.findChildren(QRadioButton)[1]
        self.btn_MakeACall = self.gb_realTimeExcution.findChildren(QPushButton)[0]
        self.btn_hangUp = self.gb_realTimeExcution.findChildren(QPushButton)[1]
        self.lbl_callerInfo = self.gb_realTimeExcution.findChildren(QLabel)[0]
        self.lbl_dectectTime = self.gb_realTimeExcution.findChildren(QLabel)[1]
        self.line_detectResult = self.gb_realTimeExcution.findChildren(QLineEdit)[0]

    def load_loadModel(self):
        self.model = wavmark.load_model().to(torch.device('cuda:0' if torch.cuda.is_available() else 'cpu'))
    
    def load_creatkey(self):
        wm.createKey()

    def load_set(self):
        self.update_soundPath(Path.getSoundFile())
        self.cb_recordTime.setCurrentText('3')
        self.update_audioDetail()
        self.rbtn_institution.setChecked(True)
        self.btn_hangUp.setEnabled(False)
        self.update_callerInfo()

    def load_folder(self):
        Folder_temp = Path.getTempFoler()
        Folder_receivced = Path.getRecievedFoler()
        Folder_sound = Path.getSoundFolder()
        Folder_key = Path.getKeyFolder()

        if os.path.exists(Folder_temp) == False:
            os.mkdir(Folder_temp)
        if os.path.exists(Folder_receivced) == False:
            os.mkdir(Folder_receivced)
        if os.path.exists(Folder_sound) == False:
            os.mkdir(Folder_sound)
        if os.path.exists(Folder_key) == False:
            os.mkdir(Folder_key)

    def load_setThreads(self):
        self.stop_recording = threading.Event()



    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def __init__(self):
        super().__init__()

        # 서브 창 띄우기
        self.loading_dialog = LoadingDialog()
        self.loading_dialog.show()
        QApplication.processEvents()  # 이벤트를 처리하여 창이 표시되도록 함

        self.loading_dialog.setProgress('UIinit ...', 0)
        self.UIinit()
        self.loading_dialog.setProgress('FindChildren ...', 20)
        self.load_findChildren()
        self.loading_dialog.setProgress('Setting ...', 40)
        self.load_folder()
        self.load_set()
        self.loading_dialog.setProgress('Load Model ...', 60)
        self.load_loadModel()
        self.loading_dialog.setProgress('Creat key ...', 80)
        self.load_creatkey()
        self.loading_dialog.setProgress('Thread setting ...', 90)
        self.load_setThreads()
        self.loading_dialog.setProgress('Clear !', 100)

        # 서브 창 닫기
        self.loading_dialog.close()

    def UIinit(self):
        self.setWindowTitle('WaterMarking Simulator')
        self.setMaximumSize(700, 450)
        self.setMinimumSize(700, 450)
        self.center()

        grid = QGridLayout()
        grid.addWidget(self.createGroup_soundFile(), 0, 0)
        grid.addWidget(self.createGroup_waterMark(), 1, 0)
        grid.addWidget(self.createGroup_realTime_setting(), 2, 0)
        grid.addWidget(self.createGroup_realTime_excution(), 3, 0)
        self.setLayout(grid)



    def createGroup_soundFile(self):
        groupbox = QGroupBox(SOUNDFILE_GB_NAME)

        vbox = QVBoxLayout()

        line_filepath = QLineEdit(self)
        line_filepath.setReadOnly(True)
        lbl_audioDetail = QLabel(self)

        vbox.addWidget(line_filepath)
        vbox.addWidget(lbl_audioDetail)

        btn_selectFile = QPushButton('Import sound file', self)
        btn_selectFile.clicked.connect(self.btn_selectSoundFile_function)
        btn_record = QPushButton('New recording', self)
        btn_record.clicked.connect(self.btn_record_function)
            
        lbl_time = QLabel(self)
        lbl_time.setText('\tRecording time (sec) :')

        cb_recordTime = QComboBox(self)
        for i in range(2, 11):
            cb_recordTime.addItem(str(i))
    
        hbox = QHBoxLayout()
        hbox.addWidget(btn_selectFile)
        hbox.addWidget(btn_record)
        hbox.addWidget(lbl_time)
        hbox.addWidget(cb_recordTime)

        vbox.addLayout(hbox)

        groupbox.setLayout(vbox)
        return groupbox

    def createGroup_waterMark(self):
        groupbox = QGroupBox(WATERMARK_GB_NAME)

        grid = QGridLayout()

        lbl_insert = QLabel('[Insert]', self)
        btn_WMcreate_insert = QPushButton('Create And insert', self)
        btn_WMcreate_insert.clicked.connect(self.btn_WMcreate_insert_function)
        line_insert_Result = QLineEdit(self)
        line_insert_Result.setReadOnly(True)
        
        lbl_extract = QLabel('[Extract]', self)
        btn_WMextract = QPushButton('Extract', self)
        line_extract_Result = QLineEdit(self)
        line_extract_Result.setReadOnly(True)
        btn_WMextract.clicked.connect(self.btn_WMextract_function)

        grid.addWidget(lbl_insert, 0, 0)
        grid.addWidget(lbl_extract, 0, 1)
        grid.addWidget(btn_WMcreate_insert, 1, 0)
        grid.addWidget(btn_WMextract, 1, 1)
        grid.addWidget(line_insert_Result, 2, 0)
        grid.addWidget(line_extract_Result, 2, 1)

        groupbox.setLayout(grid)
        return groupbox

    def createGroup_realTime_setting(self):
        groupbox = QGroupBox(REALTIMESETTING_GB_NAME)

        hbox = QHBoxLayout()

        lbl_mode = QLabel('[Caller]', self)
        rbtn_institution = QRadioButton('Institution (Watermarked)', self)
        rbtn_institution.clicked.connect(self.rbtn_SettingChange_funtion)
        rbtn_attacker = QRadioButton('Attacker (None Watermarked)', self)
        rbtn_attacker.clicked.connect(self.rbtn_SettingChange_funtion)

        vbox = QVBoxLayout()
        vbox.addWidget(lbl_mode)
        vbox.addWidget(rbtn_institution)
        vbox.addWidget(rbtn_attacker)
        
        hbox.addLayout(vbox)

        groupbox.setLayout(hbox)
        return groupbox

    def createGroup_realTime_excution(self):
        groupbox = QGroupBox(REALTIMEEXCUTION_GB_NAME)
        
        vbox = QVBoxLayout()
        lbl_callerInfo = QLabel('[Caller : Institution], Make a Call with a watermarked wave', self)
        vbox.addWidget(lbl_callerInfo)

        btn_start = QPushButton('Make a call', self)
        btn_start.clicked.connect(self.btn_call_funtion)
        btn_end = QPushButton('Hang up', self)
        btn_end.clicked.connect(self.btn_callEnd_funtion)
        
        hbox = QHBoxLayout()
        hbox.addWidget(btn_start)
        hbox.addWidget(btn_end)

        vbox.addLayout(hbox)

        lbl_detectTime = QLabel('Detect Time - 0:00:00.000000', self)
        lbl_detectResultLabel = QLabel('\tDetect Result : ', self)
        line_detectResult = QLineEdit('', self)
        line_detectResult.setReadOnly(True)

        hbox = QHBoxLayout()
        hbox.addWidget(lbl_detectTime)
        hbox.addWidget(lbl_detectResultLabel)
        hbox.addWidget(line_detectResult)

        vbox.addLayout(hbox)

        groupbox.setLayout(vbox)
        return groupbox



    def btn_selectSoundFile_function(self):
        fname = QFileDialog.getOpenFileName(self, '파일선택', '', 'AllFiles(*.wav)')
        self.update_soundPath(fname[0])

    def btn_record_function(self):
        self.gb_sound.setEnabled(False)
        self.gb_waterMark.setEnabled(False)

        recordTime = self.getrecordTime()

        def recording():
            audio.recording(recordTime, Path.getSoundFile())
            self.update_soundPath(Path.getSoundFile())

        thread_recording = threading.Thread(target=recording)
        thread_recording.start()

        self.loading_dialog = LoadingDialog('Record', 'Recording ...')
        self.loading_dialog
        self.loading_dialog.show()
        QApplication.processEvents()  # 이벤트를 처리하여 창이 표시되도록 함

        self.loading_dialog.setProgress('Recording ...', 0)
        for i in range(1, recordTime + 1):
            time.sleep(1)
            self.loading_dialog.setProgress('Recording ...', int(100/recordTime * i))
        self.loading_dialog.setProgress('Clear !', 100)

        # 서브 창 닫기
        self.loading_dialog.close()

        self.gb_sound.setEnabled(True)
        self.gb_waterMark.setEnabled(True)
        
    def btn_WMcreate_insert_function(self):
        self.loading_dialog = LoadingDialog(lbl='Create Watermark ..')
        self.loading_dialog.show()
        QApplication.processEvents() # 이벤트를 처리하여 창이 표시되도록 함

        payload = wm.create()

        self.loading_dialog.setProgress('insert Watermark ..', 10)

        signal, sample_rate = soundfile.read(self.SOUNDPATH)
        watermarked_signal, _ = wavmark.encode_watermark(self.model, signal, payload, show_progress=True)
        soundfile.write(self.SOUNDPATH, watermarked_signal, 16000)

        self.loading_dialog.setProgress('set UI ..', 90)

        payload_txt = ''.join(str(x) for x in payload)
        self.line_insert_Result.setText(payload_txt)

        self.loading_dialog.setProgress('Clear !', 100)
        self.loading_dialog.close()

    def btn_WMextract_function(self):
        self.loading_dialog = LoadingDialog(lbl='Extract Watermark ..')
        self.loading_dialog.show()
        QApplication.processEvents() # 이벤트를 처리하여 창이 표시되도록 함

        signal, sample_rate = soundfile.read(self.SOUNDPATH)
        payload_decoded, _ = wavmark.decode_watermark(self.model, signal, show_progress=True)

        self.loading_dialog.setProgress('set UI ..', 90)

        result = ''
        try:
            payload_list = payload_decoded.tolist()
            result = ''.join(str(x) for x in payload_list)
        except:
            result = 'None'
        self.line_extract_Result.setText(result)
        
        self.loading_dialog.setProgress('Clear !', 100)
        self.loading_dialog.close()

    def btn_call_funtion(self):
        self.loading_dialog = LoadingDialog()
        self.loading_dialog.show()
        QApplication.processEvents()  # 이벤트를 처리하여 창이 표시되도록 함

        self.gb_sound.setEnabled(False)
        self.gb_waterMark.setEnabled(False)
        self.gb_realTimeSetting.setEnabled(False)

        self.btn_MakeACall.setEnabled(False)
        self.btn_hangUp.setEnabled(True)

        waterMark = self.rbtn_institution.isChecked()
        self.realTimeRecording_thread =  threading.Thread(target=self.realtimeRecording, args=(self.stop_recording, waterMark))
        self.realTimeRecording_thread.start()
        self.CALLTIME_SEC = 0
        self.CALL_END = 0
        self.CALL_START = 0
        self.update_detectTime()

        self.CALL_START = self.getMSsec()

        if self.realtimeDetecting() == True:
            self.update_detectResult(1)
        else:
            self.update_detectResult(-1)
        
        self.btn_callEnd_funtion()

        self.loading_dialog.setProgress('Clear !', 100)

        # 서브 창 닫기
        self.loading_dialog.close()

    def btn_callEnd_funtion(self):
        self.detectTime_function()

        self.gb_sound.setEnabled(True)
        self.gb_waterMark.setEnabled(True)
        self.gb_realTimeSetting.setEnabled(True)

        self.btn_MakeACall.setEnabled(True)
        self.btn_hangUp.setEnabled(False)

        self.stop_recording.set()
        self.realTimeRecording_thread.join()
        self.stop_recording.clear()

        self.emptyRecievedFolder()

    def rbtn_SettingChange_funtion(self):
        self.update_callerInfo()

    def detectTime_function(self):
        self.CALL_END = self.getMSsec()
        self.update_detectTime()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())