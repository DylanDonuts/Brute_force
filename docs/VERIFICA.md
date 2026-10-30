# Verifica della versione 2.0

Ambiente locale: **Python 3.12.14, Linux**. La versione dichiara Python 3.11+; non sono state eseguite prove sulle altre versioni né su Windows/macOS. L'applicazione e i test usano esclusivamente la libreria standard.

## Comando e risultato

```bash
python3 -m unittest discover -s tests -v
```

**34 test superati.** È previsto anche l'avvio tramite `python3 test.py`. Non servono pytest, pip o un ambiente virtuale per questi comandi.

## Requisiti controllati

| Area | Evidenza |
| --- | --- |
| Copertura e ordine | Con alfabeto `as` e lunghezza 2 i candidati sono esattamente `aa`, `as`, `sa`, `ss` |
| Ordine configurabile | Con `sa` i candidati sono `ss`, `sa`, `as`, `aa` |
| Ricerca corretta | Bersagli iniziali, intermedi e finali hanno posizione e risultato attesi |
| Piccoli spazi completi | Verificati tutti i 30 bersagli sulle lunghezze 1..4 dell'alfabeto `as` |
| Arresto | Dopo il successo non si richiede un ulteriore candidato |
| Limite | Non viene generato un candidato oltre il limite; un successo esattamente al limite è valido |
| Memoria | L'API dei candidati restituisce un iteratore consumabile progressivamente, anche su spazi grandi |
| Generazione casuale | Lunghezza e alfabeto rispettati; una collisione è ammessa |
| Tempo | Orologio controllato: 1,25 secondi restano 1,25 secondi e 1.250 millisecondi |
| Intervallo | Il contatore viene letto prima della generazione dei candidati e dopo il confronto |
| Formula | Velocità ed estrapolazione normalizzate sui tentativi effettivi |
| Durata nulla | Velocità ed estrapolazione non vengono calcolate dividendo per zero |
| Input | Rifiutati lunghezze fuori limite, tipi errati, alfabeto vuoto/duplicato e bersagli fuori alfabeto |
| CLI | Provati successo, limite, input testuali errati, EOF, opzioni incompatibili, lunghezza esplicita e interruzione |

Il test sull'iteratore verifica il contratto lazy; non è un profiling della memoria. Le stime di complessità derivano dalla struttura dell'algoritmo, non da misure di RAM.

## Demo realmente eseguite

```bash
python3 algoritmo.py --password sa --alphabet as
```

Esito: `sa` trovata in **3 tentativi** su 4 combinazioni; uscita 0.

```bash
python3 algoritmo.py --password ss --alphabet as --max-attempts 2
```

Esito: **2 tentativi**, ricerca incompleta; uscita 1, che è attesa e non indica un crash.

I tempi mostrati durante queste esecuzioni variano e non sono pubblicati come benchmark. I test temporali sostituiscono il contatore per verificare le formule con dati noti.

## Integrità e revisione

I sorgenti in `originali/` sono confrontati byte per byte con gli allegati ricevuti. La documentazione corrente è distinta dai documenti storici, conservati in `docs/storia/`. I vecchi test che fissavano i difetti della v1 sono sostituiti da requisiti corretti; il primo commit della storia locale permette di recuperarli.

Non sono state effettuate prove contro reti, account o hash: non sono funzionalità implementate dal progetto. Non sono dichiarate velocità universali, copertura percentuale o prestazioni non misurate.
