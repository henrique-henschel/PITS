import re
import time
import traceback
from playwright.sync_api import Playwright, sync_playwright, expect

URL_BASE = "https://practicetestautomation.com/practice-test-login/"
USER = "student"
PASS_OK = "Password123"
PASS_BAD = "senha_errada"

def esperar(secs=3.0):
    time.sleep(secs)

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    try:
        # positivo
        page.goto(URL_BASE)
        esperar()
        page.fill("#username", USER)
        esperar()
        page.fill("#password", PASS_OK)
        esperar()
        page.click("#submit")
        esperar()
        expect(page).to_have_url(re.compile(r".*/logged-in-successfully"), timeout=10000)
        print("✅ Practice: login positivo OK")
        esperar()

        # logout
        page.click("text=Log out")
        esperar()
        expect(page).to_have_url(re.compile(r".*/practice-test-login"), timeout=10000)
        print("✅ Practice: logout OK")
        esperar()

        # negativo
        page.goto(URL_BASE)
        esperar()
        page.fill("#username", USER)
        esperar()
        page.fill("#password", PASS_BAD)
        esperar()
        page.click("#submit")
        esperar()
        erro = page.locator("#error")
        expect(erro).to_be_visible(timeout=10000)
        text = erro.inner_text().strip()
        if "Your password is invalid!" in text or "Your username is invalid!" in text:
            print("✅ Practice: fluxo negativo detectou mensagem de erro:", text)
        else:
            print("❌ Practice: mensagem de erro inesperada:", text)

    except Exception:
        print("❌ Exceção em practice_playwright:")
        print(traceback.format_exc())
    finally:
        context.close()
        browser.close()

if __name__ == "__main__":
    with sync_playwright() as pw:
        run(pw)