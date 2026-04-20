---
layout: post
title: "Canonical Language vs Grand Ontology"
date: 2026-04-20
categories: [xitnode]
tags: [ontologia, sistemi, identità, dati]
---

"Serve una grande ontologia ben modellata per usare gli agenti."

No.
Non la finisci mai.
E se anche la finissi, decade prima di essere usata.

## Dove non torna

Una grande ontologia presuppone che:
- Puoi modellare tutto il dominio prima di usarlo
- Il modello resta stabile nel tempo
- La completezza è un requisito

Nessuna di queste è vera.

Il dominio cambia mentre lo modelli.
Le relazioni emergono dall'uso, non dalla progettazione.
E quando finalmente "finisci", il codice che doveva usarla è già andato avanti.

Risultato: l'ontologia resta un documento bellissimo che nessuno interroga.

## La rottura

Non serve "ontologia".
Serve una lingua che sopravvive all'uso.

La differenza è questa:

**Ontologia** = modello completo del mondo.
**Canonical language** = vocabolario minimo che regge operazioni reali.

Il primo è un progetto che non finisce.
Il secondo è un contratto che funziona.

<p style="text-align: center;"><img src="/assets/images/ontology-vs-canonical-language.svg" alt="Ontologia vs Canonical language" style="max-width: 800px; width: 100%; height: auto;"></p>

## Identity è il muro portante

Prima di relazioni, grafi, agenti, embeddings — c'è identity.

Se l'identità è debole, tutto collassa.

Esempio concreto:
- La finanza scrive "Consulenze IT"
- Il controllo di gestione scrive "Servizi tecnici"
- La contabilità registra "Costi per servizi"

Stessa spesa. Tre nomi. Nessun ID canonico.

Quando provi a fare join, reconciliation, query cross-system — fallisci.
Perché non sai se stai parlando della stessa cosa.

**Identity prima di tutto.**

Non stringhe raw.
Non "il sistema capirà".

ID canonici:
```
company:orti
bank_account:bper_intur_001
counterparty:booking_com
```

Con regole di disambiguazione esplicite:
- Un alias table che mappia varianti → entità canonica
- Nessuna stringa libera dove serve un'entità
- Ogni riferimento si risolve a un ID o fallisce

Se l'ID è weak, il resto è teatro.

## Modella l'incertezza, non fingere certezza

I sistemi reali non sono fatti solo di fatti certi.
Contengono:
- Match sospetti
- Candidati non risolti
- Entità ambigue
- Punteggi di confidenza

Un'API seria non finge certezza dove il mondo è ambiguo.

Esempio:

**API giocattolo:**
```python
resolve_entity("Booking.com payment") -> Entity
```
Sempre ritorna qualcosa. Anche quando non sa.

**API seria:**
```python
resolve_entity("Booking.com payment") -> Entity | List[Entity] | None
```
- Un'entità se match perfetto
- Lista di candidati se ambiguo
- `None` + confidence score se troppo incerto

Questa è la differenza tra sistema che mente e sistema che puoi usare.

<p style="text-align: center;"><img src="/assets/images/toy-api-vs-serious-api.svg" alt="API giocattolo vs API seria" style="max-width: 800px; width: 100%; height: auto;"></p>

## Parti da Pydantic, non da grafi

Non RDF.
Non OWL.
Non Neo4j il primo giorno.

Pydantic.

Typed Python models che sopravvivono a:
- Ingestion
- Reconciliation
- Query
- Agent use

```python
class Entity:
    id: str
    canonical_name: str
    aliases: List[str]
    type: EntityType  # company, person, bank

class Transaction:
    id: str
    amount: Decimal
    date: date
    resolved_entity: Optional[Entity]
    confidence: float
```

Questo è canonical language.

Non è completo. Non modella tutto.
Ma funziona oggi. E domani puoi aggiungerci sopra.

## Le azioni determinano l'ontologia

Non parti dalla mappa completa.
Parti da un'azione reale.

Esempio: "Voglio vedere movimenti mensili per banca."

Quali primitivi servono?
- `Transaction`
- `Entity` (banca)
- `Dimension` (mese)

Basta.

Non serve modellare camere, prenotazioni, fornitori, staff.
Serve modellare abbastanza per fare quella query.

L'ontologia finisce quando l'azione funziona.

Poi, quando rompi qualcosa o hai bisogno di altro, aggiungi.
Non prima.

## Ten primitives, not fifty

In the era where everyone shits code, less is premium.

Chiunque con AI può generare 10,000 righe in un'ora.

Ma:
- 10,000 righe di slop collassano
- 100 righe di primitivi puliti sopravvivono

Start with three:
- `Entity`
- `Transaction`
- `Document`

Add primitive #4 only when you hit a wall you cannot solve with three.

Build less than you think.

## Il punto finale

Non stai costruendo una rappresentazione perfetta del mondo.

Stai costruendo un vocabolario minimo che regge le operazioni che devi fare oggi.

Identity forte.
Incertezza esplicita.
Deriva dalle azioni.

Non filosofia. Canonical language.

Quella sopravvive all'uso.
