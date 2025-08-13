"""
Script de automação web para emissão de boletos no sistema Embracon
Versão 2.0 - Totalmente humanizada e com tratamento robusto de erros
Desenvolvido para resistir a desconexões e comportar-se como humano
"""

import os
import time
import random
import pyautogui as py
from datetime import datetime
import smtplib
from email.message import EmailMessage
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (TimeoutException,
                                     NoSuchElementException,
                                     WebDriverException,
                                     SessionNotCreatedException)
from smtp_config import SMTPConfig

# ==============================================
# CONFIGURAÇÕES GERAIS
# ==============================================

class Config:
    """Centraliza todas as configurações do sistema"""
    
    # Diretórios
    DOWNLOAD_DIR = r"C:\xampp\htdocs\embracon\Boleto"
    CONTRATOS_DIR = r"C:\xampp\htdocs\embracon\Contrato"
    
    # Credenciais
    USERNAME = "usecred.eireli@embracon.com.br"
    PASSWORD = "Us3Cr3d3@2036"
    
    # URLs
    LOGIN_URL = "https://parceirosweb.embraconnet.com.br/Newcon_Intranet/frmCorCCCnsLogin.aspx"
    
    # Comportamento
    TYPING_SPEED = 0.1  # segundos entre caracteres
    ERROR_RATE = 0.03    # 3% chance de erro de digitação
    MAX_WAIT = 30        # segundos para timeout
    LOGIN_RETRIES = 3    # tentativas de login
    HUMAN_DELAY = (0.1, 0.5)  # intervalo de atraso entre ações

# ==============================================
# INICIALIZAÇÃO DO NAVEGADOR
# ==============================================

def init_browser():
    """Configura e inicializa o navegador Chrome de forma robusta"""
    
    print("🖥️ Inicializando navegador com configurações avançadas...")
    
    options = webdriver.ChromeOptions()
    
    # Configurações básicas
    options.add_argument('--start-maximized')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-extensions')
    options.add_argument('--log-level=3')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # Prevenção contra detecção
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    
    # Configurações de download
    options.add_experimental_option("prefs", {
        "download.default_directory": Config.DOWNLOAD_DIR,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True,
        "safebrowsing.enabled": True
    })
    
    # Configurar serviço do ChromeDriver
    service = Service(executable_path='chromedriver.exe')
    
    # Tentativa de inicialização com tratamento de erros
    try:
        driver = webdriver.Chrome(service=service, options=options)
        
        # Remover indicadores de automação
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        })
        
        return driver, WebDriverWait(driver, Config.MAX_WAIT)
    
    except SessionNotCreatedException as e:
        print(f"🚨 Erro de versão do ChromeDriver: {str(e)}")
        print("Por favor, verifique se a versão do ChromeDriver é compatível com seu Chrome.")
        raise
    except WebDriverException as e:
        print(f"🚨 Erro ao iniciar navegador: {str(e)}")
        raise

# ==============================================
# COMPORTAMENTO HUMANIZADO
# ==============================================

class HumanBehavior:
    """Simula comportamentos humanos realistas"""
    
    @staticmethod
    def random_delay(min_delay=None, max_delay=None):
        """Pausa aleatória entre ações humanas"""
        if min_delay is None or max_delay is None:
            min_delay, max_delay = Config.HUMAN_DELAY
        
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
    
    @staticmethod
    def occasional_long_pause():
        """Pausa mais longa ocasional para simular distração"""
        if random.random() < 0.05:  # 5% chance
            pause = random.uniform(0.8, 2.5)
            print(f"⏳ Pausa humana de {pause:.1f} segundos...")
            time.sleep(pause)
    
    @staticmethod
    def human_move(x, y, duration=None):
        """Movimento do mouse com trajetória natural"""
        if duration is None:
            duration = random.uniform(0.3, 1.0)
        
        # Variação na posição final para parecer mais humano
        x_final = x + random.randint(-5, 5)
        y_final = y + random.randint(-5, 5)
        
        py.moveTo(x_final, y_final, duration=duration, tween=py.easeInOutQuad)
        HumanBehavior.random_delay()
    
    @staticmethod
    def human_click(x=None, y=None, element=None):
        """Clique humanizado com variações"""
        if element is not None:
            x = element.location['x'] + random.randint(5, 15)
            y = element.location['y'] + random.randint(5, 15)
        
        if x is not None and y is not None:
            HumanBehavior.human_move(x, y)
        
        HumanBehavior.random_delay()
        
        # Variação no tempo de pressionamento do clique
        press_duration = random.uniform(0.05, 0.2)
        py.mouseDown(button='left')
        time.sleep(press_duration)
        py.mouseUp(button='left')
        
        HumanBehavior.occasional_long_pause()
    
    @staticmethod
    def human_type(text, speed=Config.TYPING_SPEED, error_chance=Config.ERROR_RATE):
        """Digitação humanizada com erros ocasionais"""
        random.seed(datetime.now().timestamp())
        
        for char in text:
            # Variação na velocidade de digitação
            typing_speed = max(0, speed * random.uniform(0.5, 1.5))
            
            # Simulação de erro de digitação
            if random.random() < error_chance and len(text) > 3:
                wrong_char = chr(ord(char) + random.randint(-2, 2))
                py.typewrite(wrong_char)
                time.sleep(typing_speed * 0.7)
                
                # Correção do erro
                py.press('backspace')
                time.sleep(typing_speed * 0.3)
                
                py.typewrite(char)
            else:
                py.typewrite(char)
            
            time.sleep(typing_speed)
            
            # Pausa ocasional durante a digitação
            if random.random() < 0.03:
                pause = random.uniform(0.3, 1.0)
                time.sleep(pause)

