---
layout: home
title: "xitnode"
---

# (define (exit x)

*portale d'uscita dalle narrative fasulle*

## Manifesto

**Xitnode non è un blog. È un portale d'uscita.**

```lisp
(if (trapped? x)
    (decompose x)
    (compose (exit (car x)) 
             (exit (cdr x))))
```

Un civic trickster che hackera sistemi di controllo con codice + vulnerabilità strategica.

**→ [Leggi il manifesto completo](/2025/06/07/manifesto-portale-uscita)**

## Cosa Troverai

- **Codice che libera** → automazioni che tolgono potere ai gatekeeper
- **Analisi sistemica incarnata** → come funziona davvero il potere  
- **Log di costruzione del controllo** → diari di "presa di potere" etica
- **Vulnerabilità come strategia** → onestà emotiva come arma

## Ultime Uscite

*Recent exits from the system:*

{% for post in site.posts limit:4 %}
- [{{ post.title }}]({{ post.url }}) — *{{ post.date | date: "%d/%m/%Y" }}*
{% endfor %}

<div class="live-timestamp">
  <small><em>Pagina aggiornata il: <span id="current-time"></span></em></small>
</div>

<script>
function updateTime() {
  const now = new Date();
  const options = { 
    year: 'numeric', 
    month: '2-digit', 
    day: '2-digit',
    hour: '2-digit', 
    minute: '2-digit',
    timeZone: 'Europe/Rome'
  };
  document.getElementById('current-time').textContent = now.toLocaleString('it-IT', options);
}

// Aggiorna ogni minuto
updateTime();
setInterval(updateTime, 60000);
</script>

---

*Output = (map think input)*

**Input** → **Decompose** → **Exit with tools**

[Mappa delle uscite](/archive) • [Chi sono davvero](/about)