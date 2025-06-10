---
layout: post
title: "Da script a sistema (v1)"
date: 2025-06-10
categories: [tech, workflow]
tags: [automation, systems, learning]
---

# Da script a sistema (v1)

Sto cercando di fare un salto.

Scrivo script da anni. Piccoli, risolutivi, spesso brutti ma funzionanti.  
Ora sento che non basta più.  

## Il problema

Ogni volta che mi serve qualcosa:
- Apro un vecchio `.py`  
- Cambio due righe  
- Lo lancio a mano

Poi lo chiudo. E me ne dimentico. Fino alla prossima volta.

Risultato?  
Una cartella disordinata e nessuna evoluzione.

## Il pattern che inizia a emergere

- Alcuni script li uso sempre (es. parsing file, aggiornamento fogli)
- Alcuni diventano **moduli** quasi senza accorgermene
- Alcuni iniziano a parlare tra loro, e lì capisco: **sta nascendo un sistema**

Ma è tutto ancora fragile:
- Dipendenze sparse  
- Parametri hardcoded  
- Zero test  
- Nome file tipo `final_final_2_versioneOK.py`

## Il desiderio

Vorrei arrivare a un **v1** che:
- Posso spiegare a voce in due minuti  
- Ha un entrypoint chiaro (`main.py`, non `random_script.ipynb`)  
- Funziona anche domani, non solo oggi  
- Se crasha, so dove guardare

Non sogno la perfezione. Sogno la **tenuta nel tempo**.

## Cosa sto facendo, piano piano

- Sposto codice in moduli (`utils`, `io`, `parser`, `logic`)
- Aggiungo logging dove prima c'erano solo `print()`
- Uso `.env` invece di scrivere token nei file
- Scrivo README anche solo per me stesso

Non è "software engineering".  
È solo provare a costruire qualcosa che duri un po' più di un pomeriggio.

---

*A volte uno script ti salva la giornata.  
Un sistema ti salva l'intero mese.*

[← Post precedente](/2025/06/03/progetto-invitalia.html) • [Tutti i post](/archive)