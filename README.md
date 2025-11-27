# Conversor de Logs OSSEC para Power BI

Este script converte arquivos de log não estruturados do OSSEC/Wazuh em planilhas Excel formatadas e prontas para importação no Power BI.

## 🚀 Como usar

### Pré-requisitos
Você precisa ter o [Python](https://www.python.org/) instalado.

### Instalação (Faça isso apenas na primeira vez)

**1. Clone ou baixe este repositório.**

**2. Crie um ambiente virtual (Recomendado):**
Isso evita erros de permissão e mantém seu sistema limpo.

* **Linux / Mac:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
* **Windows (PowerShell ou CMD):**
    ```cmd
    python -m venv venv
    venv\Scripts\activate
    ```

**3. Instale as dependências:**
```bash
pip install -r requirements.txt
