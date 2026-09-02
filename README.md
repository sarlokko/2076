# 2076

Trilogia di fantascienza ambientata nel 2076 (+ prequel sul tracollo).

## Ciclo

| Volume | Cartella | Stato |
|--------|----------|--------|
| **Libro I — 2076** | `capitoli/` | Completo (01–16) |
| **Libro II — Zenit** *(titolo provvisorio)* | `libro-2/` | Completo, prima stesura (01–16) |
| **Libro III — Eredità** *(titolo provvisorio)* | `libro-3/` | Completo, prima stesura (01–16) |
| **Prequel — Paolo** | `prequel/` | Scheletro |

_Vedi: [note/trilogia.md](note/trilogia.md)_

## Struttura

```
2076/
├── capitoli/          # Libro I
├── libro-2/           # Libro II (capitoli + note)
├── libro-3/           # Libro III (capitoli + note)
├── prequel/           # Prequel (scheletro)
├── personaggi/
├── ambientazione/
├── note/
├── bozze/
└── scripts/           # PDF / Kindle
```

## Premessa

Nel 2076 il pianeta è alimentato da energia solare orbitale. Il “dono” della luce diventa strumento di controllo (**Zenit**). Libro I: scoperta e leak. Libro II: rappresaglia dell’Alto e missione sulla Torre. Libro III (2084): eredità, figlia, **Orizzonte**.

## Export

### Libro I
- PDF: `capitoli/2076-capitoli-01-16.pdf`
- Kindle: `capitoli/2076-kindle.epub` / `.azw3`
- Script: `python3 scripts/genera_pdf_capitoli.py` · `python3 scripts/genera_kindle.py`

### Libro II
- PDF (range aggiornato a ogni run): `libro-2/capitoli/zenit-capitoli-01-16.pdf`
- Script: `python3 scripts/genera_pdf_libro2.py`

### Libro III
- PDF (range aggiornato a ogni run): `libro-3/capitoli/eredita-capitoli-01-16.pdf`
- Script: `python3 scripts/genera_pdf_libro3.py`
