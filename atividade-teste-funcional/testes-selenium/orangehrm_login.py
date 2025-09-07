import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

URL_BASE = "https://opensource-demo.orangehrmlive.com/"
USUARIO_VALIDO = "Admin"
SENHA_VALIDA = "admin123"
SENHA_INVALIDA = "senhaerrada"

def esperar() -> None:
    time.sleep(3.0)

def _wait_present(driver, by, locator, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, locator)))

def teste_fluxo_alvo(driver) -> bool:
    print("\n--- INICIANDO TESTE DO FLUXO POSITIVO ---")
    try:
        driver.get(URL_BASE)
        
        # preencher usuario (correto)
        _wait_present(driver, By.NAME, "username").send_keys(USUARIO_VALIDO)
        esperar()
        # preencher senha (correta)
        _wait_present(driver, By.NAME, "password").send_keys(SENHA_VALIDA)
        esperar()
        # clicar no botao de login
        _wait_present(driver, By.CSS_SELECTOR, "button.oxd-button--main").click()

        # checar se fez login ou nao
        try:
            WebDriverWait(driver, 10).until(EC.url_contains("dashboard"))
        except TimeoutException:
            print("❌ Falha: Não foi redirecionado para a página de dashboard após login.")
            return False
        print("✅ Login válido detectado.")
        esperar()

        # efetuar logout
        try:
            _wait_present(driver, By.CLASS_NAME, "oxd-userdropdown-tab").click()
            _wait_present(driver, By.LINK_TEXT, "Logout").click()
        except (NoSuchElementException, TimeoutException):
            print("❌ Falha no logout: elementos de logout não encontrados.")
            return False
        
        # ver se voltou ou nao para a pagina de login
        try:
            _wait_present(driver, By.NAME, "username")
            print("✅ Logout bem-sucedido. Retornou à tela de login.")
            return True
        except TimeoutException:
            print("❌ Falha no logout: Não retornou à tela de login.")
            return False

    except Exception as e:
        print("❌ Exceção no fluxo positivo:", e)
        return False
    
def teste_fluxo_erro(driver) -> bool:
    print("\n--- INICIANDO TESTE DO FLUXO NEGATIVO ---")
    try:
        driver.get(URL_BASE)

        _wait_present(driver, By.NAME, "username").send_keys(USUARIO_VALIDO)
        esperar()
        _wait_present(driver, By.NAME, "password").send_keys(SENHA_INVALIDA)
        esperar()
        _wait_present(driver, By.CSS_SELECTOR, "button.oxd-button--main").click()
        esperar()

        # verificar se a mensagem de erro apareceu
        try:
            div_erro = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.oxd-alert-content--error"))
            )
            if "Invalid credentials" in div_erro.text:
                print("✅ Mensagem de erro esperada exibida.")
                return True
            else:
                print(f"❌ Mensagem de erro diferente do esperado: '{div_erro.text.strip()}'")
                return False
        except TimeoutException:
            print("❌ Mensagem de erro não exibida.")
            return False

    except Exception as e:
        print("❌ Exceção no fluxo negativo:", e)
        return False
    
if __name__ == "__main__":
    options = Options()
    options.add_argument("--disable-features=PasswordLeakDetection")
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    }
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options)

    try:
        resultado_positivo = teste_fluxo_alvo(driver)
        resultado_negativo = teste_fluxo_erro(driver)

        print("\n--- FIM DOS TESTES ---")
        print(f"Resultado do Fluxo Positivo: {'SUCESSO' if resultado_positivo else 'FALHA'}")
        print(f"Resultado do Fluxo Negativo: {'SUCESSO' if resultado_negativo else 'FALHA'}")

    finally:
        driver.quit()