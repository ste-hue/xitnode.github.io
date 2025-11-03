---
layout: default
title: "xitnode"
---

# Basta cazzate

*Qui si scompongono le narrative fasulle.*

---

## La realtà è semplice

Il mondo è pieno di sistemi che ti fanno credere di essere più complicati di quello che sono. **xitnode** li decompone.

**Ogni post = una narrative che si rompe + gli strumenti per uscirne.**

Non è filosofia. È ingegneria inversa del controllo.

## Cosa trovi qui

**🔧 Codice che libera**  
Automazioni che tolgono potere a chi non dovrebbe averlo

**🎯 Analisi incarnata**  
Come funziona davvero il potere, senza ideologie

**📊 Dati contro propaganda**  
Numeri veri vs. storytelling istituzionale

**⚡ Strumenti pratici**  
Exit strategies che puoi usare oggi

## Ultimi post

<div class="posts-list">
{% for post in site.posts limit:5 %}
<div class="post-item">
  <h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
  <small>{{ post.date | date: "%d %b %Y" }}</small>
  {% if post.excerpt %}
  <p>{{ post.excerpt | strip_html | truncate: 100 }}</p>
  {% endif %}
</div>
{% endfor %}
</div>

---

## Perché esiste

L'Italia del 2025 è piena di gente che sa programmare, surfare, e vedere attraverso le stronzate ufficiali.

**xitnode** è per loro.

Non per cambiare il sistema. Per uscirne con stile.

---

*Input: narrative fasulle → Processing: decomposizione ricorsiva → Output: exit tools*

**[Tutti i post](/archive) • [Chi sono](/about)**

<div class="footer-timestamp">
  <small>Aggiornato: <span id="timestamp"></span></small>
</div>

<script>
(function() {
  var timestamp = document.getElementById('timestamp');
  if (timestamp) {
    var now = new Date();
    var options = {
      timeZone: 'Europe/Rome',
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    };
    timestamp.textContent = now.toLocaleString('it-IT', options);
  }
})();
</script>