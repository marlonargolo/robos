from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import random

def iniciar_whatsapp():
    options = webdriver.ChromeOptions()
    options.add_argument("--user-data-dir=./perfil")
    driver = webdriver.Chrome(options=options)
    driver.get("https://web.whatsapp.com/")
    print("Escaneie o QR Code no WhatsApp Web e pressione ENTER para continuar...")
    input()  # Pausa até o usuário pressionar ENTER
    return driver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

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
        
        # Lista para armazenar as mensagens já respondidas
        mensagens_respondidas = set()  # Usando um set para garantir que uma mensagem não seja respondida mais de uma vez

        while True:
            time.sleep(2)
            mensagens = driver.find_elements(By.XPATH, "//div[contains(@class, 'message-in')]")
            
            for mensagem in mensagens[-5:]:  # Apenas as últimas 5 mensagens
                try:
                    remetente_element = mensagem.find_element(By.XPATH, ".//div[contains(@class, 'copyable-text')]")
                    remetente = remetente_element.get_attribute("data-pre-plain-text")
                    print(f"Remetente detectado: {remetente}")

                    texto_element = mensagem.find_element(By.XPATH, ".//span[contains(@class, 'selectable-text')]")
                    texto_mensagem = texto_element.text
                    print(f"Mensagem detectada: {texto_mensagem}")

                    # Verifica se a mensagem veio de uma empresa da lista
                    if remetente and any(empresa.lower() in remetente.lower() for empresa in empresas):
                        print(f"Mensagem de empresa detectada: {texto_mensagem}")
                        
                        # Verifica se a mensagem já foi respondida
                        if texto_mensagem not in mensagens_respondidas:
                            # Passar o mouse sobre a mensagem detectada
                            action = ActionChains(driver)
                            action.move_to_element(mensagem).perform()  # Passar o mouse sobre a mensagem
                            time.sleep(2)  # Manter o mouse sobre a mensagem por um tempo, se necessário
                            
                            numero_aleatorio = random.randint(1, 100)
                            resposta = f"Mensagem respondida! Seu número é: {numero_aleatorio}"
                            responder_mensagem(driver, mensagem, resposta)

                            # Marcar a mensagem como respondida
                            mensagens_respondidas.add(texto_mensagem)
                        else:
                            print(f"Mensagem já respondida: {texto_mensagem}")
                        
                except Exception as e:
                    print(f"Erro ao processar mensagem: {e}")
    except Exception as e:
        print(f"Erro ao monitorar o grupo: {e}")



def responder_mensagem(driver, mensagem, resposta):
    try:
        # Passo 1: Passar o mouse sobre a mensagem para exibir a seta do menu, mantendo o hover por 5 segundos
        action = ActionChains(driver)
        action.move_to_element(mensagem).perform()  # Passar o mouse sobre a mensagem
        time.sleep(5)  # Manter o mouse sobre a mensagem por 5 segundos

        # Passo 2: Esperar o elemento da seta ficar visível e clicável
        seta_menu = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@aria-hidden='true' and @data-icon='down-context']"))
        )
        seta_menu.click()
        time.sleep(1)  # Esperar o menu aparecer

        # Passo 3: Esperar e clicar na opção "Responder"
        caixa_resposta = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/span[5]/div/ul/div/li[1]/div'))
        )
        caixa_resposta.click()  # Clica na opção "Responder"
        time.sleep(1)  # Espera para garantir que a caixa de resposta tenha sido ativada

        # Aqui, colamos a resposta diretamente na caixa de resposta
        caixa_resposta = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//footer//div[@contenteditable='true']"))
        )
        caixa_resposta.send_keys(resposta)  # Cola a resposta
        caixa_resposta.send_keys(Keys.ENTER)  # Envia a resposta
        time.sleep(1)  # Espera para garantir que a mensagem seja enviada

        print("Mensagem respondida com sucesso.")
    except Exception as e:
        print(f"Erro ao responder a mensagem: {e}")


"""def responder_mensagem1(driver, mensagem, resposta):
    mensagem.click()
    time.sleep(1)

    # Localizar a caixa de resposta no rodapé
    caixa_resposta = driver.find_element(By.XPATH, "//footer//div[@contenteditable='true']")
    caixa_resposta.send_keys(resposta)
    caixa_resposta.send_keys(Keys.ENTER)"""

"""def responder_mensagem(driver, mensagem, resposta):
    try:
        # Passo 1: Passar o mouse sobre a seta de menu para exibi-la
        seta_menu = mensagem.find_element(By.XPATH, ".//span[@data-icon='down-context']")
        ActionChains(driver).move_to_element(seta_menu).perform()  # Move o mouse para exibir a seta
        time.sleep(1)

        # Passo 2: Clicar na seta de menu
        seta_menu.click()
        time.sleep(1)

        # Passo 3: Clicar na opção "Responder"
        opcao_responder = driver.find_element(By.XPATH, "//div[@role='button' and text()='Responder']")
        opcao_responder.click()
        time.sleep(1)

        # Passo 4: Localizar a caixa de resposta no rodapé
        caixa_resposta = driver.find_element(By.XPATH, "//footer//div[@contenteditable='true']")
        caixa_resposta.send_keys(resposta)
        caixa_resposta.send_keys(Keys.ENTER)

        print("Mensagem respondida com sucesso.")
    except Exception as e:
        print(f"Erro ao responder a mensagem: {e}")"""


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
