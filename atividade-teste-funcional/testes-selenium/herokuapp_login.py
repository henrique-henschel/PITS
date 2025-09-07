import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

URL_BASE = "https://the-internet.herokuapp.com/login"
USUARIO_VALIDO = "tomsmith"
SENHA_VALIDA = "SuperSecretPassword!"
SENHA_INVALIDA = "senha_errada"

def esperar() -> None:
    time.sleep(3.0)

def _wait_present(driver, by, locator, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, locator)))

# -------------------- TESTE FLUXO POSITIVO: --------------------
def teste_positivo(driver) -> bool:
    print("\n--- INICIANDO TESTE DO FLUXO POSITIVO ---")
    try:
        driver.get(URL_BASE)
        
        # preencher usuario e senha corretos (espera explicita pelo campo)
        _wait_present(driver, By.ID, "username").send_keys(USUARIO_VALIDO)
        esperar()
        _wait_present(driver, By.ID, "password").send_keys(SENHA_VALIDA)
        esperar()
        # clicar no botao de login
        _wait_present(driver, By.CSS_SELECTOR, "button[type='submit']").click()

        # verificar se foi direcionado certinho
        try:
            WebDriverWait(driver, 10).until(EC.url_contains("/secure"))
        except TimeoutException:
            print("❌ Falha: Não foi redirecionado para a página /secure.")
            return False
        print("✅ Login válido detectado.")
        esperar()

        # efetuar logout
        try:
            _wait_present(driver, By.CSS_SELECTOR, "a.button[href='/logout']").click()
        except (NoSuchElementException, TimeoutException):
            print("❌ Falha no logout: botão de logout não encontrado.")
            return False
        
        # ver se voltou ou nao para a pagina de login
        try:
            WebDriverWait(driver, 10).until(EC.url_contains("/login"))
            print("✅ Logout bem-sucedido. Retornou à tela de login.")
            return True
        except TimeoutException:
            print("❌ Falha no logout: Não retornou à tela de login.")
            return False

    except Exception as e:
        print("❌ Exceção no fluxo positivo:", e)
        return False

# -------------------- TESTE FLUXO NEGATIVO: --------------------
def teste_negativo(driver) -> bool:
    print("\n--- INICIANDO TESTE DO FLUXO NEGATIVO ---")
    try:
        driver.get(URL_BASE)

        # preencher usuario valido e senha invalida
        _wait_present(driver, By.ID, "username").send_keys(USUARIO_VALIDO)
        esperar()
        _wait_present(driver, By.ID, "password").send_keys(SENHA_INVALIDA)
        esperar()
        # clicar no botao de login
        _wait_present(driver, By.CSS_SELECTOR, "button[type='submit']").click()
        esperar()

        # verificar se a mensagem de erro apareceu
        try:
            mensagem_erro_elemento = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div#flash"))
            )
            mensagem_erro_texto = mensagem_erro_elemento.text
            if ("Your username is invalid!" in mensagem_erro_texto) or ("Your password is invalid!" in mensagem_erro_texto):
                print(f"✅ Teste negativo bem-sucedido. Mensagem de erro exibida: '{mensagem_erro_texto.strip()}'")
                return True
            else:
                print(f"❌ Falha no teste negativo: Mensagem de erro inesperada: '{mensagem_erro_texto.strip()}'")
                return False
        except TimeoutException:
            print("❌ Falha no teste negativo: mensagem de erro não apareceu.")
            return False

    except Exception as e:
        print("❌ Exceção no fluxo negativo:", e)
        return False

# -------------------- EXECUCAO DOS TESTES --------------------
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
        resultado_positivo = teste_positivo(driver)
        resultado_negativo = teste_negativo(driver)

        print("\n--- FIM DOS TESTES ---")
        print(f"Resultado do Fluxo Positivo: {'SUCESSO' if resultado_positivo else 'FALHA'}")
        print(f"Resultado do Fluxo Negativo: {'SUCESSO' if resultado_negativo else 'FALHA'}")

    finally:
        driver.quit()