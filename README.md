**English** · [Português (Brasil)](README.pt-BR.md)

# faq-schema-parity-check

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) ![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)

`faq-schema-parity-check` is a free, open source tool that compares the
FAQ questions visible in a page's HTML with the `Question` nodes declared
in the JSON-LD `FAQPage`, and flags mismatches in both directions: a
visible question with no match in the schema, and a schema question with
no visible match on the page. It runs locally on an HTML file.

The default FAQ section markers are in Portuguese (plus "faq"), and the
tool prints its report in Brazilian Portuguese. You can pass your own
markers with `--marcador-faq`.

## Contents

- [Background](#background)
- [What it checks](#what-it-checks)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [FAQ](#faq)
- [Limitations](#limitations)
- [Methodology](#methodology)
- [Contributing](#contributing)
- [Author](#author)
- [License](#license)

## Background

This mismatch can keep a `FAQPage` from producing a rich result in Google
(Google checks whether the marked-up text matches what the visitor sees).
It can also lead an AI to cite, as an answer, a question that no longer
exists in the visible text. A schema left outdated after a content edit
is a silent bug that only shows up when someone audits both layers
together.

## What it checks

1. **Visible.** Headings (H2 to H4) ending in "?", found after a section
   heading such as "Perguntas frequentes" or "FAQ".
2. **Schema.** The `name` of each `Question` node referenced by the
   `mainEntity` or `hasPart` of a `FAQPage` node in the JSON-LD of the
   same page.
3. It compares both lists by normalized text and reports both sides of
   the mismatch.

## Requirements

Python 3.9 or newer. Standard library only, no external dependencies.

## Installation

```bash
git clone https://github.com/LucasFerrazSEO/faq-schema-parity-check.git
cd faq-schema-parity-check
```

## Usage

**1. Run it on the published HTML of the page.** The file needs both the
visible FAQ and the JSON-LD.

```bash
python faq_schema_parity_check.py pagina.html
```

**2. Read the report.** A real example, from a page with one visible
question missing from the schema and one schema question that no longer
exists in the text:

```
=== faq-schema-parity-check: faq.html ===
visíveis: 2 | no schema: 2

  ATENÇÃO  visível na página, ausente no FAQPage: "Quanto tempo demora?"
  ATENÇÃO  no FAQPage, ausente na página visível: "Vocês atendem em BH?"
```

Each ATENÇÃO (warning) line says which side is missing the question:
either the schema is outdated, or the visible text gained a new question
that the schema did not follow.

The exit code is 0 when there is full parity, 1 when there is any
mismatch, and 2 when the file cannot be read or no question is found on
either side.

**3. Adjust the FAQ section marker** if your site uses a heading other
than the defaults ("perguntas frequentes", "faq" and "dúvidas
frequentes"). Separate markers with commas.

```bash
python faq_schema_parity_check.py pagina.html --marcador-faq "perguntas frequentes,faq,dúvidas comuns"
```

## FAQ

**Is faq-schema-parity-check really free?**
Yes. It is open source under the MIT license.

**Does the tool fix the schema automatically?**
No. It only flags the mismatch. Deciding whether to fix the visible text
or the schema is an editorial call, not a mechanical one.

**Does it work if I do not have a section called "Perguntas frequentes"?**
Yes, as long as you pass the right heading with `--marcador-faq`. Without
a recognized marker, the tool does not know where the visible FAQ section
starts.

## Limitations

It depends on the visible FAQ section being marked by a recognizable
heading. The default covers "perguntas frequentes", "faq" and "dúvidas
frequentes"; add your site's variants with `--marcador-faq`. It does not
validate the answer content, only the presence and the text of the
question.

## Methodology

This is a generalization of a parity check used since 2026 in the
editorial process of [lucasferrazseo.com](https://lucasferrazseo.com),
where a FAQ edited without updating the schema used to be a recurring
bug.

## Contributing

Bug reports and suggestions are welcome through [GitHub Issues](https://github.com/LucasFerrazSEO/faq-schema-parity-check/issues).

## Author

[Lucas Ferraz](https://lucasferraz.com) is an SEO, website development and Generative Engine Optimization specialist and the founder of [Lucas Ferraz SEO](https://lucasferrazseo.com).

## License

MIT. See [LICENSE](LICENSE).
