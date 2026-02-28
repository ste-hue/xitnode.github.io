---
layout: default
title: "xitnode"
---

# Basta cazzate

*Qui si scompongono le narrative fasulle.*

---

C'era un tempo in cui sapevi distinguere. Prima che costruissero sistemi così eleganti da farti dubitare di quello che vedevi con i tuoi occhi.

**xitnode** non ti spiega niente. Ti ricorda quello che già sai.

Ogni post è uno strato che si stacca. Sotto, sempre la stessa cosa: un meccanismo che funziona solo finché non lo guardi.

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

Non è filosofia. Non è attivismo. È un faro acceso nel buio — non per illuminare tutto, ma per vedere chi risponde.

Se sei arrivato qui, forse stavi già cercando. Forse sapevi già che qualcosa non tornava. Questo posto esiste per quella frequenza.

---

**[Tutti i post](/archive) · [Chi sono](/about)**

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