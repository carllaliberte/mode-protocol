#!/usr/bin/env python3
"""Physics locks for MODE v0. Tests, not a theorem. Not a QUANTUM seal."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import mode  # noqa: E402


def _quelle(**overrides):
    carte = {
        "id": "QL-test",
        "source": "qrng",
        "appareil": "IDQ-Quantis",
        "simule": False,
    }
    carte.update(overrides)
    return carte


def _temoin(**overrides):
    carte = {
        "temoin_id": "TM-test",
        "niveau": "fabricant",
    }
    carte.update(overrides)
    return carte


def _epsilon(**overrides):
    carte = {
        "epsilon_id": "EP-test",
        "modele": "composable",
        "epsilon": 1e-6,
    }
    carte.update(overrides)
    return carte


def _horizon(**overrides):
    carte = {
        "horizon_id": "HZ-test",
        "suite": "UFHY1",
        "re_presser_avant": "2028-08-31",
    }
    carte.update(overrides)
    return carte


def _juger(**overrides):
    kwargs = {
        "quelle": _quelle(),
        "temoin": _temoin(),
        "epsilon": _epsilon(),
        "horizon": _horizon(),
    }
    kwargs.update(overrides)
    return mode.juger(**kwargs)


def _dump(obj) -> str:
    return json.dumps(obj, ensure_ascii=False)


class MissingFourCardsIsClassique(unittest.TestCase):
    def test_juger_without_cards_is_classique(self):
        jugement = mode.juger()
        self.assertEqual(jugement["mode"], "classique")
        self.assertIn("quelle absente", jugement["raisons"])
        self.assertIn("temoin absent", jugement["raisons"])
        self.assertIn("epsilon absent", jugement["raisons"])
        self.assertIn("horizon absent", jugement["raisons"])

    def test_example_classique_card_names_four_absences(self):
        carte = json.loads((ROOT / "examples" / "classique.mode.json").read_text(encoding="utf-8"))
        self.assertEqual(carte["mode"], "classique")
        self.assertIn("quelle absente", carte["raisons"])
        self.assertIn("temoin absent", carte["raisons"])
        self.assertIn("epsilon absent", carte["raisons"])
        self.assertIn("horizon absent", carte["raisons"])

    def test_cli_juger_without_cards_is_classique(self):
        proc = subprocess.run(
            [sys.executable, str(ROOT / "mode.py"), "juger"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        out = json.loads(proc.stdout)
        self.assertEqual(out["mode"], "classique")
        self.assertIn("quelle absente", out["raisons"])
        self.assertIn("epsilon absent", out["raisons"])


class QuelleOsIsClassique(unittest.TestCase):
    def test_quelle_os_is_phone_entropy_classique(self):
        jugement = _juger(quelle=_quelle(source="os"))
        self.assertEqual(jugement["mode"], "classique")
        self.assertTrue(any("os" in r and "qrng|qkd" in r for r in jugement["raisons"]))

    def test_quelle_os_does_not_mint_quantique_even_with_other_gates(self):
        jugement = _juger(quelle=_quelle(source="os", appareil="iphone", simule=False))
        self.assertEqual(jugement["mode"], "classique")
        self.assertNotEqual(jugement["mode"], "quantique")


class EpsilonZeroIsALie(unittest.TestCase):
    def test_epsilon_zero_refuses_quantique(self):
        jugement = _juger(epsilon=_epsilon(epsilon=0))
        self.assertEqual(jugement["mode"], "classique")
        self.assertTrue(any("ε=0" in r or "mensonge" in r for r in jugement["raisons"]))

    def test_epsilon_zero_float_refuses(self):
        jugement = _juger(epsilon=_epsilon(epsilon=0.0))
        self.assertEqual(jugement["mode"], "classique")
        self.assertTrue(any("ε=0" in r or "mensonge" in r for r in jugement["raisons"]))


class EpsilonOneIsNotABound(unittest.TestCase):
    def test_epsilon_one_refuses_quantique(self):
        jugement = _juger(epsilon=_epsilon(epsilon=1))
        self.assertEqual(jugement["mode"], "classique")
        self.assertTrue(any("(0, 1)" in r for r in jugement["raisons"]))
        self.assertFalse(any("(0, 1]" in r for r in jugement["raisons"]))

    def test_epsilon_one_float_refuses(self):
        jugement = _juger(epsilon=_epsilon(epsilon=1.0))
        self.assertEqual(jugement["mode"], "classique")
        self.assertTrue(any("hors (0, 1)" in r for r in jugement["raisons"]))

    def test_epsilon_above_one_refuses(self):
        jugement = _juger(epsilon=_epsilon(epsilon=1.1))
        self.assertEqual(jugement["mode"], "classique")
        self.assertTrue(any("(0, 1)" in r for r in jugement["raisons"]))


class MissingEpsilonIsNotZero(unittest.TestCase):
    def test_epsilon_field_missing_is_absent_not_zero(self):
        carte = {"epsilon_id": "EP-missing", "modele": "composable"}
        jugement = _juger(epsilon=carte)
        self.assertEqual(jugement["mode"], "classique")
        self.assertIn("epsilon: ε absent", jugement["raisons"])
        self.assertFalse(any("ε=0" in r for r in jugement["raisons"]))
        self.assertFalse(any("mensonge" in r for r in jugement["raisons"]))

    def test_epsilon_null_is_absent_not_zero(self):
        jugement = _juger(epsilon=_epsilon(epsilon=None))
        self.assertEqual(jugement["mode"], "classique")
        self.assertIn("epsilon: ε absent", jugement["raisons"])
        self.assertFalse(any("ε=0" in r for r in jugement["raisons"]))

    def test_epsilon_card_absent_is_not_written_as_zero(self):
        jugement = _juger(epsilon=None)
        self.assertEqual(jugement["mode"], "classique")
        self.assertIn("epsilon absent", jugement["raisons"])
        self.assertFalse(any("ε=0" in r for r in jugement["raisons"]))


class QuantiqueOnlyIfGatesHold(unittest.TestCase):
    def test_four_gates_with_epsilon_in_open_interval_is_quantique(self):
        jugement = _juger()
        self.assertEqual(jugement["mode"], "quantique")
        self.assertEqual(jugement["raisons"], [])

    def test_cli_juger_with_four_gates(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = {}
            for nom, carte in (
                ("quelle", _quelle()),
                ("temoin", _temoin()),
                ("epsilon", _epsilon()),
                ("horizon", _horizon()),
            ):
                p = Path(tmp) / (nom + ".json")
                p.write_text(json.dumps(carte), encoding="utf-8")
                paths[nom] = str(p)
            proc = subprocess.run(
                [
                    sys.executable, str(ROOT / "mode.py"), "juger",
                    "--quelle", paths["quelle"],
                    "--temoin", paths["temoin"],
                    "--epsilon", paths["epsilon"],
                    "--horizon", paths["horizon"],
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=True,
            )
            out = json.loads(proc.stdout)
            self.assertEqual(out["mode"], "quantique")


class NoQuantumSealInJson(unittest.TestCase):
    def test_juger_json_is_not_a_quantum_seal(self):
        dumped = _dump(mode.juger())
        self.assertNotIn("QUANTUM", dumped)
        self.assertNotIn("quantum seal", dumped.lower())
        self.assertNotIn("Quantum Mode ON", dumped)

    def test_ecrire_json_is_not_a_quantum_seal(self):
        dumped = _dump(mode.ecrire())
        self.assertNotIn("QUANTUM", dumped)
        self.assertNotIn("quantum seal", dumped.lower())
        self.assertEqual(json.loads(dumped)["mode"], "classique")

    def test_quantique_verdict_json_is_not_a_quantum_seal(self):
        dumped = _dump(_juger())
        self.assertEqual(json.loads(dumped)["mode"], "quantique")
        self.assertNotIn("QUANTUM", dumped)
        self.assertNotIn("Imagine", dumped)


class SimuleIsAPresentedClaim(unittest.TestCase):
    def test_quelle_os_is_classique_and_not_a_simulation(self):
        jugement = _juger(quelle=_quelle(source="os"))
        self.assertEqual(jugement["mode"], "classique")
        self.assertIs(jugement["simule"], False)

    def test_no_cards_is_classique_and_not_a_simulation(self):
        jugement = mode.juger()
        self.assertEqual(jugement["mode"], "classique")
        self.assertIs(jugement["simule"], False)

    def test_ecrire_without_cards_does_not_restamp_simule(self):
        carte = mode.ecrire()
        self.assertEqual(carte["mode"], "classique")
        self.assertIs(carte["simule"], False)

    def test_epsilon_zero_refuse_is_not_a_simulation(self):
        jugement = _juger(epsilon=_epsilon(epsilon=0))
        self.assertEqual(jugement["mode"], "classique")
        self.assertIs(jugement["simule"], False)

    def test_epsilon_one_refuse_is_not_a_simulation(self):
        jugement = _juger(epsilon=_epsilon(epsilon=1))
        self.assertEqual(jugement["mode"], "classique")
        self.assertIs(jugement["simule"], False)

    def test_epsilon_zero_plus_quelle_simule_keeps_the_claim(self):
        jugement = _juger(quelle=_quelle(simule=True), epsilon=_epsilon(epsilon=0))
        self.assertEqual(jugement["mode"], "classique")
        self.assertIs(jugement["simule"], True)
        self.assertIn("quelle: simule", jugement["raisons"])

    def test_four_gates_with_quelle_simule_is_classique_and_simule(self):
        jugement = _juger(quelle=_quelle(simule=True))
        self.assertEqual(jugement["mode"], "classique")
        self.assertIs(jugement["simule"], True)
        self.assertIn("quelle: simule", jugement["raisons"])

    def test_example_classique_card_is_not_a_simulation(self):
        carte = json.loads((ROOT / "examples" / "classique.mode.json").read_text(encoding="utf-8"))
        self.assertEqual(carte["mode"], "classique")
        self.assertIs(carte["simule"], False)


class Ufhy1IsASuiteNotADate(unittest.TestCase):
    def test_ufhy1_as_calendar_date_is_refused(self):
        jugement = _juger(horizon=_horizon(re_presser_avant="UFHY1"))
        self.assertEqual(jugement["mode"], "classique")
        self.assertTrue(any("date" in r for r in jugement["raisons"]))


class ReadmeDoorCopy(unittest.TestCase):
    def test_readme_has_no_imagine_word(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertNotIn("Imagine", text)
        self.assertNotIn("imagine", text)

    def test_readme_does_not_claim_formal_verification(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertNotIn("formally verified", text)
        self.assertNotIn("formally-verified", text)

    def test_readme_uses_exclusive_unit_interval(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("(0, 1)", text)
        self.assertNotIn("(0, 1]", text)
        self.assertIn("python3 mode.py juger", text)

    def test_copy_on_this_rail_has_no_closed_interval(self):
        for rel in ("README.md", "INTERDIT.md", "JUGE.md", "mode.py"):
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertNotIn("(0, 1]", text, msg=rel)


if __name__ == "__main__":
    unittest.main()
