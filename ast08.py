
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def main():
    driver = None

    try:
        # Configura o navegador para executar em segundo plano
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")

        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(10)

        print("Navegador iniciado em modo headless.")

        # Abre a primeira aba com o dropdown
        driver.get("https://the-internet.herokuapp.com/dropdown")
        aba_0 = driver.current_window_handle

        # Abre a segunda aba e aguarda sua criação
        abas_antes = set(driver.window_handles)

        driver.execute_script(
            "window.open(arguments[0], '_blank');",
            "https://the-internet.herokuapp.com/dynamic_loading/2"
        )

        WebDriverWait(driver, 10).until(
            EC.number_of_windows_to_be(len(abas_antes) + 1)
        )

        aba_1 = (set(driver.window_handles) - abas_antes).pop()

        # Abre a terceira aba e aguarda sua criação
        abas_antes = set(driver.window_handles)

        driver.execute_script(
            "window.open(arguments[0], '_blank');",
            "https://pt.wikipedia.org"
        )

        WebDriverWait(driver, 10).until(
            EC.number_of_windows_to_be(len(abas_antes) + 1)
        )

        aba_2 = (set(driver.window_handles) - abas_antes).pop()

        # Seleciona a opção solicitada no dropdown
        driver.switch_to.window(aba_0)

        dropdown = Select(
            driver.find_element(By.TAG_NAME, "select")
        )
        dropdown.select_by_visible_text("Option 1")

        opcao = dropdown.first_selected_option
        print("Valor selecionado:", opcao.get_attribute("value"))

        # Clica em Start e aguarda o resultado aparecer
        driver.switch_to.window(aba_1)

        espera = WebDriverWait(driver, 15)

        botao_start = espera.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "#start button")
            )
        )
        botao_start.click()

        resultado = espera.until(
            EC.visibility_of_element_located((By.ID, "finish"))
        )

        print("Texto encontrado:", resultado.text)

        # Abre a página principal da Wikipédia
        driver.switch_to.window(aba_2)
        driver.get("https://pt.wikipedia.org/wiki/P%C3%A1gina_principal")

        # Preenche a barra de pesquisa
        pesquisa = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "#searchInput, input[name='search']")
            )
        )
        pesquisa.send_keys("Automação")

        # Abre o menu lateral da Wikipédia, se estiver recolhido
        botoes_menu = driver.find_elements(
            By.CSS_SELECTOR,
            "#vector-main-menu-dropdown, "
            ".vector-header-start .mw-portlet-dropdown"
        )

        for botao in botoes_menu:
            if botao.is_displayed():
                try:
                    botao.click()
                    break
                except Exception:
                    continue

        # Procura links dentro das áreas de navegação
        seletores = [
            "#vector-main-menu a[href]",
            "#mw-panel a[href]",
            "#mw-sidebar a[href]",
            ".vector-main-menu-container a[href]"
        ]

        link_menu = None

        for seletor in seletores:
            links = driver.find_elements(By.CSS_SELECTOR, seletor)

            for link in links:
                texto = link.text.strip()

                if (
                    link.is_displayed()
                    and texto
                    and texto.lower() not in [
                        "doar",
                        "criar conta",
                        "iniciar sessão"
                    ]
                ):
                    link_menu = link
                    break

            if link_menu is not None:
                break

        if link_menu is None:
            raise RuntimeError(
                "Nenhum link visível foi encontrado no menu lateral."
            )

        print("Texto do link:", link_menu.text.strip())
        print("Destino do link:", link_menu.get_attribute("href"))

        # Salva a captura de tela da Wikipédia
        driver.save_screenshot("evidencia_wiki.png")
        print("Captura salva em evidencia_wiki.png")

    finally:
        # Fecha o navegador ao terminar
        if driver is not None:
            driver.quit()
            print("Navegador encerrado.")


if __name__ == "__main__":
    main()
