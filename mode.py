#!/usr/bin/env python3
"""MODE v0 — classique par défaut. quantique seulement si les bornes tiennent."""

from __future__ import annotations

import argparse
import json
import sys
import uuid
from datetime import date, datetime, timezone
from pathlib import Path

FORMAT = "mode.v0"
CHSH_MAX = 2 * (2**0.5)


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _load(chemin: str | None) -> dict | None:
    if not chemin:
        return None
    p = Path(chemin).expanduser()
    if not p.is_file():
        raise SystemExit("fichier introuvable : " + str(p))
    return json.loads(p.read_text(encoding="utf-8"))


def _garde_quelle(c: dict) -> list[str]:
    rat = []
    src = c.get("source")
    if src not in ("qrng", "qkd"):
        rat.append("quelle: source " + str(src) + " ≠ qrng|qkd")
    if not c.get("appareil"):
        rat.append("quelle: pas d'appareil")
    if c.get("simule") is True:
        rat.append("quelle: simule")
    return rat


def _garde_temoin(c: dict) -> list[str]:
    rat = []
    niv = c.get("niveau")
    if niv not in ("fabricant", "di"):
        rat.append("temoin: niveau " + str(niv) + " ≠ fabricant|di")
    if niv == "di":
        if c.get("simule") is True:
            rat.append("temoin: di + simule")
        t = c.get("transcript") or {}
        if not t.get("transcript_sha256"):
            rat.append("temoin: di sans transcript")
        chsh = t.get("chsh")
        if chsh is not None:
            try:
                x = float(chsh)
                if x <= 2:
                    rat.append("temoin: CHSH ≤ 2 (local)")
                if x > CHSH_MAX:
                    rat.append("temoin: CHSH > 2√2 (mensonge)")
            except (TypeError, ValueError):
                rat.append("temoin: CHSH illisible")
    return rat


def _garde_epsilon(c: dict) -> list[str]:
    rat = []
    if c.get("modele") in (None, "none"):
        rat.append("epsilon: modele none")
    eps = c.get("epsilon")
    if not isinstance(eps, (int, float)) or isinstance(eps, bool) or eps <= 0 or eps > 1:
        rat.append("epsilon: ε absent ou hors (0, 1]")
    return rat


def _garde_horizon(c: dict) -> list[str]:
    rat = []
    suite = c.get("suite")
    if suite not in ("UFHY1", "mldsa87"):
        rat.append("horizon: suite " + str(suite) + " ≠ UFHY1|mldsa87")
    jour = c.get("re_presser_avant")
    try:
        if not jour or date.fromisoformat(jour) <= datetime.now(timezone.utc).date():
            rat.append("horizon: date passée ou absente")
    except ValueError:
        rat.append("horizon: date illisible")
    return rat


def _garde_bruit(c: dict) -> list[str]:
    if c.get("trous") == "fermes" and c.get("simule") is True:
        return ["bruit: fermes + simule"]
    return []


def juger(quelle=None, temoin=None, epsilon=None, horizon=None, bruit=None) -> dict:
    raisons: list[str] = []
    if quelle is None:
        raisons.append("quelle absente")
    else:
        raisons.extend(_garde_quelle(quelle))
    if temoin is None:
        raisons.append("temoin absent")
    else:
        raisons.extend(_garde_temoin(temoin))
    if epsilon is None:
        raisons.append("epsilon absent")
    else:
        raisons.extend(_garde_epsilon(epsilon))
    if horizon is None:
        raisons.append("horizon absent")
    else:
        raisons.extend(_garde_horizon(horizon))
    if bruit is not None:
        raisons.extend(_garde_bruit(bruit))
    quantique = not raisons
    return {
        "mode": "quantique" if quantique else "classique",
        "raisons": [] if quantique else raisons,
        "quelle_id": (quelle or {}).get("id") or (quelle or {}).get("quelle_id"),
        "temoin_id": (temoin or {}).get("temoin_id") or (temoin or {}).get("id"),
        "epsilon_id": (epsilon or {}).get("epsilon_id"),
        "horizon_id": (horizon or {}).get("horizon_id"),
        "bruit_id": (bruit or {}).get("bruit_id") if bruit else None,
        "simule": not quantique,
        "note": "bornes tenues. étiquette quantique licite." if quantique else "mode classique. les raisons sont les bornes manquantes.",
    }


def ecrire(**kwargs) -> dict:
    j = juger(**kwargs)
    return {
        "format": FORMAT,
        "mode_id": "MD-" + uuid.uuid4().hex[:12],
        "mode": j["mode"],
        "quelle_id": j.get("quelle_id"),
        "temoin_id": j.get("temoin_id"),
        "epsilon_id": j.get("epsilon_id"),
        "horizon_id": j.get("horizon_id"),
        "bruit_id": j.get("bruit_id"),
        "raisons": j["raisons"],
        "simule": j["simule"],
        "juridiction": "QC",
        "langue": "fr-CA",
        "pose_at": _now(),
        "note": j["note"],
    }


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="mode")
    sub = p.add_subparsers(dest="cmd", required=True)
    for nom in ("juger", "ecrire"):
        s = sub.add_parser(nom)
        s.add_argument("--quelle", default=None)
        s.add_argument("--temoin", default=None)
        s.add_argument("--epsilon", default=None)
        s.add_argument("--horizon", default=None)
        s.add_argument("--bruit", default=None)
        if nom == "ecrire":
            s.add_argument("--vers", default="carte.mode.json")
    args = p.parse_args(argv)
    kwargs = dict(quelle=_load(args.quelle), temoin=_load(args.temoin), epsilon=_load(args.epsilon), horizon=_load(args.horizon), bruit=_load(args.bruit))
    if args.cmd == "juger":
        print(json.dumps(juger(**kwargs), ensure_ascii=False, indent=2))
        return 0
    carte = ecrire(**kwargs)
    Path(args.vers).write_text(json.dumps(carte, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    out = dict(carte); out["fichier"] = args.vers
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
