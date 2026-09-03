# MODE Protocol

**Classique par défaut. Quantique seulement si les bornes tiennent.**

MODE n'allume pas un QPU. Il juge si le dossier a le droit de porter l'étiquette `quantique`.
`quantique` is a mode obligation, not a photon and not a QUANTUM seal.

On a phone without a dongle, the mode stays `classique`. That is correct.

This repository is version 0. Phone + free. MIT. See [INTERDIT.md](INTERDIT.md).

## Four keys

```
QUELLE + TÉMOIN + EPSILON + HORIZON  →  verdict MODE
```

`mode` is not a fifth field. MODE is the collapse of the four.
`quantique` only if every physical gate holds:

| Key | Gate |
|---|---|
| QUELLE | `qrng` \| `qkd` + appareil + not simulated |
| TÉMOIN | `fabricant` \| `di` (`di` requires a transcript) |
| EPSILON | composable ε ∈ (0, 1) **exclusive** |
| HORIZON | calendar date `YYYY-MM-DD` still ahead |

`quelle: os` is phone entropy = classique, not quantique. After [famille juge.v0](https://github.com/carllaliberte/famille/blob/main/schema/juge.v0.json) that line is locked.

`UFHY1` = Ed25519 + ML-DSA-65. It is a **suite** name, not a calendar date. The judge refuses the slogan.

## Physics locks (this rail)

- Classique by default. `quantique` only if QUELLE + TÉMOIN + EPSILON + HORIZON all hold.
- `quelle: os` = classique. Phone entropy does not mint the label.
- EPSILON on this rail matches [epsilon-protocol](https://github.com/carllaliberte/epsilon-protocol) `945ddce`: composable ε ∈ (0, 1) exclusive. `ε=0` is a lie. `ε=1` is not a bound.
- **Missing ε is not zero ε.** Named below as a FLAG on other consumers — not a theorem of this rail.
- No IBM Job. No QPU as a checked gate.
- QUANTUM signs later. Keys stay off Git. This repo is not a QUANTUM seal.
- Judgment = Carl: `python3 mode.py juger`.

### Missing ≠ zero (FLAG, not this theorem)

Absence of ε is not `epsilon: 0`. This rail does not treat “field missing” as “advantage zero”.

This rail does not unwind famille `d55799e` (sdk missing → `classique`).
This rail does not collapse the three-consumer FLAG into one rule:

| Consumer (closed — not this repo) | When ε is missing |
|---|---|
| acorn-juge Worker | `400 EPSILON_MISSING` |
| famille sdk (`d55799e`) | `classique` |
| GARDE | fail-closed |

Those consumers stay closed.

### Vitrine, not a seal

https://acorn-royal-dune-blend.grok.me is a nominative grok.me slug — not a FAMILLE-owned domain, not a seal.
The PREVIEW badge is not a `quantique` verdict.

## How to run

```bash
python3 mode.py juger
python3 mode.py juger --quelle carte.quelle.json --temoin carte.temoin.json --epsilon carte.epsilon.json --horizon carte.horizon.json
```

Sans les quatre cartes : `classique`. That is the honest default.

Physics locks (stdlib, no extra packages):

```bash
python3 -m unittest discover -s tests -v
```

## Verified vs assumed

Tests lock the rows below. Nothing in this repository is a theorem. Nothing here is a QUANTUM seal.

| Claim | Status |
|---|---|
| no cards → `classique` | **verified** by tests on this rail |
| `quelle: os` → `classique` | **verified** |
| `ε=0` is refused | **verified** |
| `ε=1` is refused | **verified** |
| missing ε is named absent, not written as zero | **verified** |
| JSON verdict is not a QUANTUM seal | **verified** |
| `UFHY1` as a calendar date is refused | **verified** |
| Portmann–Renner meaning of ε | **assumed** (paper, not proven here) |
| QUANTUM signature | **later** — keys off Git, not in this repo |
| EasyCrypt / formal-layer | **not here** |
| IBM Job / QPU as a gate | **refused** — not a checked field |

## What v0 is not

See [INTERDIT.md](INTERDIT.md). In short:

1. Do not write `mode: quantique` without the four gates.
2. Do not write `quantique` because QUELLE says `os`.
3. Do not paste a Job IBM / QuNetSim / webcam as a quantique verdict.
4. Do not write `quantique` + `simule` on QUELLE, TÉMOIN `di`, or BRUIT `fermes`.
5. No token, no badge « Quantum Mode ON ».
6. Do not write « quantum-safe » in place of an HORIZON suite.
7. Do not write `ε=0`. Do not write `ε=1` as a bound.
8. Do not treat missing ε as zero ε.

The default is `classique`. Refusing that default is the only lie.

## Famille

| Rail | Question |
|---|---|
| [FIGURE](https://github.com/carllaliberte/figure-protocol) | qui |
| [SITUS](https://github.com/carllaliberte/situs-protocol) | où |
| [UNFORGE](https://github.com/carllaliberte/unforge-check) | quoi |
| [QUELLE](https://github.com/carllaliberte/quelle) | d'où le bit |
| [TÉMOIN](https://github.com/carllaliberte/temoin-protocol) | avec quelle force |
| [HORIZON](https://github.com/carllaliberte/horizon-protocol) | jusqu'à quand le sceau tient |
| [EPSILON](https://github.com/carllaliberte/epsilon-protocol) | avec quel ε |
| [MODE](https://github.com/carllaliberte/mode-protocol) | le collapse des quatre |

MIT (protocoles) · Apache-2.0 (œil UNFORGE). QUANTUM signe **plus tard**. Les clés restent hors Git. Ce dépôt n'est pas un sceau QUANTUM.

## Fichiers

- [`INTERDIT.md`](INTERDIT.md) — ce qu'on ne prétend pas
- [`JUGE.md`](JUGE.md) — MODE lit, ne signe pas
- [`schema/mode.v0.json`](schema/mode.v0.json)
- [`mode.py`](mode.py) — `python3 mode.py juger`
- [`examples/classique.mode.json`](examples/classique.mode.json) — téléphone sans dongle
- [`tests/test_physics_locks.py`](tests/test_physics_locks.py) — verrous physiques
- [`.github/workflows/physics.yml`](.github/workflows/physics.yml) — CI des tests
