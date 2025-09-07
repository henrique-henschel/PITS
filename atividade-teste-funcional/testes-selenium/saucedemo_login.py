import time
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

URL_BASE = "https://www.saucedemo.com/"
USUARIO_VALIDO = "standard_user"
SENHA_VALIDA = "secret_sauce"
SENHA_INVALIDA = "senha_errada"

def esperar() -> None:
    time.sleep(3.0)

# -------------------- CRIAR/INICIALIZAR O DRIVER: --------------------
def make_driver(headless=False):
    opts = Options()
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1366,900")
    driver = webdriver.Chrome(options=opts)
    return driver

def _wait_present(driver, by, locator, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, locator)))

# -------------------- TESTE FLUXO POSITIVO: --------------------
def teste_positivo(driver) -> bool:
    try:
        driver.get(URL_BASE)
        esperar()

        _wait_present(driver, By.ID, "user-name").send_keys(USUARIO_VALIDO)
        esperar()
        _wait_present(driver, By.ID, "password").send_keys(SENHA_VALIDA)
        esperar()
        _wait_present(driver, By.ID, "login-button").click()
        esperar()

        # verificar se URL contem "inventory"
        try:
            WebDriverWait(driver, 10).until(EC.url_contains("inventory"))
        except TimeoutException:
            print("❌ Falha: não entrou na página de inventário.")
            return False
        print("✅ Login válido detectado.")

        # efetuar logout (abrir menu e clicar logout)
        esperar()
        try:
            _wait_present(driver, By.ID, "react-burger-menu-btn").click()
            esperar()
            _wait_present(driver, By.ID, "logout_sidebar_link").click()
        except (NoSuchElementException, TimeoutException):
            print("❌ Falha no logout ou elementos do menu não encontrados.")
            return False
        
        # ver se voltou ou nao para a pagina de login
        esperar()
        try:
            _wait_present(driver, By.ID, "login-button", timeout=10)
            print("✅ Logout confirmado. Voltou à tela de login.")
            return True
        except TimeoutException:
            print("❌ Falha no logout: botão de login não encontrado após logout.")
            return False

    except Exception as e:
        print("❌ Exceção no fluxo positivo:", e)
        return False
    
# -------------------- TESTE FLUXO NEGATIVO: --------------------
def teste_negativo(driver) -> bool:
    try:
        driver.get(URL_BASE)
        _wait_present(driver, By.ID, "user-name").send_keys(USUARIO_VALIDO)
        esperar()
        _wait_present(driver, By.ID, "password").send_keys(SENHA_INVALIDA)
        esperar()
        _wait_present(driver, By.ID, "login-button").click()
        esperar()

        # tentar localizar o elemento <h3> que exibe a mensagem de erro
        try:
            elemento_erro = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test="error"]'))
            )
            expected = "Epic sadface: Username and password do not match any user in this service"
            if expected in elemento_erro.text:
                print("✅ SUCESSO: Teste de fluxo negativo concluído com sucesso.")
                print(f"   Mensagem de erro exibida: '{elemento_erro.text}'")
                return True
            else:
                print("❌ FALHA: A mensagem de erro exibida é diferente do esperado.")
                print(f"   Mensagem encontrada: '{elemento_erro.text}'")
                return False
        except TimeoutException:
            print("❌ FALHA: mensagem de erro não exibida no tempo esperado.")
            return False

    except Exception as e:
        print("❌ Exceção no fluxo negativo:", e)
        return False
    
# -------------------- METODO DE ENTRADA MAIN(): --------------------
def main(mode="both", headless=False):
    driver = make_driver(headless=headless)
    try:
        if mode in ("both", "positive"):
            print("==> Executando fluxo POSITIVO...")
            ok = teste_positivo(driver)
            print("Resultado POSITIVO:", "PASS" if ok else "FAIL")
            # estamos de volta na tela de login (ou falhou)

        if mode in ("both", "negative"):
            print("==> Executando fluxo NEGATIVO...")
            ok = teste_negativo(driver)
            print("Resultado NEGATIVO:", "PASS" if ok else "FAIL")

    finally:
        driver.quit()

# -------------------- CHAMANDO O MAIN(): --------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["both", "positive", "negative"], default="both")
    parser.add_argument("--headless", default=str(False))
    args = parser.parse_args()

    headless_flag = args.headless.lower() not in ("0", "false", "no")
    main(mode=args.mode, headless=headless_flag)