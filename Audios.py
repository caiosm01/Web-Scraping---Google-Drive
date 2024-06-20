# Importa as bibliotecas necessárias
from datetime import datetime  # Manipulação de datas
import os  # Interação com o sistema operacional
import time  # Manipulação de tempo (pausas)
import shutil  # Operações em arquivos e diretórios
import logging  # Registro de logs
import pandas as pd  # Manipulação de dataframes
from selenium.webdriver.common.by import By  # Importa a classe By para seleção de elementos web
from selenium.webdriver.support.ui import WebDriverWait  # Espera condicional
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service  # Serviço do Chrome
from selenium.webdriver.common.action_chains import ActionChains  # Sequências de ações do WebDriver
import undetected_chromedriver as uc  # Driver de Chrome não detectado
from openpyxl import load_workbook  # Manipulação de arquivos Excel
import locale  # Localização para formatação adequada
from dotenv import load_dotenv  # Carregar variáveis de ambiente
import mysql.connector  # Conexão com banco de dados MySQL
from urllib.parse import quote

# Carrega as variáveis de ambiente do arquivo .env e define a localização
load_dotenv(override=True)
locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')

# Classe DriveMonitor responsável pelo monitoramento e manipulação dos arquivos
class DriveMonitor:
    def __init__(self):
        """
        Método construtor que inicializa o driver do navegador, 
        configura o sistema de log e cria um DataFrame vazio.
        """
        self.driver = self.setup_chrome()
        self.df = pd.DataFrame(columns=["ID", "Link"])
        self.log = self.setup_logging()

    @staticmethod
    def setup_logging():
        """
        Configura o sistema de log para registrar mensagens de erro e aviso.
        
        Retorna:
            logger (Logger): Objeto de log configurado.
        """
        logging.basicConfig(filename=f'{os.getenv("caminho_log")}', level=logging.WARNING)
        return logging.getLogger()

    def setup_chrome(self):
        """
        Configura o navegador Chrome com as opções necessárias e retorna o driver configurado.
        
        Retorna:
            driver (WebDriver): Objeto WebDriver configurado.
        """
        chromedriver_path = "C:\\Users\\Admin\\.wdm\\drivers\\chromedriver\\chromedriver.exe"
        chrome_options = uc.ChromeOptions()

        chrome_options.add_argument(r'--profile-directory={}'.format(os.getenv("profile_")))
        chrome_options.add_argument(r'--user-data-dir=C:\\Users\\{}\\AppData\\Local\\Google\\Chrome\\User Data\\'.format(os.getenv("usuario")))

        driver = uc.Chrome(version_main=126, executable_path=chromedriver_path, options=chrome_options)
        driver.maximize_window()
        return driver

    def move_files_to_new_directory(self, base_audios, destino_audio, id, info, arquivo, origem_audio):
        """
        Move os arquivos de áudio para um novo diretório.

        Parâmetros:
            base_audios (DataFrame): Base de dados de arquivos de áudio.
            destino_audio (str): Diretório de destino para os arquivos de áudio.
            id (str): Identificador do arquivo.
            info (DataFrame): Informações adicionais do arquivo.
            arquivo (str): Nome do arquivo.
            origem_audio (str): Diretório de origem dos arquivos de áudio.
        """
        try:
            if int(id) not in base_audios['ID'].values:
                caminhoCompleto_old = origem_audio + arquivo
                caminhoCompleto_new = self.get_complete_new_path(destino_audio, info)
                if not os.path.exists(caminhoCompleto_new):
                    os.makedirs(caminhoCompleto_new)
                if not os.path.exists(caminhoCompleto_new + '/' + arquivo):
                    shutil.copy(caminhoCompleto_old, caminhoCompleto_new)

                    if os.path.exists(caminhoCompleto_new + '/' + arquivo):
                        print("Arquivo transferido com sucesso para:", caminhoCompleto_new)
                    else:
                        print("Erro ao transferir o arquivo para:", caminhoCompleto_new)

                    return

                print(f'Já está na pasta: {caminhoCompleto_new}\n')
                return
            else:
                print('Já está na planilha\n')
                return 'Já está na planilha'
        except Exception as e:
            print(f"Erro durante a transferência do arquivo: {e}")

    def get_aeroporto_name(self, cursor, info):
        """
        Obtém o nome do aeroporto a partir da informação da base de dados.

        Parâmetros:
            cursor (Cursor): Cursor do banco de dados.
            info (DataFrame): Informações adicionais do arquivo.

        Retorna:
            aeroporto_nome (str): Nome do aeroporto.
        """
        id_aeroporto = info['id_aeroportos'].values[0]
        cursor.execute(os.getenv("Query_banco_id")+f"{id_aeroporto};")
        aeroporto_nome = pd.DataFrame(cursor.fetchall(), columns=cursor.column_names)
        return aeroporto_nome['ICAO'].values[0]

    def get_mes(self, info):
        """
        Retorna o mês em português, com base na data de início.

        Parâmetros:
            info (DataFrame): Informações adicionais do arquivo.

        Retorna:
            mes (str): Nome do mês em português.
        """
        return datetime(pd.DatetimeIndex(info['Data_Inicio']).year.values[0], pd.DatetimeIndex(info['Data_Inicio']).month.values[0], pd.DatetimeIndex(info['Data_Inicio']).day.values[0]).strftime("%B").capitalize()

    def process_individual_file(self, df, log, driver, base_audios, planilha, id, info, arquivo, count, erro, book, page):
        """
        Processa um único arquivo de áudio, automatizando ações no Google Drive.

        Parâmetros:
            df (DataFrame): DataFrame para armazenar os links obtidos.
            log (Logger): Objeto de log para registrar eventos.
            driver (WebDriver): Driver do navegador.
            base_audios (DataFrame): Base de dados de arquivos de áudio.
            planilha (str): Caminho da planilha Excel.
            id (str): Identificador do arquivo.
            info (DataFrame): Informações adicionais do arquivo.
            arquivo (str): Nome do arquivo.
            count (int): Contador de arquivos processados.
            erro (int): Contador de erros.
            book (Workbook): Objeto da planilha Excel.
            page (Worksheet): Página da planilha Excel.

        Retorna:
            link_obtido (str): Link público do arquivo no Google Drive.
        """
        ident = []
        link = []
        Data = []
        Verificador = []
        Pesquisador = []
        Coleta = []
        Status = []
        link_obtido = ''

        try:
            os.system("echo off | clip")
            if int(id) in base_audios['ID'].values:
                print('id na base Consultas.xlsx')
                return
            else:
                base_url = "https://drive.google.com/drive/u/2/search?q="
                text = arquivo
                encoded_text = quote(text)
                final_url = base_url + encoded_text

                self.driver.get(final_url)

                try:
                    WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.XPATH,f'//*[@guidedhelpid="main_container"]//*[@aria-label="{arquivo} Áudio Mais informações (Alt + →)"]')).click()

                    element_to_click = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="drive_main_page"]//*[@aria-label="Copiar link"]')))

                    element_to_click.click()
                    time.sleep(5)
                    link_obtido = driver.execute_script("return navigator.clipboard.readText().then(text => text);")

                except:
                    link_obtido = ''

                finally:
                    if not link_obtido:
                        print('Sem link')
                        return None

                    print(link_obtido)

                    ident.append(id)
                    link.append(link_obtido)
                    Data.append('')
                    Verificador.append('')
                    Pesquisador.append('')
                    Coleta.append('')
                    Status.append('')

                    log.warning(f"{self.get_complete_new_path(destino_audio, info) + '/' + arquivo}\n")
                    log.level

                    df.loc[count] = [Data[count], Verificador[count], Pesquisador[count], ident[count], Coleta[count], Status[count], link[count]]

                    for info2 in df.values.tolist():
                        page.append(info2)

                    book.save(filename=planilha)
                    df.drop(0, axis='index')

        except:
            erro += 1
            log.error(f"{id},ERRO")
            ident.append(id)
            link.append('')
            Data.append('')
            Verificador.append('')
            Pesquisador.append('')
            Coleta.append('')
            Status.append('')
            log.level
            df.loc[count] = [Data[count], Verificador[count], Pesquisador[count], ident[count], Coleta[count], Status[count], link[count]]

            for info2 in df.values.tolist():
                page.append(info2)

            book.save(filename=planilha)
            df.drop(0, axis='index')

            if erro == 50:
                log.error(f"Limite de erros atingido")
                return
            else:
                pass

            print("Sem link")
            return "Sem link"

        return link_obtido

    def get_complete_new_path(self, destino_audio, info):
        """
        Retorna o caminho completo para o novo diretório.

        Parâmetros:
            destino_audio (str): Diretório de destino para os arquivos de áudio.
            info (DataFrame): Informações adicionais do arquivo.

        Retorna:
            caminhoCompleto (str): Caminho completo para o novo diretório.
        """
        aeroporto = self.get_aeroporto_name(cursor, info)
        mes = self.get_mes(info)
        return destino_audio + aeroporto + '/' + str(pd.DatetimeIndex(info['Data_Inicio']).year.values[0]) + '/' + mes

    def process_files(self, base, base_audios, planilha, origem_audio, destino_audio):
        """
        Processa todos os arquivos de áudio na origem especificada.

        Parâmetros:
            base (DataFrame): Base de dados.
            base_audios (DataFrame): Base de dados de arquivos de áudio.
            planilha (str): Caminho da planilha Excel.
            origem_audio (str): Diretório de origem dos arquivos de áudio.
            destino_audio (str): Diretório de destino para os arquivos de áudio.
        """
        count = 0
        erro = 0
        book = load_workbook(planilha)
        page = book[os.getenv("sheet_name")]

        for diretorio, suborigem_audios, arquivos in os.walk(origem_audio):
            for arquivo in arquivos:
                id = arquivo.split(' ')[0].strip()

                print(id)

                info = base[base['Nro. Identificação'] == int(id)]
                resposta = self.move_files_to_new_directory(base_audios, destino_audio, id, info, arquivo, origem_audio)

                if resposta == 'Já está na planilha':
                    pass
                else:
                    MAX_TENTATIVAS = 3
                    for tentativa in range(MAX_TENTATIVAS):
                        link = self.process_individual_file(self.df, self.log, self.driver, base_audios, planilha, id, info, arquivo, count, erro, book, page)
                        if link:
                            break
                        time.sleep(5)

    def run(self, banco_dados, planilha, origem_audio, destino_audio):
        """
        Inicia o processo de monitoramento.

        Parâmetros:
            banco_dados (DataFrame): Base de dados.
            planilha (str): Caminho da planilha Excel.
            origem_audio (str): Diretório de origem dos arquivos de áudio.
            destino_audio (str): Diretório de destino para os arquivos de áudio.
        """
        os.system("echo off | clip")
        base = banco_dados
        base_audios = pd.read_excel(planilha, sheet_name=os.getenv("sheet_name"))
        self.process_files(base, base_audios, planilha, origem_audio, destino_audio)
        self.driver.quit()

# Se este script for o principal em execução
if __name__ == "__main__":
    # Conecta ao banco de dados e carrega as informações necessárias
    con = mysql.connector.connect(host=os.getenv("host"), database=os.getenv("data_base"), user=os.getenv("User"), password=os.getenv("Password"))
    cursor = con.cursor()
    cursor.execute(os.getenv("Query_banco"))
    banco_dados = pd.DataFrame(cursor.fetchall(), columns=cursor.column_names)
    planilha = os.getenv("planilha")
    origem_audio = os.getenv("origem_audio")
    destino_audio = os.getenv("destino_audio")
    monitor = DriveMonitor()
    monitor.run(banco_dados, planilha, origem_audio, destino_audio)

