# MODE Protocol

**Classique par défaut. Quantique seulement si les bornes tiennent.**

MODE n'allume pas un ordinateur quantique. Il juge si le dossier a le droit de porter l'étiquette `quantique`.

Sur un téléphone sans dongle, le mode reste `classique`. C'est correct.

MIT. Voir [INTERDIT.md](INTERDIT.md).

## Primitive

```
QUELLE + TÉMOIN + EPSILON + HORIZON  →  verdict MODE
```

`quantique` exige :
- QUELLE `qrng|qkd` + appareil + pas simulé
- TÉMOIN `fabricant|di` (`di` exige transcript)
- EPSILON nombre ∈ (0, 1]
- HORIZON date calendrier `YYYY-MM-DD` encore à venir

`UFHY1` = Ed25519 + ML-DSA-65. C'est une **suite**, pas une date. Le juge refuse le slogan.

```bash
python3 mode.py juger
python -m quantum peut-dire --fichier carte.json   # exit 0 | 2
```

Sans les quatre cartes : `classique`.
Hôte cité : https://acorn-royal-dune-blend.grok.me