# ==============================================
# FUNÇÕES PRINCIPAIS DE AUTOMAÇÃO
# ==============================================

class EmbraconAutomation:
    """Classe principal que gerencia a automação"""
    
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait
        self.login_attempts = 0
    
    def check_browser_alive(self):
        """Verifica se o navegador ainda está respondendo"""
        try:
            self.driver.current_url
            return True
        except WebDriverException:
            return False
    
    def restart_browser(self):
        """Reinicia o navegador em caso de falha"""
        print("🔄 Reiniciando navegador...")
        try:
            self.driver.quit()
        except:
            pass
        
        try:
            self.driver, self.wait = init_browser()
            return True
        except Exception as e:
            print(f"🚨 Falha ao reiniciar navegador: {str(e)}")
            return False
    
    def login(self):
        """Fluxo de login com múltiplas tentativas e verificação"""
        while self.login_attempts < Config.LOGIN_RETRIES:
            try:
                print(f"\n🔑 Tentativa de login {self.login_attempts + 1} de {Config.LOGIN_RETRIES}")
                
                # Verificar estado do navegador
                if not self.check_browser_alive():
                    if not self.restart_browser():
                        return False
                
                # Acessar página de login
                self.driver.get(Config.LOGIN_URL)
                time.sleep(5)  # Espera inicial importante
                
                # Etapa 1: Inserir email
                print("📩 Inserindo email...")
                email_field = self.wait.until(
                    EC.presence_of_element_located((By.ID, "i0116")),
                    message="Campo de email não encontrado após 30s"
                )
                HumanBehavior.human_type(Config.USERNAME, speed=0.15)
                HumanBehavior.random_delay(0.5, 1.0)
                py.press("enter")
                time.sleep(5)
                
                # Etapa 2: Inserir senha
                print("🔒 Inserindo senha...")
                password_field = self.wait.until(
                    EC.presence_of_element_located((By.ID, "passwordInput")),
                    message="Campo de senha não encontrado após 30s"
                )
                HumanBehavior.human_type(Config.PASSWORD, speed=0.15, error_chance=0.02)
                HumanBehavior.random_delay(0.5, 1.5)
                py.press("enter")
                time.sleep(5)
                
                # Etapa 3: Permanecer conectado (não)
                try:
                    print("⏭ Pulando opção 'permanecer conectado'...")
                    not_now_btn = self.wait.until(
                        EC.presence_of_element_located((By.ID, "idBtn_Back")),
                        message="Botão 'Não' não encontrado após 30s"
                    )
                    HumanBehavior.human_click(x=967, y=675)
                    time.sleep(5)
                except TimeoutException:
                    print("ℹ️ Página de 'permanecer conectado' não apareceu")
                
                # Verificar login bem-sucedido
                print("✅ Verificando login...")
                try:
                    self.wait.until(
                        EC.presence_of_element_located((By.ID, "rptUnidadeNegocio_ctl02_txt_CD_Unidade_Negocio")),
                        message="Elemento pós-login não encontrado após 30s"
                    )
                    print("🎉 Login bem-sucedido!")
                    HumanBehavior.human_click(x=1156, y=520)
                    time.sleep(5)
                    return True
                
                except TimeoutException:
                    print("⚠️ Possível falha no login")
                    if self.check_login_error():
                        self.login_attempts += 1
                        continue
                    raise
            
            except Exception as e:
                self.login_attempts += 1
                print(f"⚠️ Erro durante login (tentativa {self.login_attempts}): {str(e)}")
                
                if self.login_attempts >= Config.LOGIN_RETRIES:
                    print("🚫 Número máximo de tentativas de login atingido")
                    return False
                
                # Espera exponencial antes de tentar novamente
                wait_time = min(10 * self.login_attempts, 30)
                print(f"⏳ Aguardando {wait_time}s antes de tentar novamente...")
                time.sleep(wait_time)
                continue
        
        return False
    
    def check_login_error(self):
        """Verifica se há mensagens de erro na página"""
        try:
            error_msg = self.driver.find_element(By.ID, "errorText")
            print(f"❌ Mensagem de erro: {error_msg.text}")
            return True
        except NoSuchElementException:
            return False
    
    def navigate_to_billing(self):
        """Navega até a seção de boletos"""
        print("🧭 Navegando para a seção de boletos...")
        
        # Sequência de cliques para navegação
        click_sequence = [
            (942, 444),  # Menu principal
            (742, 177),  # clica em cobranças
            (717, 227),  # Emissão de Cobrança
            (580, 395),  # emissão de cobrança
            (572, 396),  # Busca Avançada
            (532, 330),  # Clica no Nome
            (510, 417),  # Seleciona a opção Contrato
        ]
        
        for x, y in click_sequence:
            HumanBehavior.human_click(x=x, y=y)
            time.sleep(3)
    
    def issue_billing(self, contracts):
        for i, contract in enumerate(contracts, 1):
            try:
                # Localizar campo de busca
                search_field = self.driver.find_element(By.ID, "ctl00_Conteudo_edtContextoBusca")
                HumanBehavior.human_type(str(contract), speed=0.15, error_chance=0.03)
                time.sleep(2)
                
                # Clicar no botão de buscar
                search_btn = self.driver.find_element(By.ID, "ctl00_Conteudo_btnBuscar")
                HumanBehavior.human_click(x=1287, y=326)
                time.sleep(5)
                
                # Clicar no nome do Cliente
                search_btn = self.driver.find_element(By.ID, "ctl00_Conteudo_grdBuscaAvancada_ctl02_lnkNM_Pessoa")
                HumanBehavior.human_click(x=898, y=412)
                time.sleep(5)
                
                # Clicar em Confirmar Busca
                search_btn = self.driver.find_element(By.ID, "ctl00_Conteudo_btnConfirma")
                HumanBehavior.human_click(x=1356, y=471)
                time.sleep(5)
                
                # Clicar em Localizar
                search_btn = self.driver.find_element(By.ID, "ctl00_Conteudo_identificacao_cota_btnLocaliza")
                HumanBehavior.human_click(x=1279, y=396)
                time.sleep(5)
                
                # Clicar na caixa do boleto
                input = self.driver.find_element(By.ID, "ctl00_Conteudo_grdBoleto_Avulso_ctl03_imgEmite_Boleto")
                HumanBehavior.human_click(x=493, y=692)
                time.sleep(5)
                
                # abaixa a tela
                HumanBehavior.human_click(x=1917, y=927)
                time.sleep(2)
                
                 # Clicar em emitir cobrança
                search_btn = self.driver.find_element(By.ID, "ctl00_Conteudo_btnEmitir")
                HumanBehavior.human_click(x=878, y=922)
                time.sleep(5)
                
                
                
                # Fluxo de emissão de boleto
                self._billing_flow(contract)
                
                # Renomear arquivo baixado
                self._rename_downloaded_file(contract)
                
                # Voltar para tela inicial
                self._return_to_home()
                
            except Exception as e:
                print(f"⚠️ Erro ao processar contrato {contract}: {str(e)}")
                continue
    
    def _billing_flow(self, contract):
        """Executa o fluxo completo de emissão de boleto"""
        print(f"🔄 Executando fluxo para contrato {contract}...")
        
        # Sequência de cliques para emissão
        click_sequence = [
            (77, 425),   # Botão limpar
            (847, 342),  # Opção de boleto
            (437, 421),  # Gerar boleto
            (886, 485),  # Confirmar
            (854, 417),  # Imprimir
            (53, 692)    # Fechar
        ]
        
        for x, y in click_sequence:
            HumanBehavior.human_click(x=x, y=y)
            time.sleep(5)
        
        # Clicar no botão de impressão
        print_btn = self.driver.find_element(By.ID, "ctl00_Conteudo_btnImprimir")
        HumanBehavior.human_click(element=print_btn)
        time.sleep(10)
        
        # Salvar o PDF
        print("💾 Salvando PDF...")
        HumanBehavior.human_click(x=675, y=161)
        time.sleep(10)
        
        py.hotkey("ctrl", "s")
        time.sleep(2)
        
        pdf_path = os.path.join(Config.CONTRATOS_DIR, f"{contract}.pdf")
        HumanBehavior.human_type(pdf_path, speed=0.12, error_chance=0.02)
        time.sleep(2)
        py.press("enter")
        time.sleep(10)
    
    def _rename_downloaded_file(self, contract):
        """Renomeia o último arquivo baixado com o número do contrato"""
        try:
            files = sorted(
                [os.path.join(Config.DOWNLOAD_DIR, f) for f in os.listdir(Config.DOWNLOAD_DIR)],
                key=os.path.getmtime,
                reverse=True
            )
            
            if files:
                latest_file = files[0]
                new_name = os.path.join(Config.DOWNLOAD_DIR, f"{contract}.pdf")
                
                os.rename(latest_file, new_name)
                print(f"📝 Arquivo renomeado para: {new_name}")
        except Exception as e:
            print(f"⚠️ Erro ao renomear arquivo: {str(e)}")
    
    def _return_to_home(self):
        """Retorna para a tela inicial após emitir um boleto"""
        print("🏠 Voltando para tela inicial...")
        
        HumanBehavior.human_click(x=763, y=15)
        time.sleep(10)
        HumanBehavior.human_click(x=909, y=629)
        time.sleep(10)
        
        # Alterar tipo de pesquisa
        search_type = self.driver.find_element(By.ID, "ctl00_Conteudo_rblTipoPesquisa_1")
        HumanBehavior.human_click(element=search_type)
        time.sleep(10)

