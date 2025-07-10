import json
import pathlib
import sys
from typing import List, Dict

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

def analisar_codigo_conteudo(caminho: pathlib.Path, conteudo: str) -> Dict:
    ext = caminho.suffix.lower()
    linguagem = EXT_PARA_LINGUAGEM.get(ext, "Desconhecida")
    resumo = f"Arquivo com {len(conteudo.splitlines())} linhas."
    pontos_atencao: List[str] = []
    sugestoes: List[str] = []
    return {
        "arquivo": str(caminho),
        "linguagem": linguagem,
        "resumo": resumo,
        "pontos_atencao": pontos_atencao,
        "sugestoes": sugestoes,
    }

def exibir_resultado_terminal(resultado: Dict) -> None:
    print(f"\n\U0001F4C4 {resultado['arquivo']}")
    print(f"Linguagem: {resultado['linguagem']}")
    print(f"Resumo: {resultado['resumo']}")
    if resultado.get("pontos_atencao"):
        print("Pontos de atenção:")
        for ponto in resultado["pontos_atencao"]:
            print(f" - {ponto}")
    if resultado.get("sugestoes"):
        print("Sugestões:")
        for sugestao in resultado["sugestoes"]:
            print(f" - {sugestao}")

def salvar_json(resultados: List[Dict], caminho: pathlib.Path = pathlib.Path("codecompass_report.json")) -> None:
    with caminho.open("w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)

def salvar_markdown(resultados: List[Dict], caminho: pathlib.Path = pathlib.Path("codecompass_report.md")) -> None:
    linhas = ["# Relatório CodeCompass"]
    for r in resultados:
        linhas.append(f"\n## \U0001F4C4 {r['arquivo']}")
        linhas.append(f"**Linguagem:** {r['linguagem']}")
        linhas.append(f"**Resumo:** {r['resumo']}")
        if r.get("pontos_atencao"):
            linhas.append("### Pontos de atenção")
            for p in r["pontos_atencao"]:
                linhas.append(f"- {p}")
        if r.get("sugestoes"):
            linhas.append("### Sugestões")
            for s in r["sugestoes"]:
                linhas.append(f"- {s}")
    with caminho.open("w", encoding="utf-8") as f:
        f.write("\n".join(linhas))

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
    print("\n✅ Análise concluída. Relatórios salvos em: codecompass_report.json e codecompass_report.md")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        arquivos = [pathlib.Path(a) for a in sys.argv[1:]]
    else:
        arquivos = [p for p in pathlib.Path('.').glob('*') if p.is_file()]
    main(arquivos)
