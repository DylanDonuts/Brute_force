# Bruteforce 2.0

Dimostrazione Python di ricerca **brute force locale**, con generazione dei candidati, confronto con un bersaglio di prova, conteggio dei tentativi e misura del tempo effettivo.

Il bersaglio è già noto al programma: lo genera oppure lo riceve dalla riga di comando. Lo scopo è osservare come funziona una ricerca esaustiva, non recuperare credenziali da un sistema reale. Non sono presenti chiamate di rete, account, dati cifrati o verifiche di hash.

## La correzione, in breve

| Versione storica | Versione 2.0 |
| --- | --- |
| Campione casuale di 999.999 stringhe, anche duplicate | Combinazioni generate una alla volta e senza duplicati |
| Confronto con una stringa di spazi; esito scartato | Confronto con il bersaglio e arresto al successo |
| Proprietà `.microseconds`, che perde i secondi interi | Durata completa con `time.perf_counter_ns()` |
| Numero estrapolato etichettato come tempo osservato | Tempo effettivo distinto dall'estrapolazione indicativa |
| Input non validati e test casuali fragili | Validazione, limite dei tentativi e 34 test automatici |

## Prova subito

Serve Python **3.11 o successivo**. Il progetto è verificato localmente con **Python 3.12.14** su Linux e non ha dipendenze esterne.

Apri il terminale nella cartella contenente `algoritmo.py`. Su Windows:

```powershell
py algoritmo.py --password sa --alphabet as
```

Su Linux/macOS:

```bash
python3 algoritmo.py --password sa --alphabet as
```

La sequenza è `aa`, `as`, `sa`, `ss`. Il programma trova `sa` al terzo tentativo e si ferma prima di generare `ss`.

Parte deterministica dell'output:

```text
BRUTEFORSE 2.0 | dimostrazione locale
Bersaglio di prova: sa
Combinazioni a lunghezza fissa: 4
Tentativi eseguiti: 3
Password trovata: sa
```

Seguono durata, velocità media ed estrapolazione. Questi numeri variano fra esecuzioni: con pochi tentativi il costo fisso influenza molto la misura.

## Generare una password di prova

```bash
python3 algoritmo.py --length 4
```

L'alfabeto predefinito è `asdfghjk`. La password viene generata con `secrets.choice`, senza modificare uno stato globale tramite `random.seed`.

Senza opzioni, `python3 algoritmo.py` chiede la lunghezza; Invio sceglie `4`. Su Windows sostituisci `python3` con `py` nei comandi.

## Fermarsi a un numero di tentativi

```bash
python3 algoritmo.py --password ss --alphabet as --max-attempts 2
```

L'output indica **ricerca incompleta**, con 2 tentativi su 4. Non viene dichiarato un successo né l'assenza del bersaglio. Per completare la ricerca puoi ripetere il comando con `--max-attempts 4`; la nuova esecuzione riparte dall'inizio, non riprende da un checkpoint.

Per impostazione predefinita il limite è 1.000.000 di tentativi. Le lunghezze ammesse sono 1..12. Lo spazio può superare il limite: con 8 simboli e lunghezza 8 ci sono 16.777.216 combinazioni.

## Test

```bash
python3 -m unittest discover -s tests -v
```

Rimane valido anche `python3 test.py`. Entrambi i comandi eseguono i **34 test della versione 2**, senza pytest. La suite verifica:

- ordine dei candidati e copertura di piccoli spazi;
- bersaglio iniziale, intermedio, finale e arresto immediato;
- limite esatto dei tentativi e successo sull'ultimo tentativo consentito;
- durata completa, millisecondi, velocità ed estrapolazione;
- input non validi, argomenti CLI, EOF e interruzione.

I test temporali controllano un orologio sostitutivo; quelli CLI avviano davvero il programma. Non si richiede che due estrazioni casuali siano diverse.

## Struttura

| Percorso | Contenuto |
| --- | --- |
| `algoritmo.py` | Logica commentata, risultato strutturato e interfaccia da terminale |
| `tests/test_algoritmo.py` | Test dei requisiti correnti |
| `test.py` | Avvio della suite con il comando storico |
| `originali/` | Copie immutate dei sorgenti ricevuti |
| `docs/ANALISI.md` | Algoritmo, API, tempi, complessità e differenze dalla v1 |
| `docs/TUTORIAL.md` | Percorso guidato per comprendere le correzioni |
| `docs/VERIFICA.md` | Casi verificati e limiti delle verifiche |
| `docs/PUBBLICAZIONE.md` | Pubblicazione da un repository nuovo o esistente |
| `docs/storia/` | Analisi e verifica riferite esclusivamente alla v1 |
| `CHANGELOG.md` | Modifiche delle revisioni |

Il PDF personale della prima analisi descrive la **v1**, non il comportamento corretto della v2. Non fa parte del repository.

## API di base

```python
from algoritmo import brute_force_search, generate_password, iter_candidates

print(generate_password(3, "as"))
print(list(iter_candidates(2, "as")))
result = brute_force_search("sa", "as", max_attempts=4)
print(result.password, result.attempts, result.elapsed_milliseconds)
```

`result.status` distingue `found`, `limit_reached` ed `exhausted`. Con un bersaglio valido nell'alfabeto e il generatore previsto, una ricerca completa lo trova; `exhausted` è lo stato generale di uno spazio interamente visitato senza successo.

La v2 cambia volutamente l'API: le vecchie funzioni `decriptapassword`, `creaCampione`, `generapassword` e `creapassword` non sono mantenute come alias. La storia Git e `originali/` conservano il progetto precedente.

## Che cosa misura il tempo

L'intervallo include creazione dell'iteratore, generazione dei candidati, conteggio e confronti fino all'arresto. Esclude input, generazione iniziale del bersaglio, validazione e stampa. Il tempo effettivo è una durata osservata; l'estrapolazione su tutto lo spazio usa `(durata / tentativi) * combinazioni` ed è soltanto un modello lineare del medesimo lavoro locale.

La lunghezza e l'alfabeto sono noti. Il programma confronta stringhe in memoria: non misura la sicurezza di account, sistemi di autenticazione o funzioni di derivazione di password. Il tempo di ricerca resta esponenziale nella lunghezza nel caso peggiore; generare dati in modo lazy riduce la memoria, non il numero delle combinazioni.

## Provenienza

L'header originale indica **Ciro Cozzolino**, versione **1.0**, ed è preservato nei sorgenti ricevuti e richiamato nel file corrente. La versione 2 documenta la correzione del prototipo. Non è stata assegnata una nuova licenza al codice senza una scelta del titolare dei diritti.

## Riferimenti ufficiali

- [itertools.product](https://docs.python.org/3.12/library/itertools.html#itertools.product)
- [time.perf_counter_ns](https://docs.python.org/3.12/library/time.html#time.perf_counter_ns)
- [secrets.choice](https://docs.python.org/3.12/library/secrets.html#secrets.choice)