# ==============================================
# FUNÇÃO DE EMAIL
# ==============================================

def enviar_email(destinatario: str, caminho_pdf: str, contrato: str) -> None:
    """Envia o PDF gerado para o email informado."""
    msg = EmailMessage()
    msg['Subject'] = f'Boleto do contrato {contrato}'
    msg['From'] = SMTPConfig.USERNAME
    msg['To'] = destinatario
    msg.set_content('Segue em anexo o boleto solicitado.')
    with open(caminho_pdf, 'rb') as f:
        msg.add_attachment(f.read(), maintype='application', subtype='pdf', filename=os.path.basename(caminho_pdf))
    with smtplib.SMTP(SMTPConfig.SERVER, SMTPConfig.PORT) as smtp:
        smtp.starttls()
        smtp.login(SMTPConfig.USERNAME, SMTPConfig.PASSWORD)
        smtp.send_message(msg)

# ==============================================
# EXECUÇÃO PRINCIPAL
# ==============================================

def main(contract: str, email_destino: str) -> str:
    """Emite o boleto para o contrato informado e envia por email."""
    print("="*50)
    print("INICIANDO AUTOMAÇÃO EMBRACON - EMISSÃO DE BOLETOS")
    print("="*50)

    os.makedirs(Config.DOWNLOAD_DIR, exist_ok=True)
    os.makedirs(Config.CONTRATOS_DIR, exist_ok=True)
    print("✅ Diretórios verificados/criados")

    # Inicializar navegador
    try:
        print("\n🖥️ Inicializando navegador...")
        driver, wait = init_browser()
        automator = EmbraconAutomation(driver, wait)
    except Exception as e:
        print(f"🚨 Falha crítica ao iniciar navegador: {str(e)}")
        return ""

    # Executar fluxo principal
    try:
        print("\n🚀 Iniciando fluxo principal...")
        if automator.login():
            automator.navigate_to_billing()
            automator.issue_billing([contract])
        else:
            print("🚫 Não foi possível fazer login após várias tentativas")
    except Exception as e:
        print(f"🚨 Erro fatal durante execução: {str(e)}")
    finally:
        print("\n" + "="*50)
        print("PROCESSO CONCLUÍDO")
        print("="*50)
        print("O navegador permanecerá aberto para verificação.")

    pdf_path = os.path.join(Config.CONTRATOS_DIR, f"{contract}.pdf")
    try:
        enviar_email(email_destino, pdf_path, contract)
        print(f"📧 Email enviado para {email_destino}")
    except Exception as e:
        print(f"⚠️ Falha ao enviar email: {e}")
    return pdf_path


if __name__ == "__main__":
    py.PAUSE = 0.1
    py.FAILSAFE = True
    contrato = input("Número do contrato: ")
    email = input("E-mail para envio: ")
    main(contrato, email)
