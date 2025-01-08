"""from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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
        opcao_responder = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and text()='Responder']"))
        )
        opcao_responder.click()
        time.sleep(1)

        # Passo 4: Localizar a caixa de resposta no rodapé
        caixa_resposta = driver.find_element(By.XPATH, "//footer//div[@contenteditable='true']")
        caixa_resposta.send_keys(resposta)
        caixa_resposta.send_keys(Keys.ENTER)

        print("Mensagem respondida com sucesso.")
    except Exception as e:
        print(f"Erro ao responder a mensagem: {e}")
"""