"""Test dei requisiti della versione 2, senza dipendenze esterne."""
import contextlib
import io
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

import algoritmo as algo


class ValidationTests(unittest.TestCase):
    def test_alfabeto_vuoto_o_duplicato(self):
        for alphabet in ('', 'aa', 'aba'):
            with self.subTest(alphabet=alphabet), self.assertRaises(ValueError):
                algo.validate_alphabet(alphabet)

    def test_alfabeto_non_stringa(self):
        with self.assertRaises(TypeError):
            algo.validate_alphabet(['a', 's'])

    def test_lunghezza_fuori_limiti(self):
        for length in (-1, 0, algo.MAX_LENGTH + 1):
            with self.subTest(length=length), self.assertRaises(ValueError):
                algo.generate_password(length)

    def test_lunghezza_non_intera(self):
        for length in (True, 2.5, '3'):
            with self.subTest(length=length), self.assertRaises(TypeError):
                algo.generate_password(length)

    def test_bersaglio_vuoto(self):
        with self.assertRaises(ValueError):
            algo.brute_force_search('')

    def test_bersaglio_non_stringa(self):
        with self.assertRaises(TypeError):
            algo.brute_force_search(123)

    def test_bersaglio_fuori_alfabeto(self):
        with self.assertRaisesRegex(ValueError, 'assenti'):
            algo.brute_force_search('az', 'as')

    def test_limite_non_positivo(self):
        for limit in (0, -1):
            with self.subTest(limit=limit), self.assertRaises(ValueError):
                algo.brute_force_search('a', max_attempts=limit)

    def test_limite_non_intero(self):
        for limit in (True, 1.5):
            with self.subTest(limit=limit), self.assertRaises(TypeError):
                algo.brute_force_search('a', max_attempts=limit)


class GenerationTests(unittest.TestCase):
    def test_lunghezza_e_alfabeto(self):
        for length in (1, 4, algo.MAX_LENGTH):
            with self.subTest(length=length):
                password = algo.generate_password(length)
                self.assertEqual(len(password), length)
                self.assertTrue(set(password) <= set(algo.DEFAULT_ALPHABET))

    def test_estrazione_controllata(self):
        with patch.object(algo.secrets, 'choice', side_effect=['a', 's', 'k']):
            self.assertEqual(algo.generate_password(3), 'ask')

    def test_collisione_ammessa(self):
        self.assertEqual(algo.generate_password(3, 'x'), algo.generate_password(3, 'x'))

    def test_ordine_e_copertura_candidati(self):
        self.assertEqual(list(algo.iter_candidates(2, 'as')), ['aa', 'as', 'sa', 'ss'])

    def test_ordine_segue_alfabeto(self):
        self.assertEqual(list(algo.iter_candidates(2, 'sa')), ['ss', 'sa', 'as', 'aa'])

    def test_iteratore_senza_materializzare_lo_spazio(self):
        candidates = algo.iter_candidates(12)
        self.assertIs(iter(candidates), candidates)
        self.assertEqual(next(candidates), 'a' * 12)
        self.assertEqual(next(candidates), 'a' * 11 + 's')


class SearchTests(unittest.TestCase):
    def test_primo_candidato(self):
        result = algo.brute_force_search('aa', 'as')
        self.assertTrue(result.found)
        self.assertEqual(result.status, 'found')
        self.assertEqual(result.password, 'aa')
        self.assertEqual(result.attempts, 1)
        self.assertEqual(result.total_combinations, 4)

    def test_candidato_intermedio(self):
        self.assertEqual(algo.brute_force_search('sa', 'as').attempts, 3)

    def test_ultimo_candidato(self):
        result = algo.brute_force_search('ss', 'as')
        self.assertEqual(result.password, 'ss')
        self.assertEqual(result.attempts, 4)

    def test_tutti_i_bersagli_in_un_piccolo_spazio(self):
        # La rappresentazione binaria fornisce un oracolo indipendente per
        # ordine e posizione attesa, su 30 bersagli fra lunghezze 1 e 4.
        for length in range(1, 5):
            for rank in range(2 ** length):
                target = format(rank, f'0{length}b').translate(str.maketrans('01', 'as'))
                with self.subTest(target=target):
                    result = algo.brute_force_search(target, 'as')
                    self.assertEqual(result.password, target)
                    self.assertEqual(result.attempts, rank + 1)

    def test_limite_raggiunto_non_e_successo(self):
        result = algo.brute_force_search('ss', 'as', max_attempts=2)
        self.assertFalse(result.found)
        self.assertIsNone(result.password)
        self.assertEqual(result.status, 'limit_reached')
        self.assertEqual(result.attempts, 2)
        self.assertEqual(result.total_combinations, 4)

    def test_successo_esattamente_al_limite(self):
        result = algo.brute_force_search('as', 'as', max_attempts=2)
        self.assertTrue(result.found)
        self.assertEqual(result.attempts, 2)

    def test_si_ferma_senza_chiedere_un_altro_candidato(self):
        def candidates():
            yield 'aa'
            raise AssertionError('Non deve proseguire dopo il successo')
        with patch.object(algo, 'iter_candidates', return_value=candidates()):
            self.assertEqual(algo.brute_force_search('aa', 'as').attempts, 1)

    def test_limite_non_consuma_un_candidato_extra(self):
        def candidates():
            yield 'aa'
            raise AssertionError('Non deve generare oltre il limite')
        with patch.object(algo, 'iter_candidates', return_value=candidates()):
            self.assertEqual(algo.brute_force_search('ss', 'as', max_attempts=1).attempts, 1)

    def test_alfabeto_singolo(self):
        result = algo.brute_force_search('xxx', 'x')
        self.assertEqual(result.total_combinations, 1)
        self.assertEqual(result.attempts, 1)
        self.assertTrue(result.found)


