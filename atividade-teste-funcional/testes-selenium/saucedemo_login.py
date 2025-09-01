import time
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

PAUSINHA = 1.0
PAUSONA = 2.0

URL_BASE = "https://www.saucedemo.com/"
USUARIO_VALIDO = "standard_user"
SENHA_VALIDA = "secret_sauce"
SENHA_INVALIDA = "senha_errada"

# -------------------- CRIAR/INICIALIZAR O DRIVER: --------------------
def make_driver(headless=False):
    opts = Options()
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1366,900")
    # iniciar Chrome (Selenium Manager cuida do driver)
    driver = webdriver.Chrome(options=opts)
    return driver

# -------------------- TESTE FLUXO POSITIVO: --------------------
def teste_positivo(driver):
    try:
        driver.get(URL_BASE)
        time.sleep(PAUSONA)

        # preencher usuario e senha
        driver.find_element(By.ID, "user-name").send_keys(USUARIO_VALIDO)
        time.sleep(PAUSINHA)
        driver.find_element(By.ID, "password").send_keys(SENHA_VALIDA)
        time.sleep(PAUSINHA)

        # clicar no botao de login
        driver.find_element(By.ID, "login-button").click()
        time.sleep(PAUSONA)  # esperar carregar a pagina de inventario

        # verificar se URL contem "inventory" (indicador simples)
        if "inventory" not in driver.current_url:
            print("❌ Falha: não entrou na página de inventário.")
            return False

        print("✅ Login válido detectado.")

        # efetuar logout (abrir menu e clicar logout)
        driver.find_element(By.ID, "react-burger-menu-btn").click()
        time.sleep(PAUSINHA)
        driver.find_element(By.ID, "logout_sidebar_link").click()
        time.sleep(PAUSONA)

        # ver se voltou ou nao para a pagina de login
        try:
            driver.find_element(By.ID, "login-button")
            print("✅ Logout confirmado. Voltou à tela de login.")
            return True
        except Exception:
            print("❌ Falha no logout ou não voltou à tela de login.")
            return False

    except Exception as e:
        print("❌ Exceção no fluxo positivo:", e)
        return False
    
# -------------------- TESTE FLUXO NEGATIVO: --------------------
def teste_negativo(driver):
    try:
        driver.get(URL_BASE)
        time.sleep(PAUSONA)

        driver.find_element(By.ID, "user-name").send_keys(USUARIO_VALIDO)
        time.sleep(PAUSINHA)
        driver.find_element(By.ID, "password").send_keys(SENHA_INVALIDA)
        time.sleep(PAUSINHA)
        driver.find_element(By.ID, "login-button").click()

        # aguardar resposta
        time.sleep(PAUSONA)

        # tentar capturar a mensagem de erro (SauceDemo usa data-test="error")
        try:
            erro = driver.find_element(By.CLASS_NAME, "error-message-container error").text.strip()
            if erro:
                print("✅ Mensagem de erro detectada:", erro)
                return True
            else:
                print("❌ Mensagem de erro vazia.")
                return False
        except Exception:
            print("❌ Não encontrou a mensagem de erro.")
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
