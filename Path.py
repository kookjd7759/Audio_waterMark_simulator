import os
projectName = 'Auido_Digital_signature'

def getKeyFolder():
    return os.getcwd() + f'\\{projectName}\\Key\\'

def getSoundFolder():
    return os.getcwd() + f'\\{projectName}\\Sound\\'

def getSoundFile():
    return os.getcwd() + f'\\{projectName}\\Sound\\sound.wav'

def getTempFoler():
    return os.getcwd() + f'\\{projectName}\\temp\\'

def getRecievedFoler():
    return os.getcwd() + f'\\{projectName}\\Recieved\\'
