from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# Função para enviar uma mensagem
def send_message(driver, phone_number, message):
    # Aguardando a página carregar completamente
    time.sleep(5)
    
    # Acessando o campo de pesquisa para encontrar o chat
    search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
    search_box.click()
    search_box.send_keys(phone_number)
    search_box.send_keys(Keys.ENTER)
    time.sleep(3)
    
    # Encontrando o campo de mensagem e enviando a mensagem
    message_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="1"]')
    message_box.click()
    message_box.send_keys(message)
    message_box.send_keys(Keys.ENTER)
    print(f"Mensagem enviada para {phone_number}")

# Função para enviar uma figurinha
def send_sticker(driver, phone_number, sticker_path):
    # Aguardando a página carregar completamente
    time.sleep(5)

    # Acessando o campo de pesquisa para encontrar o chat
    search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
    search_box.click()
    search_box.send_keys(phone_number)
    search_box.send_keys(Keys.ENTER)
    time.sleep(3)
    
    # Clicando no botão de anexo (clip) para enviar a figurinha
    attach_button = driver.find_element(By.XPATH, '//span[@data-icon="clip"]')
    attach_button.click()
    time.sleep(1)

    # Clicando na opção de enviar figurinha
    sticker_button = driver.find_element(By.XPATH, '//input[@accept="image/webp,image/apng,image/svg+xml,image/*"]')
    sticker_button.send_keys(sticker_path)
    time.sleep(3)

    # Enviar figurinha (após enviar, o botão de enviar se torna invisível)
    send_button = driver.find_element(By.XPATH, '//span[@data-icon="send"]')
    send_button.click()
    print(f"Figurinha enviada para {phone_number}")

# Configuração do Selenium para abrir o WhatsApp Web
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")  # Abrir o navegador maximizado
options.add_argument("--disable-notifications")  # Desabilitar notificações, se necessário

# Configuração do WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Abrir o WhatsApp Web
driver.get("https://web.whatsapp.com")

# Aguardar o QR Code ser escaneado
print("O WhatsApp Web foi aberto. Escaneie o QR Code com seu celular.")
time.sleep(15)  # Espera 15 segundos para o usuário escanear o QR Code e o login ser realizado

# Verificando se o login foi bem-sucedido (a página inicial com chats será carregada)
try:
    # Se o chat estiver carregado, procuramos o campo de pesquisa para verificar que o login foi feito
    driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
    print("Login realizado com sucesso!")
except Exception as e:
    print("Erro ao fazer login. Tente novamente.")
    driver.quit()
    exit()

# Enviar uma mensagem de texto para um número específico
phone_number = "+55xxxxxxxxxxx"  # Substitua pelo número desejado
message = "Olá, essa é uma mensagem automática enviada pelo bot!"
send_message(driver, phone_number, message)

# Enviar uma figurinha (sticker) para o mesmo número
sticker_path = "/caminho/para/sua/figurinha.webp"  # Substitua com o caminho correto da figurinha
send_sticker(driver, phone_number, sticker_path)

# Finaliza o driver após o envio
time.sleep(5)
driver.quit()