class TimingTests(unittest.TestCase):
    def test_durata_completa_e_conversione(self):
        with patch.object(algo, 'perf_counter_ns', side_effect=[1_000_000_000, 2_250_000_000]):
            result = algo.brute_force_search('sa', 'as')
        self.assertEqual(result.elapsed_ns, 1_250_000_000)
        self.assertEqual(result.elapsed_seconds, 1.25)
        self.assertEqual(result.elapsed_milliseconds, 1250.0)
        self.assertAlmostEqual(result.attempts_per_second, 3 / 1.25)
        self.assertAlmostEqual(result.estimated_full_seconds, (1.25 / 3) * 4)

    def test_la_generazione_dei_candidati_e_cronometrata(self):
        events = []
        def clock():
            events.append('clock')
            return len(events) * 100
        def candidates(*args):
            events.append('generate')
            yield 'aa'
        with patch.object(algo, 'perf_counter_ns', side_effect=clock):
            with patch.object(algo, 'iter_candidates', side_effect=candidates):
                algo.brute_force_search('aa', 'as')
        self.assertEqual(events, ['clock', 'generate', 'clock'])

    def test_durata_nulla_non_divide_per_zero(self):
        with patch.object(algo, 'perf_counter_ns', return_value=42):
            result = algo.brute_force_search('a')
        self.assertEqual(result.elapsed_seconds, 0)
        self.assertIsNone(result.attempts_per_second)
        self.assertIsNone(result.estimated_full_seconds)


class CliTests(unittest.TestCase):
    def run_cli(self, *args, input_text=None):
        script = Path(algo.__file__).resolve()
        return subprocess.run([sys.executable, str(script), *args], input=input_text,
                              text=True, capture_output=True, timeout=10)

    def test_demo_ripetibile(self):
        result = self.run_cli('--password', 'sa', '--alphabet', 'as')
        self.assertEqual(result.returncode, 0)
        self.assertIn('Password trovata: sa', result.stdout)
        self.assertIn('Tentativi eseguiti: 3', result.stdout)
        self.assertIn('Tempo effettivo:', result.stdout)

    def test_ricerca_incompleta_exit_uno(self):
        result = self.run_cli('--password', 'ss', '--alphabet', 'as', '--max-attempts', '2')
        self.assertEqual(result.returncode, 1)
        self.assertIn('ricerca incompleta', result.stdout)
        self.assertNotIn('Password trovata:', result.stdout)

    def test_input_errati_senza_traceback(self):
        for value in ('0', '-2', 'ciao', '13'):
            with self.subTest(input=value):
                result = self.run_cli(input_text=value + '\n')
                self.assertEqual(result.returncode, 2)
                self.assertIn('Errore:', result.stderr)
                self.assertNotIn('Traceback', result.stderr)

    def test_eof_senza_traceback(self):
        result = self.run_cli(input_text='')
        self.assertEqual(result.returncode, 2)
        self.assertNotIn('Traceback', result.stderr)

    def test_opzioni_incompatibili(self):
        self.assertEqual(self.run_cli('--length', '2', '--password', 'aa').returncode, 2)

    def test_lunghezza_esplicita(self):
        result = self.run_cli('--length', '2', '--alphabet', 'x')
        self.assertEqual(result.returncode, 0)
        self.assertIn('Password trovata: xx', result.stdout)

    def test_interruzione(self):
        with patch('builtins.input', side_effect=KeyboardInterrupt):
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(algo.main([]), 130)


if __name__ == '__main__':
    unittest.main()
