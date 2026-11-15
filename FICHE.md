# Fiche projet : Pharmacie Nabeul

**Étudiant :** Ahmed Boumaiza · **Module :** DevOps, L3 DSI, ISET · **Dépôt :** https://github.com/Ahmedboumaizaa1/Pharmacie-Nabeul

## Architecture

```
 Développeur --git push--> GitHub --pipeline--> GHCR (image)
                                                   |
                         tag vX.Y.Z -- release ----+ (re-étiquetage, pas de reconstruction)
                                                   |
                                       deploy_test (Docker Compose)
                                       +--------------------------+
                       port 8000 ----> | app (Flask, non root)    |
                                       |        | nom de service  |
                                       |        v                 |
                                       | db (PostgreSQL, sans port|
                                       |     publié) + volume     |
                                       +--------------------------+
```

- **Application :** Flask, SQLAlchemy et PostgreSQL. Routes : `/health` (contrôle de la base, renvoie la version), `GET /pharmacies` (filtre `?quartier=`) et `POST /pharmacies`.
- **Conteneur :** image `python:3.12-slim`, utilisateur non root, `HEALTHCHECK`.
- **Compose :** `app` et `db` ; l'application joint la base par le nom `db` ; le port de la base n'est pas publié ; données dans le volume `db_data` ; `app` démarre seulement quand `db` est sain.
- **Pipeline (GitHub Actions) :** `test` (Python 3.11 et 3.12) → `build` → `release` (tag) → `deploy_test`.
- **Protection de main :** ruleset exigeant une PR et les contrôles `test (3.11)` et `test (3.12)`.

## Version mise en service

- Version : `v1.1.0` (précédente : `v1.0.0`), image `ghcr.io/ahmedboumaizaa1/pharmacie-nabeul:v1.1.0`
- Pipeline réussi (PR #3) : https://github.com/Ahmedboumaizaa1/Pharmacie-Nabeul/actions/runs/43728951243
- Pipeline en échec (PR #2) : https://github.com/Ahmedboumaizaa1/Pharmacie-Nabeul/actions/runs/43727618964
- Mise en service du tag v1.1.0 : https://github.com/Ahmedboumaizaa1/Pharmacie-Nabeul/actions/runs/43729126095

## Déroulé du retour arrière

1. Version courante `v1.1.0` en service dans l'environnement de test.
2. Décision de revenir en arrière (raison : retour démontré pour la soutenance).
3. Actions, workflow « Retour arrière », Run workflow, version = `v1.0.0` (en local : `scripts/deploy.sh v1.0.0`).
4. L'image `v1.0.0` déjà publiée est tirée, non reconstruite (`--no-build`) ; Compose recrée le service `app`.
5. `--wait` puis `scripts/check.sh` renvoient 0 : `/health` affiche `"version": "v1.0.0"`.
6. Les données sont intactes grâce au volume `db_data`.

Exécution : https://github.com/Ahmedboumaizaa1/Pharmacie-Nabeul/actions/runs/43730061659