# Progetto originale: Password generator, v1.0
# Author nell'header ricevuto: Ciro Cozzolino
"""Bruteforse 2.0: dimostrazione locale di ricerca esaustiva a lunghezza nota.

La password e' un bersaglio di prova gia' presente in memoria. I candidati
vengono generati una volta sola, confrontati e immediatamente scartati.
Il programma non usa account, reti, file cifrati o funzioni hash.
"""
from __future__ import annotations

import argparse
from collections.abc import Iterator
from dataclasses import dataclass
from itertools import islice, product
import secrets
import sys
from time import perf_counter_ns


DEFAULT_ALPHABET = "asdfghjk"
DEFAULT_MAX_ATTEMPTS = 1_000_000
MAX_LENGTH = 12
__version__ = "2.0.0"


def validate_alphabet(alphabet: str) -> str:
    """Rifiuta alfabeti vuoti o duplicati: ogni combinazione deve essere unica."""
    if not isinstance(alphabet, str):
        raise TypeError("L'alfabeto deve essere una stringa.")
    if not alphabet:
        raise ValueError("L'alfabeto non puo' essere vuoto.")
    if len(set(alphabet)) != len(alphabet):
        raise ValueError("L'alfabeto deve contenere caratteri tutti diversi.")
    return alphabet


def validate_length(length: int) -> int:
    # bool e' sottoclasse di int: lo escludiamo per non accettare True come 1.
    if isinstance(length, bool) or not isinstance(length, int):
        raise TypeError("La lunghezza deve essere un intero.")
    if not 1 <= length <= MAX_LENGTH:
        raise ValueError(f"La lunghezza deve essere compresa tra 1 e {MAX_LENGTH}.")
    return length


def generate_password(length: int, alphabet: str = DEFAULT_ALPHABET) -> str:
    """Genera un bersaglio di prova; due estrazioni possono coincidere."""
    validate_length(length)
    validate_alphabet(alphabet)
    # secrets usa la sorgente casuale del sistema: non serve un seed globale.
    return "".join(secrets.choice(alphabet) for _ in range(length))


def iter_candidates(length: int, alphabet: str = DEFAULT_ALPHABET) -> Iterator[str]:
    """Restituisce un iteratore, nell'ordine dei simboli forniti nell'alfabeto.

    Esempio: length=2, alphabet='as' -> aa, as, sa, ss.
    Non viene costruita una lista di tutte le stringhe.
    """
    validate_length(length)
    validate_alphabet(alphabet)
    return ("".join(characters) for characters in product(alphabet, repeat=length))


@dataclass(frozen=True)
class SearchResult:
    """Dati osservati della ricerca; secondi e millisecondi sono proprieta'."""
    password: str | None
    attempts: int
    total_combinations: int
    elapsed_ns: int

    @property
    def found(self) -> bool:
        return self.password is not None

    @property
    def status(self) -> str:
        if self.found:
            return "found"
        return "limit_reached" if self.attempts < self.total_combinations else "exhausted"

    @property
    def elapsed_seconds(self) -> float:
        return self.elapsed_ns / 1_000_000_000

    @property
    def elapsed_milliseconds(self) -> float:
        return self.elapsed_ns / 1_000_000

    @property
    def attempts_per_second(self) -> float | None:
        # Una misura nulla non consente di calcolare un throughput attendibile.
        if self.elapsed_ns == 0 or self.attempts == 0:
            return None
        return self.attempts / self.elapsed_seconds

    @property
    def estimated_full_seconds(self) -> float | None:
        """Estrapolazione lineare per tutto lo spazio, NON una durata osservata."""
        if self.attempts_per_second is None:
            return None
        return (self.elapsed_seconds / self.attempts) * self.total_combinations


