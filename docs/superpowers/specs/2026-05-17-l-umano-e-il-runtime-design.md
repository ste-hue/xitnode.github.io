# Design — "L'Umano è il Runtime"

Next xitnode article. Spine: **l'umano è il runtime** — i sistemi sono cognitivamente
stateless, quindi un umano diventa il runtime che porta lo stato tra una chiamata e
l'altra. La fonte è il pattern "LLM Wiki" più un thread di ansia AI da Twitter; il
documento sorgente non è un articolo sul note-taking, è sull'**escape della
ricomputazione**.

## Decisioni

- **Lingua:** corpo in italiano, registro xitnode, con termini tecnici inglesi inline
  (`runtime`, `RAG`, `phase transition`, `synthesis`, `retrieval`, `state`). Coerente
  con la cadenza 2026 (compilatore umano, ambiguità costosa, canonical language).
- **Data / ordine:** questo è il post del 2026-05-17. `il-compilatore-umano` viene
  spostato a 2026-05-24 (rinomina file + aggiorna `date:` nel frontmatter).
- **Posizione:** `_drafts/2026-05-17-l-umano-e-il-runtime.md` (draft, come gli altri;
  la pipeline lo promuove a `_posts/`).
- **Footer:** nessun footer `Co-Authored-By` né riga data — i post pubblicati
  (`ambiguità costosa`, `canonical language`) non lo portano.
- **Ending:** solo diagnosi. Nessuna sezione "cosa fare": l'exit (persistent
  synthesis) è già consegnato in §7. Si chiude sulla riga del burnout.

## Frontmatter

```yaml
---
layout: post
title: "L'Umano è il Runtime"
date: 2026-05-17
categories: [xitnode]
tags: [runtime-umano, ricomputazione, persistent-synthesis, memoria-operativa, phase-transition]
---
```

## Diagrammi

Tre SVG forniti dall'utente, da copiare in `assets/images/` mantenendo i nomi:

- `assets/images/01-human-runtime.svg`
- `assets/images/02-phase-transition.svg`
- `assets/images/03-two-loops.svg`

Sorgente: `/Users/stefanodellapietra/Downloads/excalidras/`. Le label interne agli SVG
restano in inglese (come la diagram a 5 layer in `ambiguità costosa`).

Embed con il blocco standard usato dagli altri post:

```html
<p style="text-align: center;"><img src="/assets/images/NOME.svg" alt="ALT" style="max-width: 800px; width: 100%; height: auto;"></p>
```

Regola di posizionamento: ogni diagramma cade **dopo** che l'idea è stata enunciata in
prosa — cristallizza, non anticipa.

## Struttura — ~10 sezioni brevi

Intro headerless. Ogni sezione distilla un blocco della prosa sorgente inglese; la
resa italiana deve restare fedele al ritmo (frasi corte, righe isolate, niente
retorica).

1. **(intro, no header)** — I sistemi moderni sono cognitivamente stateless. Non
   tecnicamente: cognitivamente. L'informazione esiste, la sintesi non persiste,
   quindi ogni interazione ricomincia.
2. **`## Ricomputazione`** — La lista dei ricominci (meeting, manager, consulente,
   reorg, onboarding, quarter). L'organizzazione sembra complessa, ma gran parte
   della complessità è solo ricomputazione.
3. **`## RAG Rende Visibile il Pattern`** — RAG espone il pattern: upload, retrieve
   fragments, improvisa coerenza al query time. Ancora. E ancora. Niente si accumula.
4. **`## Il Software è Vuoto`** — CRM/ERP/ticketing/Slack/Drive/Email immagazzinano
   frammenti. Il software immagazzina dati, le persone immagazzinano stato.
   Sostituire un operatore → amnesia sistemica. "Chiedi all'amministrazione." Chiude
   su: **"L'umano diventa il runtime di un sistema non computabile."**
   → **SVG 1 `01-human-runtime.svg`** subito dopo questa riga.
