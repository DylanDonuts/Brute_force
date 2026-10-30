# Pubblicare la versione 2 su GitHub

Una modifica verificata viene registrata con un commit locale. Il push invia i commit a un repository remoto. Il progetto preparato contiene una storia locale con due commit: il prototipo annotato e la correzione funzionante. La pubblicazione remota richiede un collegamento autenticato e una destinazione GitHub.

Il PDF personale resta fuori da questa cartella. Non copiare dati personali o credenziali nel repository. `.gitignore` non rimuove dalla cronologia file già tracciati.

## Controllare prima di pubblicare

```bash
python3 -m unittest discover -s tests -v
git status
git log --oneline
git show --stat HEAD
```

Su Windows usa `py` al posto di `python3`. Il risultato atteso è 34 test superati e una cartella Git senza modifiche non registrate.

## Se hai ricevuto l'archivio con il bundle Git

L'archivio contiene una cartella `bruteforse/` con i file consultabili e un file `Bruteforse_v2.bundle` che conserva i commit. Per ottenere una vera cartella Git, dalla cartella in cui hai estratto lo ZIP:

```bash
git clone Bruteforse_v2.bundle bruteforse-git
cd bruteforse-git
git log --oneline
```

Il bundle diventa inizialmente il remoto `origin`; rinominalo per collegare il nuovo repository GitHub:

```bash
git remote rename origin bundle-locale
```

Il nome `bruteforse-git` evita di sovrascrivere la cartella di sola consultazione già estratta. Non inizializzare di nuovo il repository dopo il clone: i commit sono già presenti.

## Nuovo repository remoto

Crea su GitHub un repository vuoto, per esempio `bruteforse`. Scegli la visibilità desiderata. Non inizializzare un secondo README: quello del progetto è già incluso nei commit.

Nella cartella Git ottenuta dal bundle, sostituisci il segnaposto con l'URL HTTPS reale:

```bash
git remote add origin URL_HTTPS_DEL_REPOSITORY_VUOTO
git push -u origin main
```

Il push include i due commit. L'attribuzione dei sorgenti resta nei file; i commit preparati dall'assistente usano l'identità Git dell'ambiente di lavoro e non inventano un'identità personale dell'utente.

## Repository GitHub già esistente

Non inviare alla cieca la storia nuova sopra una storia remota diversa. Prima clona il repository esistente e leggi le istruzioni `AGENTS.md`, se presenti. Crea un ramo per la modifica, confronta i contenuti, copia le modifiche pertinenti e conserva la storia e i file non correlati.

Dopo aver ripetuto i test nel repository esistente:

```bash
git status
git diff
git add algoritmo.py test.py tests README.md CHANGELOG.md docs originali requirements-dev.txt .gitignore
git diff --cached --stat
git commit -m "Implementa ricerca brute force locale e misura corretta dei tempi"
git push -u origin NOME_DEL_RAMO_SCELTO
```

Sostituisci il segnaposto con il ramo effettivo. Non usare force push per unire storie non correlate. Se il repository esistente ha già file con gli stessi nomi, le modifiche vanno integrate e verificate sul suo contenuto corrente.

## Descrizione del commit

> Il prototipo confrontava stringhe casuali con spazi e scartava l'esito. La nuova versione enumera candidati senza duplicati, confronta con il bersaglio locale e si ferma al successo o al limite di tentativi. Misura l'intervallo completo con perf_counter_ns e distingue il tempo osservato da un'estrapolazione lineare.
>
> Aggiunge input validati, CLI ripetibile, risultato strutturato e documentazione aggiornata. Verifica: 34 test unittest superati su Python 3.12.14; demo deterministica `sa` su `as` trovata in tre tentativi. I sorgenti originali rimangono conservati.

Queste sono istruzioni di pubblicazione e una descrizione pronta: non attestano che il push sia già avvenuto.
