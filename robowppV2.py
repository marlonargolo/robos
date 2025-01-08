import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random

def iniciar_whatsapp():
    options = webdriver.ChromeOptions()
    options.add_argument("--user-data-dir=./perfil")
    driver = webdriver.Chrome(options=options)
    driver.get("https://web.whatsapp.com/")
    print("Escaneie o QR Code no WhatsApp Web e pressione ENTER para continuar...")
    input()  # Pausa até o usuário pressionar ENTER
    return driver

def monitorar_grupo(driver, nome_grupo, empresas):
    try:
        # Esperar até que o campo de pesquisa esteja visível
        search_box = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@contenteditable='true']"))
        )
        search_box.click()
        search_box.send_keys(nome_grupo)
        search_box.send_keys(Keys.ENTER)

        print(f"Monitorando o grupo: {nome_grupo}")
        
        # Dicionário para armazenar a última mensagem de cada empresa
        mensagens_por_empresa = {}
        # Dicionário para armazenar o tempo da última resposta enviada para cada empresa
        ultima_resposta = {}

        while True:
            time.sleep(2)
            mensagens = driver.find_elements(By.XPATH, "//div[contains(@class, 'message-in')]")
            
            for mensagem in mensagens[-5:]:  # Apenas as últimas 5 mensagens
                try:
                    remetente_element = mensagem.find_element(By.XPATH, ".//div[contains(@class, 'copyable-text')]")
                    remetente = remetente_element.get_attribute("data-pre-plain-text")
                    texto_element = mensagem.find_element(By.XPATH, ".//span[contains(@class, 'selectable-text')]")
                    texto_mensagem = texto_element.text

                    # Verifica se a mensagem veio de uma empresa da lista
                    if remetente and any(empresa.lower() in remetente.lower() for empresa in empresas):
                        empresa_detectada = next(empresa for empresa in empresas if empresa.lower() in remetente.lower())
                        
                        # Armazena a mensagem mais recente da empresa
                        mensagens_por_empresa[empresa_detectada] = (mensagem, texto_mensagem)
                except Exception as e:
                    print(f"Erro ao processar mensagem: {e}")

            # Responder apenas a mensagem mais recente de cada empresa após o tempo de espera
            agora = datetime.now()
            for empresa, (mensagem, texto_mensagem) in mensagens_por_empresa.items():
                if empresa in ultima_resposta:
                    tempo_espera = agora - ultima_resposta[empresa]
                    if tempo_espera < timedelta(minutes=4):
                        print(f"Aguardando 4 minutos para responder novamente a {empresa}.")
                        continue
                
                # Responder à mensagem mais recente
                try:
                    print(f"Respondendo à mensagem mais recente de {empresa}: {texto_mensagem}")
                    numero_aleatorio = random.randint(1, 100)
                    resposta = f"Mensagem respondida! Seu número é: {numero_aleatorio}"
                    responder_mensagem(driver, mensagem, resposta)
                    
                    # Atualizar o tempo da última resposta
                    ultima_resposta[empresa] = datetime.now()
                except Exception as e:
                    print(f"Erro ao responder mensagem de {empresa}: {e}")
            
            # Limpar o dicionário para a próxima verificação
            mensagens_por_empresa.clear()
    except Exception as e:
        print(f"Erro ao monitorar o grupo: {e}")

def responder_mensagem(driver, mensagem, resposta):
    try:
        # Passo 1: Passar o mouse sobre a mensagem para exibir a seta do menu
        action = ActionChains(driver)
        action.move_to_element(mensagem).perform()
        time.sleep(2)

        # Passo 2: Localizar e clicar na seta do menu
        seta_menu = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@aria-hidden='true' and @data-icon='down-context']"))
        )
        seta_menu.click()
        time.sleep(1)

        # Passo 3: Selecionar a opção "Responder"
        opcao_responder = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/span[5]/div/ul/div/li[1]/div'))
        )
        opcao_responder.click()
        time.sleep(1)

        # Passo 4: Escrever e enviar a resposta
        caixa_resposta = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//footer//div[@contenteditable='true']"))
        )
        caixa_resposta.send_keys(resposta)
        caixa_resposta.send_keys(Keys.ENTER)
        print("Mensagem respondida com sucesso.")
    except Exception as e:
        print(f"Erro ao responder a mensagem: {e}")

if __name__ == "__main__":
    lista_empresas = ["Hugo", "EMarlon", "Mercado Z"]
    nome_do_grupo = "Grupoteste"
    driver = iniciar_whatsapp()
    try:
        monitorar_grupo(driver, nome_do_grupo, lista_empresas)
    except KeyboardInterrupt:
        print("Bot encerrado.")
    finally:
        driver.quit()
