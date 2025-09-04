import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

URL_BASE = "https://the-internet.herokuapp.com/login"
USUARIO_VALIDO = "tomsmith"
SENHA_VALIDA = "SuperSecretPassword!"
SENHA_INVALIDA = "senha_errada"

def esperar() -> None:
    time.sleep(3.0)

# -------------------- TESTE FLUXO POSITIVO: --------------------
def teste_positivo(driver) -> bool:
    print("\n--- INICIANDO TESTE DO FLUXO POSITIVO ---")
    try:
        driver.get(URL_BASE)
        esperar()

        # preencher usuario e senha corretos
        driver.find_element(By.ID, "username").send_keys(USUARIO_VALIDO)
        esperar()
        driver.find_element(By.ID, "password").send_keys(SENHA_VALIDA)
        esperar()
        # clicar no botao de login
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        esperar()

        # verificar se foi direcionado certinho ou nao
        if "/secure" not in driver.current_url:
            print("❌ Falha: Não foi redirecionado para a página /secure.")
            return False
        print("✅ Login válido detectado.")
        esperar()

        # efetuar logout
        driver.find_element(By.CSS_SELECTOR, "a.button[href='/logout']").click()
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

# -------------------- TESTE FLUXO NEGATIVO: --------------------
def teste_negativo(driver) -> bool:
    print("\n--- INICIANDO TESTE DO FLUXO NEGATIVO ---")
    try:
        driver.get(URL_BASE)
        esperar()

        # Preencher usuario valido e senha invalida
        driver.find_element(By.ID, "username").send_keys(USUARIO_VALIDO)
        esperar()
        driver.find_element(By.ID, "password").send_keys(SENHA_INVALIDA)
        esperar()
        # Clicar no botao de login
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        esperar()

        # Verificar se a mensagem de erro apareceu
        # O elemento da mensagem tem id="flash" e a classe "error"
        mensagem_erro_elemento = driver.find_element(By.CSS_SELECTOR, "div#flash.error")
        mensagem_erro_texto = mensagem_erro_elemento.text
        if "Your username is invalid!" or "Your password is invalid!" in mensagem_erro_texto:
            print(f"✅ Teste negativo bem-sucedido. Mensagem de erro exibida: '{mensagem_erro_texto.strip()}'")
            return True
        else:
            print(f"❌ Falha no teste negativo: Mensagem de erro inesperada ou não encontrada.")
            return False

    except Exception as e:
        print("❌ Exceção no fluxo negativo:", e)
        return False

# -------------------- EXECUÇÃO DOS TESTES --------------------
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
        resultado_positivo = teste_positivo(driver)
        resultado_negativo = teste_negativo(driver)

        print("\n--- FIM DOS TESTES ---")
        print(f"Resultado do Fluxo Positivo: {'SUCESSO' if resultado_positivo else 'FALHA'}")
        print(f"Resultado do Fluxo Negativo: {'SUCESSO' if resultado_negativo else 'FALHA'}")

    finally:
        driver.quit()