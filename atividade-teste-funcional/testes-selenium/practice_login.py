import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

URL_BASE = "https://practicetestautomation.com/practice-test-login/"
USUARIO_VALIDO = "student"
SENHA_VALIDA = "Password123"
SENHA_INVALIDA = "shaolimmatadordeporco"

def esperar() -> None:
    time.sleep(3.0)

def _wait_present(driver, by, locator, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, locator)))

def teste_fluxo_positivo(driver) -> bool:
    print("\n--- INICIANDO TESTE DO FLUXO POSITIVO ---")
    try:
        driver.get(URL_BASE)
        _wait_present(driver, By.ID, "username").send_keys(USUARIO_VALIDO)
        esperar()
        _wait_present(driver, By.ID, "password").send_keys(SENHA_VALIDA)
        esperar()
        _wait_present(driver, By.ID, "submit").click()

        # checar se fez o login ou nao
        try:
            WebDriverWait(driver, 10).until(EC.url_contains("/logged-in-successfully"))
        except TimeoutException:
            print("❌ Falha: Não foi redirecionado para a página de sucesso após login.")
            return False
        print("✅ Login válido detectado.")
        esperar()

        # efetuar logout
        try:
            _wait_present(driver, By.LINK_TEXT, "Log out").click()
        except (NoSuchElementException, TimeoutException):
            print("❌ Falha no logout: botão 'Log out' não encontrado.")
            return False
        
        # ver se voltou ou nao para a pagina de login (fez o logout ou nao)
        try:
            WebDriverWait(driver, 10).until(EC.url_contains("/practice-test-login"))
            print("✅ Logout bem-sucedido. Retornou à tela de login.")
            return True
        except TimeoutException:
            print("❌ Falha no logout: Não retornou à tela de login.")
            return False

    except Exception as e:
        print("❌ Exceção no fluxo positivo:", e)
        return False

def teste_fluxo_negativo(driver) -> bool:
    print("\n--- INICIANDO TESTE DO FLUXO NEGATIVO ---")
    try:
        driver.get(URL_BASE)
        _wait_present(driver, By.ID, "username").send_keys(USUARIO_VALIDO)
        esperar()
        _wait_present(driver, By.ID, "password").send_keys(SENHA_INVALIDA)
        esperar()
        _wait_present(driver, By.ID, "submit").click()
        esperar()

        # verificar se a mensagem de erro apareceu
        try:
            div_erro = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "error")))
            if ("Your password is invalid!" in div_erro.text) or ("Your username is invalid!" in div_erro.text):
                print("✅ Teste negativo: mensagem de erro correta exibida.")
                return True
            else:
                print(f"❌ Mensagem de erro inesperada: '{div_erro.text.strip()}'")
                return False
        except TimeoutException:
            print("❌ Mensagem de erro não exibida no tempo esperado.")
            return False

    except Exception as e:
        print("❌ Exceção no fluxo positivo:", e)
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
        resultado_positivo = teste_fluxo_positivo(driver)
        resultado_negativo = teste_fluxo_negativo(driver)

        print("\n--- FIM DOS TESTES ---")
        print(f"Resultado do Fluxo Positivo: {'SUCESSO' if resultado_positivo else 'FALHA'}")
        print(f"Resultado do Fluxo Negativo: {'SUCESSO' if resultado_negativo else 'FALHA'}")

    finally:
        driver.quit()