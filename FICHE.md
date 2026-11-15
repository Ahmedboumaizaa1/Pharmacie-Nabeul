# Fiche projet : Pharmacie Nabeul

**Étudiant :** ____________  **Groupe :** ____________  **Dépôt :** ____________

## Architecture

```
 Développeur ──git push──> GitLab ──pipeline──> Registry (image)
                                                    │
                          tag vX.Y.Z ── release ────┘ (re-étiquetage, pas de reconstruction)
                                                    │
                                        deploy_test (Docker Compose)
                                        ┌──────────────────────────┐
                        port 8000  ───> │ app (Flask, non root)    │
                                        │        │ nom de service  │
                                        │        ▼                 │
                                        │ db (PostgreSQL, sans port│
                                        │     publié) + volume     │
                                        └──────────────────────────┘
```

- **Application :** Flask, routes `/health`, `/pharmacies` (GET, POST).
- **Conteneur :** image `python:3.12-slim`, utilisateur non root, `HEALTHCHECK`.
- **Compose :** `app` et `db`; l'application joint la base par le nom `db`; le port de la base n'est pas publié;
  les données sont dans le volume `db_data`; `app` démarre seulement quand `db` est sain.
- **Pipeline :** `test` (Python 3.11 et 3.12) → `build` → `release` (tag) → `deploy_test`.

## Version mise en service

- Version : `v1.0.0` (tag Git, image `registry/.../pharmacie-nabeul:v1.0.0`)
- Date de mise en service : ____________
- Adresse du pipeline réussi : ____________
- Adresse du pipeline en échec : ____________

## Déroulé du retour arrière

1. Version courante `v1.1.0` : `/health` affiche `"version": "v1.1.0"`.
2. Décision de revenir en arrière (raison : ____________).
3. Lancement du job manuel `rollback_test` avec `ROLLBACK_VERSION=v1.0.0`
   (en local : `scripts/deploy.sh v1.0.0`).
4. L'image `v1.0.0` déjà publiée est tirée, non reconstruite; Compose recrée le service `app`.
5. `scripts/check.sh` renvoie 0 et `/health` affiche `"version": "v1.0.0"`.
6. Les données sont intactes grâce au volume `db_data`.
