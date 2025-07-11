import json
import pathlib
import sys
import os
from typing import List, Dict

import openai

EXT_PARA_LINGUAGEM = {
    ".py": "Python",
    ".java": "Java",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".c": "C",
    ".cpp": "C++",
    ".cs": "C#",
    ".go": "Go",
    ".rb": "Ruby",
    ".php": "PHP",
    ".rs": "Rust",
    ".swift": "Swift",
}


def listar_arquivos(diretorio: pathlib.Path) -> List[pathlib.Path]:
    """Retorna todos os arquivos conhecidos em um diretório recursivamente.

    Pastas comuns de build e dependências são ignoradas.
    """
    ignorar_pastas = {"target", "build", "node_modules", "__pycache__"}
    return [
        p
        for p in diretorio.rglob("*")
        if p.is_file()
        and p.suffix in EXT_PARA_LINGUAGEM
        and not any(part in ignorar_pastas for part in p.parts)
    ]


def analisar_codigo_conteudo(caminho: pathlib.Path, conteudo: str) -> Dict:
    ext = caminho.suffix.lower()
    linguagem = EXT_PARA_LINGUAGEM.get(ext, "Desconhecida")
    resumo = f"Arquivo com {len(conteudo.splitlines())} linhas."
    pontos_atencao: List[str] = []
    sugestoes = {
        "refatoracao": [],
        "modernizacao": [],
        "boas_praticas": [],
    }

    # Heurísticas simples para preencher dados de demonstração
    lower_content = conteudo.lower()
    if "select" in lower_content:
        pontos_atencao.append("Consulta SQL direta detectada")
        sugestoes["boas_praticas"].append("Criar camada DAO")
        sugestoes["modernizacao"].append("Migrar para ORM ou Spring Data JPA")

    if linguagem == "Java":
        sugestoes["modernizacao"].append("Considere usar Spring Boot para modernização")
    if linguagem == "Python" and "print(" in lower_content:
        pontos_atencao.append("Uso de prints diretos")
        sugestoes["boas_praticas"].append("Utilize logging para melhor controle")

    qtd_pontos = len(pontos_atencao)
    risco = "baixo"
    if qtd_pontos >= 4:
        risco = "alto"
    elif qtd_pontos >= 2:
        risco = "médio"

    return {
        "arquivo": str(caminho),
        "linguagem": linguagem,
        "resumo": resumo,
        "pontos_atencao": pontos_atencao,
        "sugestoes": sugestoes,
        "risco": risco,
    }


def gerar_documentacao_codigo(caminho: pathlib.Path, conteudo: str) -> str:
    """Gera documentação automática para um arquivo usando a OpenAI API."""
    ext = caminho.suffix.lower()
    linguagem = EXT_PARA_LINGUAGEM.get(ext, "Desconhecida")
    openai.api_key = os.getenv("OPENAI_API_KEY")
    prompt = (
        "Gere a documentação automática para o código a seguir.\n"
        f"Use o estilo da linguagem {linguagem}, como docstrings, Javadoc ou comentários explicativos.\n"
        "Não altere a lógica do código, apenas adicione comentários que ajudem a entendê-lo.\n\n"
        f"Código:\n{conteudo}"
    )
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        return resp["choices"][0]["message"]["content"]
    except Exception as exc:
        print(f"Aviso: falha ao documentar {caminho}: {exc}")
        return conteudo


def exibir_resultado_terminal(resultado: Dict) -> None:
    print(f"\n\U0001f4c4 {resultado['arquivo']}")
    print(f"Linguagem: {resultado['linguagem']}")
    print(f"Resumo: {resultado['resumo']}")
    print(f"Risco: {resultado['risco']}")
    if resultado.get("pontos_atencao"):
        print("Pontos de atenção:")
        for ponto in resultado["pontos_atencao"]:
            print(f" - {ponto}")
    if resultado.get("sugestoes"):
        for categoria, itens in resultado["sugestoes"].items():
            if itens:
                print(f"Sugestões - {categoria.replace('_', ' ').title()}:")
                for sugestao in itens:
                    print(f" - {sugestao}")


