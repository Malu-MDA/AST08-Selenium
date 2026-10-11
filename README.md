# AST08 — Automação com Selenium

## Sobre a atividade

A AST08 consiste em desenvolver um script Python com Selenium para automatizar tarefas no navegador em modo headless, gerenciar três abas, interagir com elementos HTML e extrair informações de páginas web.

## Execução

O script `ast08.py` foi executado localmente com Python e Selenium. Ele configura o navegador em modo headless, seleciona `Option 1` em um dropdown, aguarda o carregamento do texto `Hello World!`, pesquisa por **Automação** na Wikipédia e extrai o texto e o endereço de um link do menu lateral. Ao final, salva a captura `evidencia_wiki.png` e encerra o navegador com `driver.quit()`.

Para executar, instale o Selenium e rode:

```bash
pip install selenium
python ast08.py
```

## Testes e integração contínua

O fluxo foi validado por execução local, conferindo os resultados impressos no terminal e a captura de tela gerada. A integração contínua está prevista para ser realizada com **GitHub Actions**, automatizando a execução do script a cada atualização do repositório e permitindo acompanhar o resultado na aba **Actions**.
