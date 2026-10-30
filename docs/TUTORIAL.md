# Capire insieme le correzioni

## 1. Partiamo da quattro sole combinazioni

Usa questo comando, sostituendo `python3` con `py` su Windows:

```bash
python3 algoritmo.py --password sa --alphabet as
```

Con due simboli e due posizioni le possibilità sono quattro. Prima di guardare il risultato, scrivile: `aa`, `as`, `sa`, `ss`. Il risultato atteso è tre tentativi. Se il bersaglio fosse `aa` servirebbe un tentativo; con `ss` ne servirebbero quattro.

La password è intenzionalmente nota nella demo: ci serve per verificare che la ricerca la trovi nella posizione giusta. Il ciclo non calcola la posizione dal testo del bersaglio: prova i candidati in ordine.

## 2. Correggiamo il significato del confronto

La vecchia riga confrontava il candidato con una stringa di spazi e scartava il booleano. La nuova logica è:

```python
for candidate in islice(iter_candidates(len(target), alphabet), max_attempts):
    attempts += 1
    if candidate == target:
        return SearchResult(candidate, attempts, total, perf_counter_ns() - start_ns)
```

`candidate` è il tentativo corrente. `target` è il bersaglio. `==` verifica l'uguaglianza; `if` usa quel risultato; `return` termina la funzione. Non viene generato il candidato successivo dopo un successo.

**Esercizio:** spiega perché cambiare il vecchio `==` in `=` non sarebbe stato sufficiente. Con `=` avresti assegnato un valore, senza decidere se hai trovato il bersaglio.

## 3. Sostituiamo il campione con un iteratore

Il campione casuale poteva contenere duplicati e omettere combinazioni. Il prodotto cartesiano genera ogni combinazione ammessa una volta, nell'ordine dell'alfabeto. L'espressione generatrice restituisce una stringa alla volta: non serve una lista da quasi un milione di elementi.

```bash
python3 -c "from algoritmo import iter_candidates; print(list(iter_candidates(2, 'as')))"
```

Qui `list` viene usata solo per vedere le quattro possibilità della demo; il motore di ricerca non materializza lo spazio completo.

**Esercizio:** cambia l'alfabeto in `sa`. Come cambia la posizione del bersaglio `sa`? Ora è il secondo candidato, perché l'ordine è `ss`, `sa`, `as`, `aa`.

## 4. Misuriamo una durata, con unità esplicite

Il programma legge un contatore prima e dopo la ricerca:

```python
elapsed_ns = end_ns - start_ns
seconds = elapsed_ns / 1_000_000_000
milliseconds = elapsed_ns / 1_000_000
```

Non viene estratta la sola parte frazionaria di una data. Una durata di 1,25 secondi rimane 1,25 secondi, pari a 1.250 millisecondi.

Il tempo include la creazione dei candidati e il confronto. Non include ciò che fai al terminale né la stampa. Una prova breve può mostrare risultati diversi a ogni esecuzione: ciò non cambia il numero atteso di tentativi per un bersaglio e un ordine fissati.

## 5. Distinguiamo misura ed estrapolazione

La durata effettiva riguarda i tentativi eseguiti. Se misuro `D` secondi per `S` tentativi, il costo medio è `D/S`. Una estrapolazione su `N` combinazioni è `(D/S) * N`. Non è un secondo esperimento e non assicura che la velocità resti uguale su tutto lo spazio.

**Esercizio:** tre tentativi in 1,25 secondi su uno spazio di quattro combinazioni danno circa 1,667 secondi come estrapolazione completa. Il tempo realmente misurato resta 1,25 secondi.

## 6. Un limite non equivale a un fallimento definitivo

```bash
python3 algoritmo.py --password ss --alphabet as --max-attempts 2
```

Il bersaglio è valido, ma il programma può visitare solo `aa` e `as`. Dichiara la ricerca incompleta. Per questa prova, portare il limite a quattro permette di trovare `ss`. La nuova esecuzione parte nuovamente da `aa`.

## 7. Verifichiamo i requisiti

```bash
python3 -m unittest discover -s tests -v
```

I 34 test correnti non conservano gli errori della vecchia versione come risultati desiderati. Verificano il comportamento corretto, per esempio il recupero del bersaglio, il conteggio esatto e la conservazione dei secondi interi. Gli orologi sostitutivi rendono verificabile la formula senza affidarsi alla velocità del computer.

Un test visita anche tutti i 30 bersagli dell'alfabeto `as` per lunghezze da uno a quattro e controlla il numero di tentativi tramite la loro posizione binaria. È una verifica di spazi piccoli, non una misura di prestazioni su password reali.

## 8. Leggiamo il commit

Il repository locale contiene prima il prototipo annotato e poi la correzione. Dopo aver ottenuto la copia Git:

```bash
git log --oneline
git show --stat HEAD
git diff HEAD~1 HEAD -- algoritmo.py
```

Una modifica funzionante diventa un commit solo dopo aver verificato codice e documentazione. Il push invia quel commit al repository remoto: commit e push sono due operazioni diverse.
