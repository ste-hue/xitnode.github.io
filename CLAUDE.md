# CLAUDE.md

## Project

Jekyll blog deployed on GitHub Pages at xitnode.com. Newsletter via Resend API.

## Identity

xitnode è un trasformatore ricorsivo di pensieri. Le idee complesse vengono decomposte, semplificate e raffinate fino alla loro essenza atomica.

```scheme
(define (think x)
  (if (atomic? x)
      x
      (map think (simplify (decompose x)))))
```

Processo: Input grezzo → Scomponi → Semplifica → Ricorri → Output atomico.

exit + node = punti di partenza che si connettono ad altri punti di partenza. Ogni insight è sia una fine (della confusione) che un inizio (di chiarezza).

Niente fronzoli, niente riempitivi. Ogni post distilla qualcosa di complesso in qualcosa di pratico. Modelli di pensiero, non solo conclusioni.

## Writing Style

Write as if these are architecture notes written mid-build.

Prioritize clarity under stress over elegance.

Assume the reader is intelligent but busy.

State constraints, assumptions, and tradeoffs explicitly.

Describe systems in terms of components, flows, and failure modes.

Explain *why* choices were made, including what was rejected and why.

Do not persuade. Do not motivate. Do not perform.

Avoid grand claims, emotional framing, and rhetorical padding.

Prefer plain language, short sentences, and precise terms.

Use structure only where it reduces ambiguity.

If a sentence does not increase understanding of how the system holds or breaks, remove it.

Write to make the system maintainable, not to earn approval.
