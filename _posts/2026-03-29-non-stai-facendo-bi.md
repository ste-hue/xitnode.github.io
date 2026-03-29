---
layout: post
title: "Non Stai Facendo BI"
date: 2026-03-29
categories: [xitnode]
tags: [sistemi, dati, semantica, architettura]
---

"Abbiamo bisogno di dashboard."

No.
Avete bisogno di decidere cosa significano i numeri.

Oggi la stessa realtà entra nel sistema con nomi diversi.
La finanza la chiama "Consulenze IT".
Il controllo di gestione la chiama "Servizi tecnici".
La contabilità la registra come "Costi per servizi".

Stessa spesa.
Tre vocabolari.
Nessuna definizione vincolante.

La dashboard non risolve questo.
Lo comprime.

Mostra un numero che sembra condiviso.
Non lo è.
È il risultato di una scelta implicita fatta da qualcuno, da qualche parte, una volta.

Quella scelta non è visibile.
Non è riutilizzabile.
Non è difendibile.

Quando la domanda cambia, la definizione cambia.
Il lavoro riparte.
Tre tempi. Stesso evento.


![Prisma temporale del fatto finanziario](/assets/images/prisma_temporale_fatto_finanziario.svg)


## Aggregare non è riconciliare

La versione ufficiale dice: i dati sono dispersi, serve aggregarli.
Sembra logico.
È falso.

Aggregare è sommare.
Riconciliare è decidere quando due descrizioni diverse parlano della stessa cosa.

Le aziende fanno bene la prima.
Saltano la seconda.

Tesoreria lavora per cassa.
Contabilità per competenza.
Controllo di gestione per margini.

Tre funzioni.
Tre modelli.
Tre verità parziali.

Nessuno paga il costo della divergenza.
Quel costo emerge quando qualcuno chiede: "quanto stiamo davvero spendendo?"

A quel punto iniziano le traduzioni manuali.
Query, Excel, eccezioni.
Ogni volta diverse.
Ogni volta non riutilizzabili.

Questo non è un problema tecnico.
È un vuoto decisionale.

Nessuno ha deciso cosa significa una voce in modo vincolante per tutti.

## Il semantic layer

Quel punto ha un nome preciso: semantic layer.

Non è un glossario.
È un sistema di decisioni che lega il linguaggio del business ai fatti registrati.

Stabilisce che:
- una parola usata dalla finanza corrisponde a un insieme preciso di conti
- una categoria usata dal controllo di gestione è una proiezione coerente degli stessi fatti
- le due cose non sono alternative: sono viste dello stesso oggetto

Se questo layer non esiste, la logica vive negli output.
Ogni report contiene la sua versione della verità.
Le versioni divergono.

Se esiste, la logica vive nel modello.
Gli output diventano interrogazioni.

La differenza è operativa.

Nel primo caso, ogni nuova domanda genera lavoro.
Nel secondo, ogni nuova domanda riusa lavoro già fatto.

## Le tre dimensioni temporali

C'è un punto che rompe quasi tutti i sistemi.

Ogni evento finanziario esiste in più tempi:

**COMPETENZA** — quando genera risultato economico

**CASSA** — quando muove denaro

**IMPEGNO** — quando crea obbligazione

Tre tempi.
Stesso evento.

Se questi livelli non sono riconciliati in modo esplicito, ogni domanda che li attraversa diventa un progetto.

"Quanta cassa serve per coprire gli impegni del prossimo mese?"
Non è una domanda difficile.
Diventa difficile in un sistema senza semantica.

Qualcuno la risolve ogni volta a mano.
E ogni volta introduce variazioni.

## Le due scorciatoie

A questo punto arrivano due scorciatoie tipiche.

**Data lake:** tutto dentro, nessun significato deciso.
Risultato: accesso totale, interpretazione continua.

**ERP monolitico:** tutto definito, niente flessibilità.
Risultato: coerenza rigida, incapacità di adattarsi.

Entrambe evitano il problema centrale: decidere e mantenere un significato condiviso che può evolvere.

![Spettro datalake ERP semantic layer](/assets/images/spettro_datalake_erp_semantic_layer.svg)
## Dashboard e agenti non sono il sistema

Qui entra la distinzione che molti stanno ignorando.

Dashboard e agenti non sono il sistema.
Sono interfacce.

Se sotto non esiste una semantica canonica, entrambe leggono lo stesso disordine.
Una lo visualizza.
L'altra lo automatizza.

Un agente sopra dati non riconciliati non prende decisioni migliori.
Le prende più velocemente su basi ambigue.

Automatizza il conflitto.

Se invece il significato è stato deciso una volta, a monte, cambia tutto.

I fatti entrano.
Vengono validati.
Vengono mappati a un modello canonico.

A quel punto:
- le viste sono proiezioni
- i report non duplicano logica
- gli agenti operano su definizioni stabili

Questo non è business intelligence.
È un operating system finanziario.

Nel primo modello, ogni output è un oggetto costruito.
Nel secondo, ogni output è una query.

Nel primo, la complessità cresce con le domande.
Nel secondo, si comprime.

![Dashboard vs Financial OS architettura](/assets/images/dashboard_vs_financial_os_architettura.svg)

## Il test

Il test è semplice.

Quando arriva una nuova domanda, serve scrivere nuova logica?
O basta interrogare ciò che esiste già?

Se serve nuova logica ogni volta, il sistema non esiste.
Esiste solo lavoro ricorrente.

Se la risposta emerge dal modello, allora la base è corretta.

## Dove sta il valore

Il valore non sta nei dati.
Sta nelle decisioni che collegano i dati al loro significato.

I dati cambiano.
La semantica, una volta costruita, accumula valore.

Senza quel livello, continuerete a costruire dashboard.
E a rifare le stesse domande.

Con quel livello, iniziate a operare il sistema.
