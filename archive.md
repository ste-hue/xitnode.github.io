---
layout: page
title: "Archivio Completo"
permalink: /archive/
---

# Archivio dei Pensieri

*Tutti i post ordinati per data, con timestamp sempre aggiornati*

<div class="archive-info">
  <p><strong>Ultimo controllo archivio:</strong> <span id="archive-timestamp"></span></p>
</div>

## Posts per Anno

{% assign posts_by_year = site.posts | group_by_exp: 'post', 'post.date | date: "%Y"' %}
{% for year in posts_by_year %}

### {{ year.name }}

{% for post in year.items %}
<div class="archive-entry">
  <div class="archive-date">
    <strong>{{ post.date | date: "%d/%m/%Y" }}</strong>
    <small class="original-date">pubblicato</small>
  </div>
  <div class="archive-content">
    <h4><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h4>
    {% if post.categories.size > 0 %}
      <div class="archive-categories">
        {% for category in post.categories %}
          <span class="category-tag">{{ category }}</span>
        {% endfor %}
      </div>
    {% endif %}
    {% if post.tags.size > 0 %}
      <div class="archive-tags">
        {% for tag in post.tags %}
          <span class="tag">#{{ tag }}</span>
        {% endfor %}
      </div>
    {% endif %}
  </div>
</div>
{% endfor %}

{% endfor %}

---

## Statistiche Archivio

<div class="archive-stats">
  <div class="stat">
    <strong>{{ site.posts.size }}</strong><br>
    <small>Post totali</small>
  </div>
  <div class="stat">
    <strong>{{ posts_by_year.size }}</strong><br>
    <small>Anni attivi</small>
  </div>
  <div class="stat">
    <strong id="days-since-first"></strong><br>
    <small>Giorni dal primo post</small>
  </div>
</div>

[← Torna alla home]({{ '/' | relative_url }})

<script>
function updateArchiveTimestamp() {
  const now = new Date();
  const options = { 
    year: 'numeric', 
    month: '2-digit', 
    day: '2-digit',
    hour: '2-digit', 
    minute: '2-digit',
    second: '2-digit',
    timeZone: 'Europe/Rome'
  };
  document.getElementById('archive-timestamp').textContent = now.toLocaleString('it-IT', options);
}

function calculateDaysSinceFirst() {
  // Data del primo post (dalla variabile Jekyll)
  {% assign first_post = site.posts | last %}
  const firstPostDate = new Date('{{ first_post.date | date: "%Y-%m-%d" }}');
  const today = new Date();
  const diffTime = Math.abs(today - firstPostDate);
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  document.getElementById('days-since-first').textContent = diffDays;
}

// Inizializza
updateArchiveTimestamp();
calculateDaysSinceFirst();

// Aggiorna timestamp ogni 30 secondi
setInterval(updateArchiveTimestamp, 30000);
</script>

<style>
.archive-info {
  background: #f8f9fa;
  padding: 1em;
  border-radius: 5px;
  margin-bottom: 2em;
  text-align: center;
}

.archive-entry {
  display: flex;
  margin-bottom: 1.5em;
  padding-bottom: 1em;
  border-bottom: 1px solid #eee;
}

.archive-date {
  min-width: 120px;
  margin-right: 1.5em;
  text-align: right;
}

.archive-date .original-date {
  display: block;
  color: #666;
  font-size: 0.8em;
}

.archive-content {
  flex: 1;
}

.archive-content h4 {
  margin: 0 0 0.5em 0;
}

.archive-content h4 a {
  text-decoration: none;
  color: #333;
}

.archive-content h4 a:hover {
  color: #007acc;
}

.archive-categories {
  margin: 0.5em 0;
}

.category-tag {
  background: #e3f2fd;
  color: #1565c0;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.8em;
  margin-right: 5px;
}

.archive-tags {
  margin: 0.5em 0;
}

.archive-tags .tag {
  background: #f0f0f0;
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 0.75em;
  margin-right: 5px;
  color: #666;
}

.archive-stats {
  display: flex;
  justify-content: space-around;
  background: #f5f5f5;
  padding: 1.5em;
  border-radius: 8px;
  margin: 2em 0;
}

.stat {
  text-align: center;
}

.stat strong {
  font-size: 1.5em;
  color: #333;
}

.stat small {
  color: #666;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

@media (max-width: 600px) {
  .archive-entry {
    flex-direction: column;
  }
  
  .archive-date {
    min-width: auto;
    margin-right: 0;
    margin-bottom: 0.5em;
    text-align: left;
  }
  
  .archive-stats {
    flex-direction: column;
    gap: 1em;
  }
}
</style>