# 🧭 CodeCompass
> Uma ferramenta CLI com inteligência artificial para explorar, compreender e modernizar códigos legados.

Não se perca no legado — deixe o CodeCompass guiar.

![GitHub last commit](https://img.shields.io/github/last-commit/pedroeugenio212/CodeCompass)
![GitHub repo size](https://img.shields.io/github/repo-size/pedroeugenio212/CodeCompass)
![GitHub license](https://img.shields.io/github/license/pedroeugenio212/CodeCompass)

---

## 📌 Visão Geral

O **CodeCompass** é um agente de linha de comando que ajuda desenvolvedores a entender códigos legados de forma rápida, clara e objetiva. Ele analisa múltiplos arquivos de um projeto, identifica padrões problemáticos e gera relatórios em diversos formatos.

---

## ✨ Funcionalidades

- 📁 Varredura automática de arquivos em múltiplas linguagens
- 🧠 Simulação de análise com IA (resumo, sugestões, riscos)
- ⚠️ Classificação de pontos de atenção e sugestões por tipo
- 📊 Relatórios em JSON, Markdown e Excel
- 🔥 Pronto para integração com IA real (ChatGPT, Claude, etc.)

---

## 🖼️ Exemplo de Uso

```bash
python3 codecompass.py ./seu-projeto
```

📄 `src/main/java/UserDao.java`  
Linguagem: Java  
Resumo: Arquivo com 132 linhas.  
Pontos de atenção:
- Consulta SQL direta  
- Método muito longo  
Sugestões:
- Criar camada DAO  
- Usar Spring Boot  
Risco: **Alto**

---

## 🧩 Tecnologias Utilizadas

- Python 3
- `argparse`, `pathlib`, `json`
- [pandas](https://pandas.pydata.org/) + `openpyxl` (para exportar Excel)
- Suporte a múltiplas linguagens: Java, Python, JavaScript, C#, etc.

---

## 📤 Relatórios Gerados

- `codecompass_report.json`
- `codecompass_report.md`
- `codecompass_report.xlsx`

---

## 🛠️ Como executar

### 1. Clonar o projeto
```bash
git clone https://github.com/pedroeugenio212/CodeCompass.git
cd CodeCompass
```

### 2. Instalar dependências
```bash
pip install -r requirements.txt
```

### 3. Executar análise
```bash
python3 codecompass.py ./caminho/do/projeto
```

---

## 📅 Roadmap

- [x] Análise básica com sugestões simuladas
- [x] Exportação para JSON, Markdown e Excel
- [x] Classificação de risco por arquivo
- [x] Ignorar pastas de build
- [ ] Integração com OpenAI API (GPT-4)
- [ ] Extensão VS Code
- [ ] Web dashboard interativo

---

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se livre para abrir *issues* ou *pull requests*.

---

## 📜 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