def brute_force_search(
    target: str,
    alphabet: str = DEFAULT_ALPHABET,
    *,
    max_attempts: int = DEFAULT_MAX_ATTEMPTS,
) -> SearchResult:
    """Cerca target in uno spazio noto e si ferma al successo o al limite.

    target deve essere non vuoto e composto da simboli dell'alfabeto. Non
    conoscere la lunghezza richiederebbe una ricerca su piu' lunghezze.
    """
    validate_alphabet(alphabet)
    if not isinstance(target, str):
        raise TypeError("Il bersaglio deve essere una stringa.")
    validate_length(len(target))
    if any(character not in alphabet for character in target):
        raise ValueError("Il bersaglio contiene caratteri assenti dall'alfabeto.")
    if isinstance(max_attempts, bool) or not isinstance(max_attempts, int):
        raise TypeError("Il limite dei tentativi deve essere un intero.")
    if max_attempts < 1:
        raise ValueError("Il limite dei tentativi deve essere maggiore di zero.")

    total = len(alphabet) ** len(target)
    attempts = 0

    # La misura comprende creazione dell'iteratore, generazione dei candidati,
    # conteggio e confronto. Esclude input, validazione e stampa dei risultati.
    start_ns = perf_counter_ns()
    for candidate in islice(iter_candidates(len(target), alphabet), max_attempts):
        attempts += 1
        # Il risultato del confronto viene finalmente usato per fermarsi.
        if candidate == target:
            return SearchResult(candidate, attempts, total, perf_counter_ns() - start_ns)

    # Un limite raggiunto non dimostra che il bersaglio sia irraggiungibile.
    return SearchResult(None, attempts, total, perf_counter_ns() - start_ns)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Demo locale: genera o scegli un bersaglio e cercalo per tentativi."
    )
    target_group = parser.add_mutually_exclusive_group()
    target_group.add_argument("--length", type=int, help=f"Genera un bersaglio di 1-{MAX_LENGTH} caratteri.")
    target_group.add_argument("--password", help="Bersaglio di prova gia' noto, per una demo ripetibile.")
    parser.add_argument("--alphabet", default=DEFAULT_ALPHABET, help="Simboli unici, nell'ordine di ricerca.")
    parser.add_argument("--max-attempts", type=int, default=DEFAULT_MAX_ATTEMPTS,
                        help=f"Limite dei tentativi (predefinito: {DEFAULT_MAX_ATTEMPTS}).")
    parser.add_argument("--version", action="version", version=__version__)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        validate_alphabet(args.alphabet)
        if args.password is not None:
            target = args.password
        else:
            length = args.length
            if length is None:
                # Il dialogo storico rimane disponibile senza opzioni CLI.
                text = input(f"Lunghezza della password di prova (1-{MAX_LENGTH}) [4]: ")
                length = int(text) if text.strip() else 4
            target = generate_password(length, args.alphabet)

        result = brute_force_search(target, args.alphabet, max_attempts=args.max_attempts)
    except (TypeError, ValueError) as error:
        print(f"Errore: {error}", file=sys.stderr)
        return 2
    except EOFError:
        print("Errore: input assente; usa --length oppure --password.", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("\nRicerca interrotta dall'utente.", file=sys.stderr)
        return 130

    print("\nBRUTEFORSE 2.0 | dimostrazione locale")
    print(f"Bersaglio di prova: {target}")
    print(f"Combinazioni a lunghezza fissa: {result.total_combinations}")
    print(f"Tentativi eseguiti: {result.attempts}")
    if result.found:
        print(f"Password trovata: {result.password}")
    else:
        print("Limite dei tentativi raggiunto: ricerca incompleta.")
    print(f"Tempo effettivo: {result.elapsed_seconds:.9f} s ({result.elapsed_milliseconds:.6f} ms)")
    if result.attempts_per_second is not None:
        print(f"Velocita' media osservata: {result.attempts_per_second:.2f} tentativi/s")
        print(f"Estrapolazione indicativa su tutto lo spazio: {result.estimated_full_seconds:.9f} s")
    else:
        print("Misura troppo breve per calcolare velocita' ed estrapolazione.")
    return 0 if result.found else 1


if __name__ == "__main__":
    raise SystemExit(main())
