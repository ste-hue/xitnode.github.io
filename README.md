# xitnode

Blog personale di **ste-hue** pubblicato con [GitHub Pages](https://pages.github.com/)

🌐 **Live**: [ste-hue.github.io/xitnode](https://ste-hue.github.io/xitnode)

## Setup

Questo blog usa Jekyll con il tema `minima`. La struttura è intenzionalmente minimale:

```
xitnode/
├── _config.yml          # Configurazione Jekyll
├── index.md            # Homepage
├── _posts/             # Post del blog
│   ├── 2024-01-15-primo-post.md
│   └── 2024-01-20-tools-minimal.md
├── assets/             # Immagini, CSS, JS
└── README.md           # Questo file
```

## Deploy

### Prima volta

```bash
git init
git remote add origin https://github.com/ste-hue/xitnode.github.io
git add .
git commit -m "Primo deploy"
git push -u origin main
```

### Aggiornamenti

```bash
git add .
git commit -m "Nuovo post: titolo"
git push
```

## Scrivere un post

1. Crea un file in `_posts/` con formato: `YYYY-MM-DD-titolo-del-post.md`
2. Aggiungi il front matter:

```yaml
---
layout: post
title: "Titolo del Post"
date: YYYY-MM-DD
categories: [categoria1, categoria2]
tags: [tag1, tag2]
---
```

3. Scrivi il contenuto in Markdown
4. Commit e push

## Test locale

```bash
# Installa Jekyll (una volta)
gem install jekyll bundler

# Serve il sito localmente
jekyll serve

# Apri http://localhost:4000
```

## Filosofia

**Minimale**. **Diretto**. **Funzionale**.

Niente fronzoli, solo contenuto che vale la pena condividere.

---

*Costruito con ❤️ e Jekyll*