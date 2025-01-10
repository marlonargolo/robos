from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random


def iniciar_whatsapp():
    options = webdriver.ChromeOptions()
    options.add_argument("--user-data-dir=./perfil")  # Perfil para manter login
    driver = webdriver.Chrome(options=options)
    driver.get("https://web.whatsapp.com/")
    print("Escaneie o QR Code no WhatsApp Web e pressione ENTER para continuar...")
    input()  # Pausa até o usuário pressionar ENTER
    return driver

def mover_mouse_para_elemento(driver, elemento):
    """
    Leva o mouse até um elemento específico na página.

    :param driver: Instância do webdriver
    :param elemento: WebElement correspondente ao objeto alvo
    """
    try:
        # Garantir que o elemento esteja visível
        driver.execute_script("arguments[0].scrollIntoView(true);", elemento)
        time.sleep(1)  # Pequena pausa para garantir o scroll completo

        # Mover o mouse até o elemento
        action = ActionChains(driver)
        action.move_to_element(elemento).perform()
        action.click()
        print("Mouse movido para o elemento com sucesso.")
    except Exception as e:
        print(f"Erro ao mover o mouse para o elemento: {e}")



def monitorar_grupo(driver, nome_grupo, empresas):
    try:
        # Localizar e acessar o grupo
        search_box = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@contenteditable='true']"))
        )
        search_box.click()
        search_box.send_keys(nome_grupo)
        search_box.send_keys(Keys.ENTER)

        print(f"Monitorando o grupo: {nome_grupo}")

        # Ignorar mensagens anteriores
        mensagens_respondidas = set()
        print("Ignorando mensagens antigas...")
        time.sleep(5)  # Tempo para carregar as mensagens anteriores
        mensagens_respondidas.update(
            msg.text for msg in driver.find_elements(By.XPATH, "//span[contains(@class, 'selectable-text')]")
        )

        print("Bot iniciado, aguardando novas mensagens...")

        while True:
            # Monitorar novas mensagens
            mensagens = driver.find_elements(By.XPATH, "//div[contains(@class, 'message-in')]")
            nova_mensagem_detectada = False  # Para controlar o loop após responder

            for mensagem in mensagens[-5:]:
                try:
                    remetente_element = mensagem.find_element(By.XPATH, ".//div[contains(@class, 'copyable-text')]")
                    remetente = remetente_element.get_attribute("data-pre-plain-text")

                    texto_element = mensagem.find_element(By.XPATH, ".//span[contains(@class, 'selectable-text')]")
                    texto_mensagem = texto_element.text

                    # Verificar remetente e se a mensagem foi respondida
                    if remetente and texto_mensagem not in mensagens_respondidas and \
                            any(empresa.lower() in remetente.lower() for empresa in empresas):

                        print(f"Nova mensagem de {remetente}: {texto_mensagem}")

                        # Mover o mouse até a mensagem
                        mover_mouse_para_elemento(driver, mensagem)

                        # Responder a mensagem
                        resposta = f"118"
                        responder_mensagem(driver, mensagem, resposta)

                        # Marcar a mensagem como respondida
                        mensagens_respondidas.add(texto_mensagem)

                        # Atualizar o conjunto de mensagens respondidas com todas as mensagens visíveis
                        mensagens_respondidas.update(
                            msg.text for msg in driver.find_elements(By.XPATH, "//span[contains(@class, 'selectable-text')]")
                        )

                        # Pausar por 1 minuto e aguardar novas mensagens
                        print("Aguardando 1 minuto antes de continuar...")
                        time.sleep(60)  # Suspende o processamento por 1 minuto
                        nova_mensagem_detectada = True
                        break  # Sai do loop interno para reiniciar o monitoramento

                except Exception as e:
                    print(f"Erro ao processar mensagem: {e}")
            
            # Se nenhuma nova mensagem foi detectada, continue o loop
            if not nova_mensagem_detectada:
                print("Aguardando novas mensagens...")
                time.sleep(2)  # Pequena pausa para reduzir uso de CPU

    except Exception as e:
        print(f"Erro ao monitorar o grupo: {e}")



def responder_mensagem(driver, mensagem, resposta):
    try:
        # Tornar a seta do menu visível
        seta_menu = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[@aria-hidden='true' and @data-icon='down-context']"))
        )
        driver.execute_script(
            "arguments[0].setAttribute('style','visibility:visible; display:block;');", seta_menu
        )

        # Garantir que a seta do menu esteja clicável
        seta_menu = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@aria-hidden='true' and @data-icon='down-context']"))
        )
        seta_menu.click()
        time.sleep(1)

        # Selecionar a opção "Responder"
        opcao_responder = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/span[5]/div/ul/div/li[1]/div'))
        )
        opcao_responder.click()
        time.sleep(1)

        # Escrever e enviar a resposta
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
    nome_do_grupo = "Automacao"
    driver = iniciar_whatsapp()
    try:
        monitorar_grupo(driver, nome_do_grupo, lista_empresas)
    except KeyboardInterrupt:
        print("Bot encerrado.")
    finally:
        driver.quit()
