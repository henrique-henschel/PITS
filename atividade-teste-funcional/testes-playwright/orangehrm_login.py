import re
import time
import traceback
from playwright.sync_api import Playwright, sync_playwright, expect

URL_BASE = "https://opensource-demo.orangehrmlive.com/"
USER = "Admin"
PASS_OK = "admin123"
PASS_BAD = "senhaerrada"

def esperar(secs=3.0):
    time.sleep(secs)

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    try:
        # fluxo positivo
        page.goto(URL_BASE)
        esperar()
        page.fill('input[name="username"]', USER)
        esperar()
        page.fill('input[name="password"]', PASS_OK)
        esperar()
        page.click("button.oxd-button--main")
        esperar()
        # aguardar dashboard (url ou elemento)
        expect(page).to_have_url(re.compile(r".*dashboard.*"), timeout=10000)
        print("✅ OrangeHRM: login positivo OK")
        esperar()

        # logout via user dropdown -> Logout
        page.click(".oxd-userdropdown-tab")
        esperar()
        page.click("text=Logout")
        esperar()
        # confirmar retorno à tela de login (campo username presente)
        expect(page.locator('input[name="username"]')).to_be_visible(timeout=10000)
        print("✅ OrangeHRM: logout OK")
        esperar()

        # fluxo negativo
        page.goto(URL_BASE)
        esperar()
        page.fill('input[name="username"]', USER)
        esperar()
        page.fill('input[name="password"]', PASS_BAD)
        esperar()
        page.click("button.oxd-button--main")
        esperar()
        # aguardar elemento de erro
        erro = page.locator("div.oxd-alert-content--error")
        expect(erro).to_be_visible(timeout=10000)
        text = erro.inner_text().strip()
        if "Invalid credentials" in text:
            print("✅ OrangeHRM: fluxo negativo detectou mensagem de erro:", text)
        else:
            print("❌ OrangeHRM: mensagem de erro inesperada:", text)

    except Exception:
        print("❌ Exceção em orangehrm_playwright:")
        print(traceback.format_exc())
    finally:
        context.close()
        browser.close()

if __name__ == "__main__":
    with sync_playwright() as pw:
        run(pw)