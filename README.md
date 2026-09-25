# faq-schema-parity-check — ferramenta grátis e de código aberto de paridade FAQ × schema

`faq-schema-parity-check` é uma ferramenta gratuita e de código aberto que
compara as perguntas de FAQ visíveis no HTML de uma página contra os nós
`Question` declarados no `FAQPage` do JSON-LD, e aponta divergência nos
dois sentidos: pergunta visível sem par no schema, pergunta no schema sem
par visível na página.

## Por que isso importa

Essa divergência é o motivo mais comum de um `FAQPage` não gerar rich
result no Google (o Google confere se o texto marcado bate com o que a
pessoa vê), e é também um jeito de uma IA citar como resposta uma pergunta
que já não existe mais no texto visível — schema desatualizado depois de
uma edição de conteúdo é um bug silencioso que só aparece quando alguém
audita as duas camadas juntas.

## O que a ferramenta verifica

1. **Visível** — headings (H2-H4) terminando em "?", localizados depois
   de um heading de seção como "Perguntas frequentes" ou "FAQ".
2. **Schema** — os `name` de cada nó `Question` referenciado pelo
   `mainEntity`/`hasPart` de um nó `FAQPage` no JSON-LD da mesma página.
3. Compara as duas listas por texto normalizado e reporta os dois lados
   da divergência.

## Instalação

Só biblioteca padrão do Python (3.9 ou mais recente). Sem dependência
externa.

```bash
git clone https://github.com/lucasferrazseo/faq-schema-parity-check.git
cd faq-schema-parity-check
```

## Como usar, passo a passo

**1. Rode contra o HTML publicado da página** (precisa ter tanto o FAQ
visível quanto o JSON-LD no mesmo arquivo):

```bash
python faq_schema_parity_check.py pagina.html
```

**2. Leia o relatório.** Exemplo real, de uma página com uma pergunta
visível fora do schema e uma pergunta no schema que não existe mais no
texto:

```
=== faq-schema-parity-check: faq.html ===
visíveis: 2 | no schema: 2

  ATENÇÃO  visível na página, ausente no FAQPage: "Quanto tempo demora?"
  ATENÇÃO  no FAQPage, ausente na página visível: "Vocês atendem em BH?"
```

Cada linha de ATENÇÃO já diz de que lado está a falta — se é o schema que
ficou desatualizado, ou se é o texto visível que ganhou uma pergunta nova
sem o schema acompanhar.

**3. Ajuste o marcador de seção de FAQ**, se o seu site usa um heading
diferente de "Perguntas frequentes" ou "FAQ":

```bash
python faq_schema_parity_check.py pagina.html --marcador-faq "perguntas frequentes,faq,dúvidas comuns"
```

## Perguntas frequentes

**faq-schema-parity-check é realmente grátis?**
Sim, código aberto sob licença MIT.

**A ferramenta corrige o schema automaticamente?**
Não. Só aponta a divergência; decidir se corrige o texto visível ou o
schema é editorial, não mecânico.

**Funciona sem eu ter uma seção chamada "Perguntas frequentes"?**
Funciona, desde que você informe o heading certo com `--marcador-faq`. Sem
um marcador reconhecido, a ferramenta não sabe onde a seção de FAQ visível
começa.

## Limitações

Depende de a seção de FAQ visível estar marcada por um heading
reconhecível — o padrão cobre "perguntas frequentes" e "faq"; adicione
variantes do seu site com `--marcador-faq`. Não valida o conteúdo da
resposta, só a presença e o texto da pergunta.

## Método e origem

Generalização de uma checagem de paridade usada desde 2026 no processo
editorial de [lucasferrazseo.com](https://lucasferrazseo.com), onde um FAQ
editado sem atualizar o schema já foi bug recorrente.

## Autor

[Lucas Ferraz](https://lucasferraz.com) — especialista em SEO, criação de
sites e SEO para IA, fundador da [Lucas Ferraz SEO](https://lucasferrazseo.com).

## Licença

MIT — ver [LICENSE](LICENSE).
