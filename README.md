# MODE Protocol

**Classique par défaut. Quantique seulement si les bornes tiennent.**

MODE n'allume pas un ordinateur quantique. Il juge si le dossier a le droit de porter l'étiquette `quantique`.

Sur un téléphone sans dongle, le mode reste `classique`. C'est correct. C'est le Wow.

MIT. Voir [INTERDIT.md](INTERDIT.md).

## Primitive

```
QUELLE + TÉMOIN + EPSILON + HORIZON + BRUIT?  →  fiche .mode.json
```

`quantique` exige : QUELLE `qrng|qkd` + appareil + pas simulé ; TÉMOIN `fabricant|di` ; EPSILON ε ∈ (0,1] ; HORIZON `UFHY1|mldsa87` encore devant soi. `UFHY1` = Ed25519 + ML-DSA-65.

```bash
python3 mode.py juger
python3 mode.py ecrire --vers carte.mode.json
```

Sans cartes matérielles : `classique`.
