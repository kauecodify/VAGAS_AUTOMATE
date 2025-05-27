# VAGAS\_AUTOMATE

Automação open‑source em Python que lê informações chave do seu currículo e se candidata automaticamente a vagas compatíveis em portais como **Indeed** e formulários externos.

---

## Principais Recursos

![image](https://github.com/user-attachments/assets/38ece46f-40e4-4ce6-9cd1-69723db79e05)


| Funcionalidade                      | Descrição                                                                                                    |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| **Interface Tkinter**               | GUI para selecionar o currículo, definir número máximo de candidaturas e iniciar o bot sem linha de comando. |
| **Preenchimento Inteligente**       | Completa nome, e‑mail, telefone, experiência, formação e resumo profissional.                                |
| **Suporte a Múltiplos Formulários** | Detecta e preenche formulários do Indeed, iframes externos e layouts genéricos.                              |
| **Upload de Currículo**             | Anexa PDF ou DOCX sempre que o campo `<input type="file">` estiver disponível.                               |
| **Registro em CSV**                 | Salva em `vagas_aplicadas.csv` data/hora, título, empresa, link e status (Aplicado/Falha).                   |
| **Evasão de CAPTCHA**               | Pausa quando CAPTCHA é detectado, evitando bloqueios.                                                        |

---

## ⚙️ Pré‑requisitos

* **Python ≥ 3.9** (recomendado 3.12)
* **Google Chrome** ou **Microsoft Edge** instalado
* **Chromedriver/Edgedriver** (gerenciado automaticamente pelo `webdriver‑manager`)

Instale as dependências em um ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt  # ou:
pip install selenium webdriver-manager pandas python-docx tk
```

> **Observação:** no Linux, instale as bibliotecas Tk (`sudo apt install python3-tk`) e os pacotes do navegador (fonts‑liberation, etc.) se necessário.

---

## 🔑 Configuração Rápida

Abra **`vagas_automate.py`** e edite o dicionário `self.user_data` na classe `JobApplicationAutomation`:

```python
self.user_data = {
    "email": "seu_email@exemplo.com",      # e‑mail de contato
    "senha": "sua_senha",                 # senha (se necessário para login)
    "nome_completo": "Seu Nome Completo",
    "telefone": "(11) 91234‑5678",
    "experiencia": ["Python", "Automação", "Selenium", "Web Scraping"],
    "formacao": "Seu curso ou último grau",   # Ex.: Bacharel em Eng. da Computação
    "resumo": "Profissional com X anos em…"   # Máx. ~2 000 caracteres
}
```

Variáveis adicionais:

| Campo                    | Onde usar                                | Obrigatório                        |
| ------------------------ | ---------------------------------------- | ---------------------------------- |
| `self.applied_jobs_file` | Nome do CSV de log                       | Não (padrão `vagas_aplicadas.csv`) |
| `self.resume_path`       | Caminho do currículo selecionado via GUI | Sim – se quiser anexar currículo   |

---

## ▶️ Como Executar

```bash
python vagas_automate.py
```

1. **Selecionar Currículo**: clique em **“Selecionar Currículo (PDF/DOCX)”**.
2. **Número Máx. de Candidaturas**: defina quantas vagas o bot deve tentar (padrão = 5).
3. **Iniciar Automação**: o navegador abrirá e o script começará a busca/aplicação.
4. **Acompanhe o Terminal**: mensagens ✅/⚠️ indicam sucesso ou falha.

O CSV de log é gerado na mesma pasta; abra‑o no Excel/Sheets para acompanhar.

---

## 📁 Estrutura de Diretórios Sugerida

```
VAGAS_AUTOMATE/
├── vagas_automate.py         # Script principal (GUI + automação)
├── requirements.txt          # Lista de dependências
├── vagas_aplicadas.csv       # Gerado automaticamente
└── README.md                 # Este documento
```

---

## 🛠️ Personalização

* **Filtros de vagas**: implemente lógica de palavra‑chave ou localização dentro do método `search_jobs()`.
* **CAPTCHA handling**: hoje o bot pausa; você pode integrar serviços de resolução.
* **Novos portais**: crie métodos parecidos com `fill_indeed_form()` para outros sites.

---

## 🤝 Contribuindo

1. Faça um *fork* do projeto
2. Crie sua *branch*: `git checkout -b feature/MinhaFuncionalidade`
3. *Commit*: `git commit -m 'Adiciona MinhaFuncionalidade'`
4. *Push*: `git push origin feature/MinhaFuncionalidade`
5. Abra um *Pull Request*

Sugestões, *issues* e *PRs* são bem‑vindos!

---

## 📝 Licença

Distribuído sob a licença **MIT**. Veja `LICENSE` para detalhes.

---

## 📣 Aviso Legal

> Este software automatiza interações com websites de terceiros. Verifique os **Termos de Uso** dos portais antes de executar o bot por suspensões de conta ou uso indevido.

---

### Feliz caça – vagas! 🚀

![anonymous-minneapolis](https://github.com/user-attachments/assets/669aadbc-d4c1-4786-b85e-cfaffcd7ebcb)


