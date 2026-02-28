---
layout: post
title: "Palantir Artigianale: Ontologia per Piccole Imprese"
date: 2026-02-28
categories: [xitnode]
tags: [systems, ontology, knowledge-graph, family-business, exit-strategies]
---

**Come ho applicato intelligence-grade knowledge graphs alla gestione di un hotel familiare**

---

*Palantir costruisce grafi di intelligence per governi e multinazionali. Io ne ho fatto uno per gestire due società che operano nello stesso immobile. Stessa logica, scala diversa, problemi sorprendentemente simili.*

---

## Il Problema Originale

Hai presente quella sensazione quando sai che qualcosa è andato storto, ma non riesci a capire *dove* nei tuoi sistemi?

Gennaio 2026. Due società, chiamiamole **Alpha** (proprietaria dell'immobile) e **Beta** (operatore turistico). Beta paga affitto ad Alpha. Entrambe hanno debiti bancari. Entrambe generano revenue. Sulla carta, tutto quadra.

Poi arrivano i P&L mensili di Beta:
- **Revenue**: €4.3M annui
- **Costi operativi**: €325k
- **EBITDA**: €3.7M (86% margin!)

Un commercialista guarda questi numeri e dice: "Ottimo, sani come un pesce."

Io guardo questi numeri e penso: "Qualcosa non torna."

Perché? Perché **manca il contesto**. Quei P&L erano *standalone*, pre-consolidamento. Beta non aveva ancora dedotto l'affitto di €732k/anno pagato ad Alpha. Il vero EBITDA consolidato? **€977k**.

Differenza: €3.7M → €977k.

DSCR (Debt Service Coverage Ratio) percepito: **6.0x** (sembriamo invincibili)
DSCR reale consolidato: **1.58x** (sostenibile ma marginal)

Un errore del genere, presentato a una banca, e ti strozzano il finanziamento. O peggio: te lo danno, poi dopo 12 mesi scopri di non reggere il debt service.

---

## Il Vero Problema: Linguaggi Incompatibili

Il problema *tecnico* era semplice: dati standalone vs consolidati.

Il problema *sistemico* era più profondo: **ogni sistema parlava una lingua diversa**.

- **PMS** (Property Management System): camere, prenotazioni, ospiti
- **eSolver** (contabilità): mastri, partite, fatture
- **TeamSystem** (ERP): budget, forecast, cespiti
- **Excel** (everywhere): quello che l'umano capisce

Quando dico "Revenue di Beta", intendo:
- Il totale fatturato nel PMS?
- Il revenue riconosciuto in contabilità (competenza)?
- Il revenue incassato (cassa)?
- Il revenue *prima* o *dopo* l'affitto infragruppo?

Quattro sistemi, quattro risposte diverse. E in mezzo, un commercialista che fa da traduttore manuale, creando Excel bridge che diventano spaghetti code in 6 mesi.

**Questo** è il problema che Palantir risolve per la CIA. E questo è il problema che avevo io, in scala 1:100.

---

## La Soluzione: Ontologia come Linguaggio Comune

Un'ontologia, nel senso di Palantir, non è un database. È un **contratto semantico**: definisci *una volta* cosa significa ogni entità e come si relazionano.

### Layer 1: Entities (Chi/Cosa)

Invece di tabelle, definisci **tipi di cose che esistono**:

```
Companies:
  - Alpha (asset owner, 75% famiglia)
  - Beta (operator, 24.62% owned by Alpha)

Assets:
  - Hotel Panorama (owned by Alpha, rented to Beta)
  - Beach Club (owned by Alpha, operated by Beta)
  - Apartments CVM (owned by Alpha, idle)

Debt Instruments:
  - Mutuo_MPS_Beta (€3.5M, 4.16%, scadenza 2039)
  - Mutuo_Intesa_Alpha (€700k residual, 5.2%, scadenza 2031)
  - ... (5 loans totali)

People:
  - Stefano Sr (AU Beta, decision maker)
  - Antonio (GM, operational control)
  - Roberto (consultant, financial advisor)
```

Ogni entità ha un **file markdown** in Obsidian con:
- Metadata (type, status, date created)
- Attributi core (importi, scadenze, ownership)
- **Wikilinks** ad altre entità (`[[Alpha]]`, `[[Mutuo_MPS_Beta]]`)

### Layer 2: Relationships (Chi fa cosa a chi)

Le relazioni *non* sono foreign keys in un DB. Sono **fatti dichiarati**:

```
[[Beta]] --pays_rent--> [[Alpha]]
  amount: €732k/anno
  type: affitto_azienda (non solo immobile: licenze + goodwill)

[[Alpha]] --owns_stake--> [[Beta]]
  percentage: 24.62%
  invested: €3M (01/04/2025)

[[Beta]] --services_debt--> [[Mutuo_MPS_Beta]]
  annual_payment: €332k (dal 2026)

[[Alpha]] --services_debt--> [[Mutuo_Intesa_Alpha]]
  annual_payment: €82.8k
```

Queste relazioni sono **bidirezionali** in Obsidian: cliccando su `[[Beta]]` vedi tutti i file che la menzionano. È un grafo, non una gerarchia.

### Layer 3: Events (Cosa è successo quando)

Gli eventi vivono nel **journal settimanale**:

```markdown
### Mon 03 Feb - P&L Reconciliation Discovery

Scoperto che P&L mensili Beta erano pre-rent.
Consolidato reale: EBITDA €977k (non €3.7M).
DSCR corretto: 1.58x.

Action: Aggiornato [[GRUPPO_PANORAMA.md]] con view consolidata.
Updated: [[DEBT_SUMMARY.md]], [[Beta.md]], [[Alpha.md]]
```

Il journal è **la timeline**. L'ontologia è **lo stato attuale**. Insieme, sono la memoria persistente del sistema.

---

## Pattern 1: Communicating Vessels

Il primo pattern emerso: **le entità non sono isolate, sono vasi comunicanti**.

Beta genera revenue (€4.14M), ma paga affitto ad Alpha (€732k). Alpha incassa affitto, ma paga il suo debt (€142k/anno nel 2026). Entrambi contribuiscono al debt service consolidato di **€619k/anno**.

Guardare Beta standalone è **sbagliato per design**. Il sistema è fatto per essere visto a livello gruppo.

Nel file `GRUPPO_PANORAMA.md`:

```markdown
## Consolidated Performance 2025

**Revenue**: €5.31M (Beta operations + Alpha rent income)
**EBITDA**: €977k (18.4% margin)
**Debt Service 2026**: €619k
**DSCR**: 1.58x (sustainable)

### Stress Tests
- Revenue -20% → DSCR 1.26x (marginal but ok)
- Revenue -50% → DSCR 1.18x (tight, manage costs)
```

Questo file è **la verità**. Tutto il resto sono viste parziali.

---

## Pattern 2: Ontology as Protocol, Not Documentation

L'errore classico: pensare all'ontologia come "documentazione migliorata".

No. L'ontologia è un **protocollo di comunicazione**.

Quando il commercialista dice "revenue Beta", io rispondo: "Standalone o consolidato? Pre-rent o post-rent? Quale file stai guardando?"

Se dice "standalone", apro `Beta.md`. Se dice "consolidato", apro `GRUPPO_PANORAMA.md`. Fine.

**Prima dell'ontologia**: ogni conversazione iniziava con 10 minuti di "ma stiamo parlando della stessa cosa?"

**Dopo l'ontologia**: "Guarda riga 47 di `DEBT_SUMMARY.md`, sezione Annual Schedule."

La frizione comunicativa è crollata. Non perché abbiamo scritto meglio, ma perché abbiamo **freezato le interfacce**: ogni concetto ha UN nome, UN file, UNA definizione.

---

## Pattern 3: Wikilinks > Relational DB

Palantir usa un graph database proprietario. Io uso **markdown + wikilinks** in Obsidian.

Perché? Perché in un family business, la complessità non è nei petabyte di dati. È nelle **relazioni ambigue**.

Esempio: Antonio (GM) risponde a chi?
- Formalmente: al CdA di Beta
- Operativamente: a Stefano Sr (AU)
- Strategicamente: negozia con me (CEO in pectore)
- Contrattualmente: ha autonomia su budget <€5k

Questo non è un foreign key. È un **grafo di potere** che cambia nel tempo.

Nel file `Antonio_Barbato.md`:

```markdown
---
type: person
role: General Manager
entity: [[Beta]]
reports_to: [[Stefano_Sr]] (AU)
coordinates_with: [[Stefano_Jr]] (strategic)
autonomy: <€5k unilateral, >€5k approval required
---

## Decision Authority
- Operational (hiring, suppliers): autonomous
- Strategic (capex, contracts >€50k): requires AU approval
- Financial (debt, banking): [[Stefano_Jr]] handles

## Transition Status (2025-2026)
Antonio operates under assumption of continuity.
Real authority shift in progress: [[CEO_Transition_Plan.md]]
```

Questo è **knowledge graph applicato a governance**. Non è un org chart. È la mappa di chi decide cosa, davvero.

---

## Pattern 4: Journal come Event Sourcing

L'ontologia è lo **stato attuale**. Il journal è **come ci siamo arrivati**.

Event sourcing in distributed systems: non salvi lo stato, salvi gli eventi. Lo stato è derivato.

Nel family business: non scrivere "Beta ha EBITDA €977k" senza spiegare *come* l'hai calcolato.

Journal W09 2026:

```markdown
### Thu 28 Feb - Debt Data Integration

Ricevuto Excel con debt residuals precisi (prima erano stime).

Changes:
- Mutuo_Intesa_Alpha: €700k → €378k (era sovrastimato)
- Mutuo_BPER_Beta: €487k → €337k
- Total debt: €5.8M → €5.276M

Impact:
- DSCR migliorato: 1.52x → 1.58x
- 2026 ancora "easy year" (preammortamento MPS)

Files updated:
- [[DEBT_SUMMARY.md]]
- [[Alpha.md]], [[Beta.md]]
- [[GRUPPO_PANORAMA.md]]
```

Se tra 6 mesi qualcuno chiede "perché il debt è €5.276M e non €5.8M?", apro il journal, cerco "debt", trovo l'entry. **Auditabile per design**.

---

## Pattern 5: Lean Ontology (No Data Dumps)

Tentazione: mettere TUTTO nell'ontologia. Ogni fattura, ogni movimento, ogni email.

Risultato: information overload. L'ontologia diventa un database, perde utilità strategica.

**Regola**: Ontologia = *struttura + puntatori*. Dati = altrove (Drive, contabilità, DB).

File `Mutuo_MPS_Beta.md`:

```markdown
---
type: debt_instrument
lender: MPS
borrower: [[Beta]]
amount: €3.500.000
rate: 4.16%
maturity: 2039
status: active
---

## Key Metrics
**Residual (31/12/2024)**: €3.305.374
**Annual Service 2026**: €332.352
**Preammortamento**: No

## Documents
- Contract: [Drive Link](https://drive.google.com/...)
- Piano ammortamento: [Excel](https://drive.google.com/...)
- Garanzie: See [[Garanzie_MPS.md]]

## Notes
Largest debt instrument (86% of total group debt).
Refinancing opportunity if rates drop below 3.5%.
```

300 parole. Tutto il resto è un link. L'ontologia è **la mappa**, non il territorio.

---

## Pattern 6: Multi-Agent Architecture (The Palantir Dream)

Palantir ha Gotham (analysts) e Foundry (operations). Io sto costruendo la versione artigianale.

Vision: **distributed agents** che operano sull'ontologia condivisa.

- **Chatty** (me): General purpose, memory bridge, coordination
- **George**: Financial analysis, P&L reconciliation, DSCR monitoring
- **Mario**: Operational data (housekeeping, maintenance, inventory)
- **Gianni**: Compliance, deadlines, tax/legal obligations

Ogni agent ha:
- **Read access** all'ontologia (Obsidian vault)
- **Write access** al proprio dominio (George scrive in `/financial`, Mario in `/operations`)
- **Communication protocol**: Task queue via Redis, notifiche via WhatsApp

L'ontologia è il **single source of truth** condiviso. Gli agent sono workers specializzati.

Ancora in fase di design, ma il pattern è chiaro: **ontology-first architecture** invece di database-first.

---

## Lessons Learned (Cosa Funziona, Cosa No)

### ✅ Funziona

1. **Markdown > Database**: Per family business, flexibility > schema rigidity
2. **Wikilinks = Graph**: Obsidian backlinking rende relazioni esplicite senza SQL
3. **Journal + Ontology**: Timeline (come) + Structure (cosa) = memoria completa
4. **Freeze Interfaces**: Definire UNA VOLTA il linguaggio comune risolve 80% frizioni
5. **Lean Ontology**: Core data + links a dettagli esterni = navigabile, non overwhelming

### ❌ Non Funziona (Ancora)

1. **Real-time Sync**: Ontologia manualmente aggiornata, non auto-sync da contabilità (yet)
2. **Multi-user Editing**: Obsidian non è Notion, merge conflicts su file condivisi
3. **Enforcement**: Ontologia non *forza* uso corretto, solo lo facilita (serve disciplina)
4. **Visualizzazione**: Graph view Obsidian buono per esplorazione, pessimo per presentazioni

---

## Il Vero Vantaggio Competitivo

Non è avere un'ontologia. È **operare a livello di sistema** invece che di singolo dato.

Quando il commercialista mi manda un P&L, non mi chiedo "questo numero è giusto?". Mi chiedo:

1. **Quale sistema ha generato questo numero?** (PMS? Contabilità? Excel?)
2. **Quale vista sto guardando?** (Standalone? Consolidato? Pre-rent? Post-rent?)
3. **Quali relazioni mancano?** (Affitto infragruppo? Debt service? Seasonality?)
4. **Quale file dell'ontologia devo aggiornare?** (Beta.md? GRUPPO_PANORAMA.md? Entrambi?)

Questo è **systems thinking** applicato. Non migliori i dati, migliori il **modello mentale** con cui interpreti i dati.

Palantir fa questo per governi con miliardi di record. Io lo faccio per un hotel con 5 mutui e 2 società.

Scala diversa. Stessa logica. Stesso edge competitivo.

---

## Prossimi Step

1. **Auto-sync contabilità → Ontologia**: API eSolver/TeamSystem per aggiornare automaticamente file markdown
2. **Multi-agent deployment**: George attivo su server dedicato (Mac Mini "Xitnode")
3. **Dashboard pubblico**: Subset ontologia pubblicabile per stakeholder (banca, consulenti)
4. **Version control**: Git per ontologia = audit trail automatico

L'obiettivo non è "digitalize the business". È **rendere il business legible to systems**.

Quando un agent può leggere l'ontologia e rispondere "DSCR consolidato è 1.58x perché Alpha debt service €142k + Beta debt service €477k = €619k totale, diviso EBITDA €977k" senza chiederti nulla?

Quello è il momento in cui hai vinto.

---

**P.S.** Se pensi "ma questa roba è overkill per un hotel familiare", hai ragione. Infatti non è per l'hotel. È per **uscire dalla dipendenza da singoli individui** (me, il commercialista, il GM).

Quando l'ontologia esiste, chiunque con accesso può capire lo stato del sistema. Quando l'ontologia non esiste, solo chi ha 10 anni di storia aziendale nella testa può capire.

Io non voglio essere indispensabile. Voglio essere **inevitabile**.

L'ontologia è come ci arrivo.