def salvar_json(
    resultados: List[Dict],
    caminho: pathlib.Path = pathlib.Path("codecompass_report.json"),
) -> None:
    with caminho.open("w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)


def salvar_markdown(
    resultados: List[Dict],
    caminho: pathlib.Path = pathlib.Path("codecompass_report.md"),
) -> None:
    linhas = ["# Relatório CodeCompass"]
    for r in resultados:
        linhas.append(f"\n## \U0001f4c4 {r['arquivo']}")
        linhas.append(f"**Linguagem:** {r['linguagem']}")
        linhas.append(f"**Resumo:** {r['resumo']}")
        linhas.append(f"**Risco:** {r['risco']}")
        if r.get("pontos_atencao"):
            linhas.append("### Pontos de atenção")
            for p in r["pontos_atencao"]:
                linhas.append(f"- {p}")
        if r.get("sugestoes"):
            for categoria, itens in r["sugestoes"].items():
                if itens:
                    linhas.append(
                        f"### Sugestões - {categoria.replace('_', ' ').title()}"
                    )
                    for s in itens:
                        linhas.append(f"- {s}")
    with caminho.open("w", encoding="utf-8") as f:
        f.write("\n".join(linhas))


def salvar_html(
    resultados: List[Dict],
    caminho: pathlib.Path = pathlib.Path("codecompass_report.html"),
) -> None:
    html = ["<html><body>", "<h1>Relatório CodeCompass</h1>"]
    for r in resultados:
        html.append(f"<h2>{r['arquivo']}</h2>")
        html.append(f"<p><strong>Linguagem:</strong> {r['linguagem']}</p>")
        html.append(f"<p><strong>Resumo:</strong> {r['resumo']}</p>")
        html.append(f"<p><strong>Risco:</strong> {r['risco']}</p>")
        if r.get("pontos_atencao"):
            html.append("<h3>Pontos de atenção</h3><ul>")
            for p in r["pontos_atencao"]:
                html.append(f"<li>{p}</li>")
            html.append("</ul>")
        if r.get("sugestoes"):
            for categoria, itens in r["sugestoes"].items():
                if itens:
                    html.append(
                        f"<h3>Sugestões - {categoria.replace('_', ' ').title()}</h3><ul>"
                    )
                    for s in itens:
                        html.append(f"<li>{s}</li>")
                    html.append("</ul>")
    html.append("</body></html>")
    with caminho.open("w", encoding="utf-8") as f:
        f.write("\n".join(html))


def salvar_excel(
    resultados: List[Dict],
    caminho: pathlib.Path = pathlib.Path("codecompass_report.xlsx"),
) -> None:
    """Gera um relatório gerencial em Excel."""
    import pandas as pd

    linhas = []
    for r in resultados:
        linhas.append(
            {
                "Arquivo": r["arquivo"],
                "Linguagem": r["linguagem"],
                "Resumo": r["resumo"],
                "Risco": r["risco"],
                "Pontos de Atenção": ", ".join(r["pontos_atencao"]),
                "Sugestões - Refatoração": ", ".join(r["sugestoes"]["refatoracao"]),
                "Sugestões - Modernização": ", ".join(r["sugestoes"]["modernizacao"]),
                "Sugestões - Boas Práticas": ", ".join(r["sugestoes"]["boas_praticas"]),
            }
        )
    df = pd.DataFrame(linhas)
    df.to_excel(caminho, index=False)


def main(arquivos: List[pathlib.Path]) -> None:
    resultados = []
    for caminho in arquivos:
        try:
            with caminho.open("r", encoding="utf-8", errors="ignore") as f:
                conteudo = f.read()
            resultado = analisar_codigo_conteudo(caminho, conteudo)
            resultados.append(resultado)
            exibir_resultado_terminal(resultado)
        except Exception as exc:
            print(f"Erro ao analisar {caminho}: {exc}")
    salvar_json(resultados)
    salvar_markdown(resultados)
    salvar_html(resultados)
    salvar_excel(resultados)
    print(
        "\n✅ Análise concluída. Relatórios salvos em: codecompass_report.json, codecompass_report.md, codecompass_report.html e codecompass_report.xlsx"
    )


def gerar_documentacao_arquivos(alvo: pathlib.Path) -> None:
    if alvo.is_dir():
        arquivos = listar_arquivos(alvo)
    else:
        arquivos = [alvo]
    ok: List[str] = []
    falha: List[str] = []
    for caminho in arquivos:
        try:
            with caminho.open("r", encoding="utf-8", errors="ignore") as f:
                conteudo = f.read()
            novo_conteudo = gerar_documentacao_codigo(caminho, conteudo)
            novo_nome = caminho.with_name(f"{caminho.stem}_doc{caminho.suffix}")
            with novo_nome.open("w", encoding="utf-8") as f:
                f.write(novo_conteudo)
            ok.append(str(novo_nome))
        except Exception as exc:
            print(f"Erro ao documentar {caminho}: {exc}")
            falha.append(str(caminho))
    if ok:
        print("\nArquivos documentados:")
        for o in ok:
            print(f" - {o}")
    if falha:
        print("\nFalha ao documentar:")
        for f in falha:
            print(f" - {f}")


if __name__ == "__main__":
    if "--docs" in sys.argv:
        idx = sys.argv.index("--docs")
        alvo = pathlib.Path(sys.argv[idx + 1]) if len(sys.argv) > idx + 1 else pathlib.Path(".")
        gerar_documentacao_arquivos(alvo)
        sys.exit(0)

    if len(sys.argv) > 1:
        alvo = pathlib.Path(sys.argv[1])
        if alvo.is_dir():
            arquivos = listar_arquivos(alvo)
        else:
            arquivos = [alvo]
    else:
        arquivos = listar_arquivos(pathlib.Path("."))
    main(arquivos)
