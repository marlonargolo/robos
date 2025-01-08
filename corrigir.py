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
        search_box = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@contenteditable='true']"))
        )
        search_box.click()
        search_box.send_keys(nome_grupo)
        search_box.send_keys(Keys.ENTER)

        print(f"Monitorando o grupo: {nome_grupo}")

        ultima_resposta = datetime.min  # Inicialmente, nenhuma mensagem foi respondida
        mensagens_respondidas = {}  # Dicionário para rastrear mensagens respondidas com timestamp

        while True:
            time.sleep(2)

            # Se o bot ainda está no intervalo de espera, aguarda o tempo de 4 minutos
            if (datetime.now() - ultima_resposta) < timedelta(minutes=4):
                continue

            mensagens = driver.find_elements(By.XPATH, "//div[contains(@class, 'message-in')]")

            for mensagem in mensagens:
                try:
                    # Verificar se o atributo 'data-pre-plain-text' está presente
                    remetente_element = mensagem.find_element(By.XPATH, ".//div[contains(@class, 'copyable-text')]")
                    remetente = remetente_element.get_attribute("data-pre-plain-text")

                    if not remetente:
                        continue  # Pula mensagens que não possuem o atributo esperado

                    texto_element = mensagem.find_element(By.XPATH, ".//span[contains(@class, 'selectable-text')]")
                    texto_mensagem = texto_element.text

                    # Extraímos o timestamp da mensagem no formato "[HH:mm]"
                    try:
                        timestamp = remetente.strip().split(",")[1].strip("[]").split(" ")[0]
                        horario_recebido = datetime.strptime(timestamp, "%H:%M").replace(
                            year=datetime.now().year, month=datetime.now().month, day=datetime.now().day
                        )
                    except (IndexError, ValueError):
                        print("Horário não encontrado ou em formato inesperado. Ignorando mensagem.")
                        continue

                    # Verifica se a mensagem veio de uma empresa da lista
                    if remetente and any(empresa.lower() in remetente.lower() for empresa in empresas):
                        empresa_detectada = next(empresa for empresa in empresas if empresa.lower() in remetente.lower())

                        # Ignora mensagens recebidas antes do início do bot
                        if horario_recebido < ultima_resposta:
                            continue

                        # Ignora mensagens já respondidas
                        if (texto_mensagem, horario_recebido) in mensagens_respondidas.values():
                            print(f"Mensagem já respondida: {texto_mensagem}")
                            continue

                        # Responder a mensagem
                        print(f"Respondendo à mensagem de {empresa_detectada}: {texto_mensagem}")
                        resposta = f"Resposta automatizada: {random.randint(100, 999)}"
                        responder_mensagem(driver, mensagem, resposta)

                        # Atualizar o controle de mensagens respondidas e última resposta
                        mensagens_respondidas[empresa_detectada] = (texto_mensagem, horario_recebido)
                        ultima_resposta = datetime.now()
                        break  # Sai do loop para reiniciar o ciclo de monitoramento
                except Exception as e:
                    print(f"Erro ao processar mensagem: {e}")
    except Exception as e:
        print(f"Erro ao monitorar o grupo: {e}")


def responder_mensagem(driver, mensagem, resposta):
    try:
        # Passo 1: Passar o mouse sobre a mensagem para exibir a seta do menu
        action = ActionChains(driver)
        action.move_to_element(mensagem).perform()
        time.sleep(1)

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
    lista_empresas = ["Marlon ChatBoot", "Luana Lima", "Guilherme - Barbeiro", "Hugo"]
    nome_do_grupo = "Grupoteste"
    driver = iniciar_whatsapp()
    try:
        monitorar_grupo(driver, nome_do_grupo, lista_empresas)
    except KeyboardInterrupt:
        print("Bot encerrado.")
    finally:
        driver.quit()
