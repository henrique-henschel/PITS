import time
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

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

# -------------------- TESTE FLUXO POSITIVO: --------------------
def teste_positivo(driver) -> bool:
    try:
        driver.get(URL_BASE)
        esperar()

        # preencher usuario e senha corretos
        driver.find_element(By.ID, "user-name").send_keys(USUARIO_VALIDO)
        esperar()
        driver.find_element(By.ID, "password").send_keys(SENHA_VALIDA)
        esperar()
        # clicar no botao de login
        driver.find_element(By.ID, "login-button").click()
        esperar()  # esperar carregar a pagina de inventario

        # verificar se URL contem "inventory"
        if "inventory" not in driver.current_url:
            print("❌ Falha: não entrou na página de inventário.")
            return False
        print("✅ Login válido detectado.")

        # efetuar logout (abrir menu e clicar logout)
        driver.find_element(By.ID, "react-burger-menu-btn").click()
        esperar()
        driver.find_element(By.ID, "logout_sidebar_link").click()
        esperar()
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
def teste_negativo(driver) -> bool:
    try:
        driver.get(URL_BASE)
        esperar()

        driver.find_element(By.ID, "user-name").send_keys(USUARIO_VALIDO)
        esperar()
        driver.find_element(By.ID, "password").send_keys(SENHA_INVALIDA)
        esperar()
        driver.find_element(By.ID, "login-button").click()
        # aguardar resposta
        esperar()

        # tentar localizar o elemento <h3> que exibe a mensagem de erro
        elemento_erro = driver.find_element(By.CSS_SELECTOR, '[data-test="error"]')
        if "Epic sadface: Username and password do not match any user in this service" in elemento_erro.text:
            print(f"✅ SUCESSO: Teste de fluxo negativo concluído com sucesso.")
            print(f"   Mensagem de erro exibida: '{elemento_erro.text}'")
            return True
        else:
            print(f"❌ FALHA: A mensagem de erro exibida é diferente do esperado.")
            print(f"   Mensagem encontrada: '{elemento_erro.text}'")
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