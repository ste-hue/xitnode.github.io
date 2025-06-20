# Templates per Contenuti Xitnode

Questo directory contiene i template per i diversi tipi di contenuto del portale d'uscita.

## Tipi di Contenuto

### 1. Progetti Tecnico-Creativi
**File**: `template-progetto.md`
- Codice funzionante con contesto strategico
- Open source con impatto territoriale
- Automazioni che liberano dal controllo dei gatekeeper

### 2. Analisi Sistemica
**File**: `template-analisi.md`  
- Decostruzione di sistemi di controllo
- Governance, potere, strutture invisibili
- Basato su esperienza diretta, non teoria

### 3. Log Operativi
**File**: `template-log.md`
- Diari di "presa di potere" etica
- Strategie di indipendenza economica
- Case studies concreti

### 4. Riflessioni Esistenziali
**File**: `template-riflessione.md`
- Vulnerabilità strategica
- Dissonanze identitarie (Sud vs mondo)
- Onestà emotiva come materiale di costruzione

### 5. Guide Pratiche
**File**: `template-guida.md`
- Tools immediamente utilizzabili
- Mappe di uscita dai sistemi di dipendenza
- Step-by-step operativi

## Come Usare i Template

### Workflow Manuale (Template Diretti)
1. Copia il template appropriato
2. Rinomina con la data: `YYYY-MM-DD-titolo-slug.md`  
3. Aggiorna il frontmatter
4. Riempi le sezioni seguendo la struttura
5. Testa che tutto funzioni
6. Pubblica

### Workflow Obsidian (Conversione Automatica)
1. Scrivi l'articolo in Obsidian con nome naturale (es. `"Il Futuro dell'AI in Italia".md`)
2. Usa lo script di conversione automatica:
   - `./sync-obsidian.sh retro` - Date retroattive (oggi → indietro)
   - `./sync-obsidian.sh prog` - Date progressive (oggi → avanti)  
   - `./sync-obsidian.sh dry` - Anteprima senza convertire
3. Lo script aggiunge automaticamente:
   - Front matter Jekyll completo
   - Date sequenziali per pubblicazione
   - Sanitizzazione URL-safe dei titoli
4. Commit e push automatico

## Regole di Scrittura

- **Zero bullshit**: ogni parola deve essere utilizzabile
- **Ibrido per design**: tecnico + umano + politico sempre insieme
- **Vulnerabilità strategica**: errori come materiale di apprendimento
- **Open source del pensiero**: tutto replicabile
- **Codice + contesto**: mai tecnologia senza strategia

## Esempi di Titoli per Tipo

### Progetti
- "Hotel automation: togliere potere ai booking monopoli"
- "ETL pipeline che rende obsoleti i consulenti parassiti"
- "Sistema di gestione familiare: governance vs caos"

### Analisi
- "Come funziona davvero il controllo nelle PMI del Sud"
- "Booking.com vs indipendenza alberghiera: anatomia di un ricatto"
- "Eredità familiare: quando la tradizione è una trappola"

### Log
- "Settimana 3: da dipendente a controllore di sistemi"
- "Financial engineering per l'indipendenza: primi risultati"
- "Costruire autorità senza diventare un boss tossico"

### Riflessioni
- "Sud Italia vs Silicon Valley: quale è il vero tech hub?"
- "Vulnerabilità dichiarata come forma di potere"
- "Essere competenti E umani: falso dilemma"

### Guide
- "Exit strategy dai monopoli digitali: guida pratica"
- "Come automatizzare senza perdere l'anima"
- "Toolkit del civic hacker: essenziali per iniziare"