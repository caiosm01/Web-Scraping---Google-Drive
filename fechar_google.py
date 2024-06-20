import psutil
import os


# Essa parte do código verifica se tem alguma instância do Google Chrome aberta. Se sim, fecha todas, para que o código não dê erro
if "chrome.exe" in (i.name() for i in psutil.process_iter()):
    os.system("taskkill /f /im chrome.exe")

