import re
import time
import traceback
from playwright.sync_api import Playwright, sync_playwright, expect

URL_BASE = "https://the-internet.herokuapp.com/login"
USER = "tomsmith"
PASS_OK = "SuperSecretPassword!"
PASS_BAD = "senha_errada"

def esperar(secs=3.0):
    time.sleep(secs)

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    try:
        # --- fluxo positivo ---
        page.goto(URL_BASE)
        esperar()
        page.fill("#username", USER)
        esperar()
        page.fill("#password", PASS_OK)
        esperar()
        page.click("button[type='submit']")
        esperar()
        # aguardar redirecionamento para /secure
        expect(page).to_have_url(re.compile(r".*/secure"), timeout=10000)
        print("✅ Herokuapp: login positivo OK")
        esperar()

        # logout
        page.click("a[href='/logout']")
        esperar()
        expect(page).to_have_url(re.compile(r".*/login"), timeout=10000)
        print("✅ Herokuapp: logout OK")
        esperar()

        # --- fluxo negativo ---
        page.goto(URL_BASE)
        esperar()
        page.fill("#username", USER)
        esperar()
        page.fill("#password", PASS_BAD)
        esperar()
        page.click("button[type='submit']")
        esperar()
        # aguardar aparecimento da mensagem de erro
        flash = page.locator("#flash")
        expect(flash).to_be_visible(timeout=10000)
        text = flash.inner_text().strip()
        if "Your username is invalid!" in text or "Your password is invalid!" in text:
            print("✅ Herokuapp: fluxo negativo detectou mensagem de erro:", text)
        else:
            print("❌ Herokuapp: mensagem de erro inesperada:", text)

    except Exception:
        print("❌ Exceção em herokuapp_playwright:")
        print(traceback.format_exc())
    finally:
        context.close()
        browser.close()

if __name__ == "__main__":
    with sync_playwright() as pw:
        run(pw)