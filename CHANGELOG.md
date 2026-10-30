# Changelog

## 2.0.0 - 21 ottobre 2026

- Implementata la ricerca esaustiva locale con candidati lazy, confronto con il bersaglio e arresto al successo.
- Sostituito il campione casuale con `itertools.product`; ogni combinazione viene generata una volta nell'ordine dell'alfabeto.
- Misurata la durata completa con `perf_counter_ns`, includendo generazione dei candidati e confronti.
- Separati tempo osservato, velocità media ed estrapolazione lineare normalizzata.
- Introdotti input validati, alfabeto configurabile, lunghezza 1..12 e limite predefinito di un milione di tentativi.
- Usato `secrets.choice` per il bersaglio di prova; eliminato il seed globale.
- Aggiunte CLI ripetibile, gestione di input errati/EOF/Ctrl+C e risultato strutturato immutabile.
- Sostituiti i test di caratterizzazione con 34 test dei requisiti correnti, senza dipendenze esterne.
- Aggiornati README, analisi, tutorial, verifica e istruzioni Git; archiviata l'analisi della v1.
- Conservati immutati i sorgenti ricevuti in `originali/`.

**API:** le funzioni storiche sono sostituite dalle nuove API; non ci sono alias impliciti. Vedi `docs/ANALISI.md`.

---


## Recupero del progetto - 20 ottobre 2026

- Aggiunti commenti italiani ai due sorgenti e documentazione del comportamento effettivo.
- In `algoritmo.py`, sostituito esclusivamente `random.seed(dt.now())` con `random.seed()` per consentire l'import su Python 3.11 e successivi. La versione precedente solleva `TypeError` nell'ambiente verificato (Python 3.12.14).
- Conservati nomi, alfabeto, formule, dimensione del campione, messaggi, import inutilizzati e difetti logici. I commenti non devono essere interpretati come una correzione del benchmark.
- `test.py` conserva lo stesso codice eseguibile dell'originale, compresi import `pytest`, stampe e asserzione probabilistica.
- Aggiunti 18 test ripetibili basati sulla libreria standard, distinti dai test storici.
- Conservate copie esatte degli allegati in `originali/`.
- Aggiunti file di supporto per pubblicazione e dipendenza facoltativa dei test storici.

L'header di autore e versione ricevuto non è stato sostituito. Il PDF personale è distribuito separatamente, fuori dal materiale pubblico.
