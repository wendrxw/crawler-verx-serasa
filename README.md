# Yahoo Finance Screener Crawler

Este repositório é um teste para a empresa VERX. Na ocasião, desenvolvi um **crawler automatizado** para o **Yahoo Finance – Equity Screener**, utilizando **Python**, que coleta dados de ações de forma paginada, com suporte a **filtros por região**, geração de **CSV**, **logs estruturados** e **testes automatizados com pytest**.

---

## Objetivo

Extrair dados do **Yahoo Finance Screener**, especificamente:

* `symbol` → Código da ação
* `name` → Nome da empresa
* `price` → Preço intraday

Com suporte a:

* Remoção de filtros default (ex: *United States*)
* Aplicação de filtros personalizados (ex: `--region Brazil`)
* Paginação automática até a última página
* Exportação dos resultados em CSV

---

## Tecnologias Utilizadas

* **Python 3.13+**
* **Selenium (Chromium)**
* **BeautifulSoup4**
* **pandas**
* **pytest**
* **logging**
* **uv** (gerenciador de ambiente)

---

## Estrutura do Projeto

```text
crawler/
├── src/
│   ├── driver.py        # Lógica principal do crawler
│   ├── logger.py        # Configuração de logging
│   ├── utils.py         # Parser de argumentos CLI
│   └── __init__.py
├── tests/
│   ├── test_crawler.py  # Testes globais
│   └── __init__.py
├── main.py              # Entry point do projeto
├── pyproject.toml
└── README.md
```

---

## Configuração

### Criar ambiente virtual

```bash
uv venv
source .venv/bin/activate
```

### Instalar dependências

```bash
uv sync
```

### Configurar variáveis de ambiente

O arquivo `.env` já existe no projeto (como é um teste pontual, não removi o .env do repositório):

```env
URL=https://finance.yahoo.com/research-hub/screener/equity/
```

---

## Como Rodar o Projeto

### Execução simples (sem filtro)

```bash
uv run main.py
```

### Execução com filtro de região

```bash
uv run main.py --region Brazil
```

Regiões suportadas dependem da UI do Yahoo Finance (ex: `Brazil`, `Argentina`, `United States`).

O navegador roda em **modo headless** (nenhuma janela é aberta).

---

## Saída

Ao final da execução, será gerado um arquivo CSV no formato:

```text
stocks_YYYY_MM_DD_HH_MM_SS.csv
```

Com as colunas:

```csv
symbol,name,price
```

---

## Logs

O projeto utiliza o módulo `logging` para exibir informações no terminal:

* Inicialização do crawler
* Aplicação de filtros
* Paginação
* Extração de dados
* Geração do CSV

Exemplo:

```text
[2026-01-07 15:12:10] [INFO] Iniciando crawler
[2026-01-07 15:12:18] [INFO] Iniciando crawler filtrando pela região: Brazil
[2026-01-07 15:12:30] [INFO] Iniciando gravação dos dados para CSV
```

---

## 🧪 Testes Automatizados

Os testes foram escritos com **pytest**, focando em **lógica de negócio**, sem depender de um navegador real.

### Executar todos os testes

```bash
uv run pytest
```

### Executar com coverage

```bash
uv run pytest -cov=src
```

---

## Boas Práticas Aplicadas

* Selenium desacoplado dos testes
* Uso de mocks para WebDriver
* Headless browser para CI / servidores
* Logging estruturado
* Código organizado por responsabilidade

