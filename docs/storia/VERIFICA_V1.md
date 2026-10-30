# Documento storico: versione 1, non descrive la v2

# Verifica della revisione

Ambiente effettivamente usato: **Python 3.12.14, Linux**. I comandi Windows sono forniti come istruzioni equivalenti; non è stato eseguito un collaudo su Windows.

## Controlli effettuati

| Controllo | Esito |
| --- | --- |
| Esecuzione del sorgente ricevuto | `TypeError` su `random.seed(dt.now())`, prima dell'input |
| Confronto strutturale AST di `algoritmo.py` | Solo il seed differisce nel codice eseguibile; commenti e spaziatura non cambiano la logica |
| Confronto strutturale AST di `test.py` | Codice eseguibile invariato |
| Confronto byte per byte delle copie `originali/` | Entrambe uguali agli allegati ricevuti |
| Nuova suite `unittest` | **18 test superati** |
| CLI annotata con input `3` | Genera tre caratteri e completa il benchmark storico |
| CLI annotata con input `0` | Mostra input non valido e mancata generazione; termina senza eccezione |
| CLI annotata con input `-2` | Stringa vuota e mancata generazione; evidenzia la validazione incompleta |
| CLI annotata con input `ciao` | `ValueError` non intercettato; limite noto conservato |

I tempi numerici osservati non vengono usati come risultato prestazionale: l'algoritmo di misura ha i difetti descritti in [ANALISI.md](ANALISI_V1.md).

## Suite ripetibile aggiunta

```bash
python3 -m unittest discover -s tests -v
```

Su Windows usa `py` al posto di `python3`. La suite controlla lunghezza e alfabeto, indici estratti controllati, collisioni ammesse, input zero/negativo/non intero, dimensione effettiva del campione, stringa vuota e duplicati. Per il benchmark usa un campione sostitutivo e un orologio controllato.

Due misure artificiali di 0,25 e 1,25 secondi producono lo stesso risultato storico: il test dimostra che `.microseconds` perde i secondi interi. Un altro controllo mostra che, con campione e orologio fissati, password diverse di uguale lunghezza producono lo stesso valore.

Questi sono **test di caratterizzazione**: descrivono ciò che il codice fa, compresi errori noti. Non sono test di accettazione di una ricerca corretta. Se il benchmark viene corretto, i test che fissano il difetto andranno sostituiti con requisiti nuovi.

## Test storici

Il file `test.py` è annotato ma non corretto. Non è stato eseguito con pytest in questo ambiente, dove la dipendenza non era installata. La nuova suite non richiede pytest. Per ripetere i test storici installa facoltativamente `requirements-dev.txt` e usa `python3 -m pytest test.py`.

Il nome esplicito evita l'esclusione di `test.py` dalla normale scoperta di pytest. Un eventuale fallimento della disuguaglianza fra password casuali richiede una verifica del requisito: due stringhe uguali non dimostrano di per sé un difetto del generatore.

## Integrità degli allegati conservati

SHA-256 delle copie presenti in `originali/`:

```text
algoritmo.py
2d30054a5c40b5cf9342268b7e68d6e040c8ef6052e812aa6f784d9ea4e0b4bc

test.py
2975d793d5280230ae3ab6cc5d94f2ffa02b675c9e9ee64b028d9e106df2d24e
```

Non sono stati effettuati test di carico, misure su GPU, ricerca su account o confronti con sistemi di autenticazione. Il programma non implementa queste funzioni.
