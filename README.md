# Projeto, Implementação e Teste de Software

Breve guia para baixar, configurar e executar os scripts de teste presentes neste repositório.

> Estrutura dentro deste repositório:

```
atividade-teste-funcional/
├─ .venv/                  # ambiente virtual (DEVERÁ SER CRIADO, NÃO VEM JUNTO!)
├─ testes-selenium/        # 4 scripts em Python + Selenium (1 por site)
├─ testes-playwright/      # 4 scripts em Python + Playwright (mesma cobertura)
└─ ATIVIDADE-TESTE-FUNCIONAL.pdf  # enunciado da atividade
```

---

## Pré-requisitos

- Python 3.8+ instalado
- Git (para clonar o repositório)
- Conexão com a internet (para baixar dependências e navegadores do Playwright)

---

## 1) Clonar o repositório

```bash
git clone https://github.com/henrique-henschel/PITS
cd PITS
```

---

## 2) Recomendações de ambiente (virtualenv)

Linux / macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

---

## 3) Instalar dependências

Instale dependências comuns para ambos os conjuntos de testes (Selenium e Playwright):

### Selenium

```bash
pip install selenium
```

### Playwright

```bash
pip install playwright
playwright install
```

---

## 4) Rodar os testes

### Executar os scripts em Selenium

```bash
cd testes-selenium
python <nome_do_arquivo.py>
```

### Executar os scripts em Playwright

```bash
cd testes-playwright
python <nome_do_arquivo.py>
```

#### **OBS: Substitua `<nome_do_arquivo.py>` pelo nome do arquivo que deseja rodar**

---

## 5) Onde está a descrição da atividade?

O enunciado completo encontra-se em `atividade-teste-funcional/ATIVIDADE-TESTE-FUNCIONAL.pdf`.