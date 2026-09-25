#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
faq-schema-parity-check — compara as perguntas de FAQ visíveis no HTML de
uma página contra os nós `Question` declarados no `FAQPage` do JSON-LD, e
aponta divergência nos dois sentidos.

O QUE FAZ
    Extrai duas listas de perguntas da mesma página:

    1. **Visível.** Headings (H2-H4) que terminam em "?", localizados depois
       de um heading de seção do tipo "Perguntas frequentes" / "FAQ"
       (heurística configurável por --marcador-faq).
    2. **Schema.** Os `name` de cada nó `Question` referenciado pelo
       `mainEntity`/`hasPart` de um nó `FAQPage` no JSON-LD da página.

    Depois compara as duas listas (por texto normalizado) e reporta:
    pergunta visível sem par no schema, pergunta no schema sem par visível
    na página. Essa divergência é o motivo mais comum de um FAQPage não
    gerar rich result no Google, ou de uma IA citar uma pergunta que já não
    existe mais no texto.

USO
    python faq_schema_parity_check.py pagina.html
    python faq_schema_parity_check.py pagina.html --marcador-faq "perguntas frequentes,faq,dúvidas comuns"

LIMITAÇÕES
    Depende de a seção de FAQ visível estar marcada por um heading
    reconhecível (o padrão cobre "perguntas frequentes" e "faq"; adicione
    variantes com --marcador-faq). Não valida o conteúdo da resposta, só a
    presença e o texto da pergunta.

Autor: Lucas Ferraz (lucasferraz.com) — dependência zero, só biblioteca padrão.
Licença: MIT.
"""
from __future__ import annotations

import argparse
import json
import re
import sys

BLOCO_JSONLD = re.compile(
    r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
    re.I | re.S,
)


def strip_tags(html: str) -> str:
    html = re.sub(r"(?is)<(script|style).*?</\1>", " ", html)
    return re.sub(r"(?s)<[^>]+>", " ", html)


def normaliza(texto: str) -> str:
    return re.sub(r"\s+", " ", texto).strip()


def chave(texto: str) -> str:
    return re.sub(r"[^\w]+", "", normaliza(texto).lower())


def perguntas_visiveis(html: str, marcadores: list[str]) -> list[str]:
    partes = re.split(r"(?is)(<h[234][^>]*>.*?</h[234]>)", html)
    perguntas: list[str] = []
    dentro_faq = False
    i = 1
    while i < len(partes):
        texto = normaliza(strip_tags(partes[i]))
        baixo = texto.lower().rstrip("?").strip()
        if any(baixo == m or baixo.startswith(m + " ") for m in marcadores):
            dentro_faq = True
        elif dentro_faq and texto.endswith("?"):
            perguntas.append(texto)
        i += 2
    return perguntas


def perguntas_schema(html: str) -> list[str]:
    perguntas: list[str] = []
    for bloco in BLOCO_JSONLD.findall(html):
        try:
            doc = json.loads(bloco)
        except json.JSONDecodeError:
            continue
        grafo = doc.get("@graph", [doc])
        ids = {n.get("@id"): n for n in grafo if isinstance(n, dict) and n.get("@id")}
        for no in grafo:
            if not isinstance(no, dict) or no.get("@type") != "FAQPage":
                continue
            partes = no.get("mainEntity") or no.get("hasPart") or []
            if isinstance(partes, dict):
                partes = [partes]
            for p in partes:
                if isinstance(p, dict) and "@id" in p and p["@id"] in ids:
                    p = ids[p["@id"]]
                if isinstance(p, dict) and p.get("name"):
                    perguntas.append(normaliza(p["name"]))
    return perguntas


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Compara perguntas de FAQ visíveis no HTML contra o FAQPage no JSON-LD."
    )
    ap.add_argument("arquivo", help="arquivo .html")
    ap.add_argument("--marcador-faq", default="perguntas frequentes,faq,dúvidas frequentes",
                     help="headings, separados por vírgula, que marcam o início da seção de FAQ visível")
    args = ap.parse_args()

    try:
        with open(args.arquivo, encoding="utf-8") as fh:
            html = fh.read()
    except OSError as exc:
        print(f"Não consegui ler {args.arquivo}: {exc}", file=sys.stderr)
        sys.exit(2)

    marcadores = [m.strip().lower() for m in args.marcador_faq.split(",") if m.strip()]
    visiveis = perguntas_visiveis(html, marcadores)
    do_schema = perguntas_schema(html)

    chaves_visiveis = {chave(p): p for p in visiveis}
    chaves_schema = {chave(p): p for p in do_schema}

    so_visivel = [p for k, p in chaves_visiveis.items() if k not in chaves_schema]
    so_schema = [p for k, p in chaves_schema.items() if k not in chaves_visiveis]

    print(f"\n=== faq-schema-parity-check: {args.arquivo} ===")
    print(f"visíveis: {len(visiveis)} | no schema: {len(do_schema)}\n")

    if not visiveis and not do_schema:
        print("Nenhuma pergunta encontrada (nem visível, nem no schema). Confira --marcador-faq.")
        sys.exit(2)

    for p in so_visivel:
        print(f"  ATENÇÃO  visível na página, ausente no FAQPage: \"{p[:70]}\"")
    for p in so_schema:
        print(f"  ATENÇÃO  no FAQPage, ausente na página visível: \"{p[:70]}\"")
    if not so_visivel and not so_schema:
        print("  Paridade completa: toda pergunta visível está no schema, e vice-versa.")

    sys.exit(1 if (so_visivel or so_schema) else 0)


if __name__ == "__main__":
    main()