5. **`## Ricomputazione Socialmente Costosa`** — Perché il lavoro white-collar
   stanca: non è fatica fisica, è ricomputazione socialmente costosa (ricostruire
   contesto, sincronizzare memoria, tradurre ambiguità, riscoprire intent, portare
   stato a mano tra sistemi scollegati). I meeting non producono valore: riparano
   memory loss.
6. **`## L'Ambiguità Diventa Infrastruttura`** — Quando il contesto è non
   documentato: gli intermediari diventano necessari, l'opacità diventa job
   security. L'ambiguità smette di essere un bug, diventa infrastruttura.
7. **`## La Vera Transizione di Fase`** — La transizione di fase nascosta nei
   discorsi AI non è "AI sostituisce i lavoratori" — è "persistent synthesis
   sostituisce la ricomputazione". Chiude su: **"Il punto non è il retrieval. È
   l'accumulazione."** → **SVG 2 `02-phase-transition.svg`** subito dopo questa riga.
   Poi la coda: quando l'interpretazione persiste — contraddizioni visibili,
   decisioni che sopravvivono, memoria operativa che si compone, contesto
   ispezionabile — il sistema diventa più computabile, e cambiano le economie di
   intere categorie di lavoro.
8. **`## La Paura Vera è la Demistificazione`** — L'ansia AI raccontata come paura di
   disoccupazione è incompleta. La paura più profonda è la demistificazione: lo
   status veniva dall'essere il ponte tra contesti frammentati; quando il ponte
   diventa infrastruttura, si scopre che l'organizzazione non mancava di
   informazione — mancava di interpretazione persistente.
9. **`## Sistemi Limitati Accumulano`** — Perché un piccolo ristorante può sembrare
   più stabile di un ambiente corporate ben pagato. Non perché la povertà è pura: i
   sistemi limitati accumulano memoria per natura. Il proprietario vede clienti,
   inventario, staff, cassa, conseguenze. I loop si chiudono fisicamente. Chiude su:
   **"La realtà persiste abbastanza a lungo da stabilizzarsi."**
   → **SVG 3 `03-two-loops.svg`** subito dopo questa riga.
10. **`## Quando l'Umano è il Runtime`** — Molti sistemi corporate fanno l'opposto:
    distruggono e ricostruiscono contesto in continuazione, niente si compone tranne
    lo stress. Gli umani compensano: diventano memoria, sincronizzazione,
    traduzione, continuità, runtime. Chiude su: **"Non è un effetto collaterale. È un
    costo infrastrutturale."**

## Resa italiana — note di registro

- Frasi corte. Righe isolate per le frasi-chiave (come `ambiguità costosa`).
- Termini tecnici inglesi inline, non tradotti: `runtime`, `RAG`, `retrieval`,
  `synthesis`, `phase transition`, `state`, `stateless`, `job security`.
- Bullet list dove la prosa sorgente elenca (i ricominci, le forme di ricomputazione,
  le conseguenze della persistenza).
- Non persuadere, non motivare. Descrivere il sistema in termini di componenti,
  flussi, failure mode.
- Connessione implicita al thread esistente (`compilatore umano`, `ambiguità
  costosa`): la frase "sistema non computabile" è già nel lessico del blog. Nessuna
  citazione esplicita degli altri post.

## Lavoro collaterale

Spostare il draft `il-compilatore-umano`:

- Rinominare `_drafts/2026-05-17-il-compilatore-umano.md` →
  `_drafts/2026-05-24-il-compilatore-umano.md`.
- Aggiornare `date: 2026-05-17` → `date: 2026-05-24` nel frontmatter.

## Criterio di completamento

- Nuovo draft `_drafts/2026-05-17-l-umano-e-il-runtime.md` esiste, corpo in italiano,
  ~10 sezioni, 3 diagrammi embeddati nelle posizioni indicate.
- 3 SVG presenti in `assets/images/`.
- `il-compilatore-umano` rinominato e ridatato a 2026-05-24.
- `bundle exec jekyll build` (o lo script di build del repo) completa senza errori e
  la pagina del post rende i 3 diagrammi.
