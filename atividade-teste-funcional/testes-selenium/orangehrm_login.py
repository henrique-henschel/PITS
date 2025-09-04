import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

URL_BASE = "https://opensource-demo.orangehrmlive.com/"
USUARIO_VALIDO = "Admin"
SENHA_VALIDA = "admin123"
SENHA_INVALIDA = "senhaerrada"

def esperar() -> None:
    time.sleep(3.0)

def teste_fluxo_alvo(driver) -> bool:
    print("\n--- INICIANDO TESTE DO FLUXO POSITIVO ---")
    try:
        driver.get(URL_BASE)
        esperar()

        # preencher usuario (correto)
        driver.find_element(By.NAME, "username").send_keys(USUARIO_VALIDO)
        esperar()
        # preencher senha (correta)
        driver.find_element(By.NAME, "password").send_keys(SENHA_VALIDA)
        esperar()
        # clicar no botao de login
        driver.find_element(By.CSS_SELECTOR, "button.oxd-button--main").click()
        esperar()

        # checar se fez login ou nao
        if "dashboard/index" not in driver.current_url:
            print("❌ Falha: Não foi redirecionado para a página de quando o login eh bem-sucedido")
            return False
        print("✅ Login válido detectado.")
        esperar()

        # efetuar logout
        driver.find_element(By.CLASS_NAME, "oxd-userdropdown-tab").click()
        esperar()
        driver.find_element(By.LINK_TEXT, "Logout").click()
        esperar()
        # ver se voltou ou nao para a pagina de login
        if URL_BASE in driver.current_url:
            print("✅ Logout bem-sucedido. Retornou à tela de login.")
            return True
        else:
            print("❌ Falha no logout: Não retornou à tela de login.")
            return False

    except Exception as e:
        print("❌ Exceção no fluxo positivo:", e)
        return False
    
def teste_fluxo_erro(driver) -> bool:
    print("\n--- INICIANDO TESTE DO FLUXO NEGATIVO ---")
    try:
        driver.get(URL_BASE)
        esperar()

        # preencher usuario (correto)
        driver.find_element(By.NAME, "username").send_keys(USUARIO_VALIDO)
        esperar()
        # preencher senha errada
        driver.find_element(By.NAME, "password").send_keys(SENHA_INVALIDA)
        esperar()
        # clicar no botao de login
        driver.find_element(By.CSS_SELECTOR, "button.oxd-button--main").click()
        esperar()

        # verificar se a mensagem de erro apareceu
        div_erro = driver.find_element(By.CSS_SELECTOR, "div.oxd-alert-content--error")
        if "Invalid credentials" in div_erro.text:
            return True
        else:
            return False

    except Exception as e:
        print("❌ Exceção no fluxo negativo:", e)
        return False
    
if __name__ == "__main__":
    options = Options()
    # 1. Desabilita a interface gráfica que pergunta se você quer salvar a senha
    options.add_argument("--disable-features=PasswordLeakDetection")
    # 2. Desabilita o gerenciador de credenciais e o gerenciador de senhas do perfil
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    }
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options)

    try:
        # Executar os testes
        resultado_positivo = teste_fluxo_alvo(driver)
        resultado_negativo = teste_fluxo_erro(driver)

        print("\n--- FIM DOS TESTES ---")
        print(f"Resultado do Fluxo Positivo: {'SUCESSO' if resultado_positivo else 'FALHA'}")
        print(f"Resultado do Fluxo Negativo: {'SUCESSO' if resultado_negativo else 'FALHA'}")

    finally:
        driver.quit()