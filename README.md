# 2076

Trilogia di fantascienza ambientata nel 2076 (+ prequel sul tracollo).

## Ciclo

| Volume | Cartella | Stato |
|--------|----------|--------|
| **Libro I — 2076** | `capitoli/` | Completo (01–16) |
| **Libro II — Zenit** *(titolo provvisorio)* | `libro-2/` | In corso |
| **Libro III** | — | Da aprire |
| **Prequel — Paolo** | `prequel/` | Scheletro |

_Vedi: [note/trilogia.md](note/trilogia.md)_

## Struttura

```
2076/
├── capitoli/          # Libro I
├── libro-2/           # Libro II (capitoli + note)
├── prequel/           # Prequel (scheletro)
├── personaggi/
├── ambientazione/
├── note/
├── bozze/
└── scripts/           # PDF / Kindle Libro I
```

## Premessa

Nel 2076 il pianeta è alimentato da energia solare orbitale. Il “dono” della luce diventa strumento di controllo (**Zenit**). Libro I: scoperta e leak. Libro II: rappresaglia dell’Alto e guinzaglio del punteggio — ritmo più action.

## Export

### Libro I
- PDF: `capitoli/2076-capitoli-01-16.pdf`
- Kindle: `capitoli/2076-kindle.epub` / `.azw3`
- Script: `python3 scripts/genera_pdf_capitoli.py` · `python3 scripts/genera_kindle.py`

### Libro II
- PDF (bozza, range aggiornato a ogni run): `libro-2/capitoli/zenit-capitoli-01-06.pdf`
- Script: `python3 scripts/genera_pdf_libro2.py`
