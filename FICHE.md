# \# Fiche projet : Pharmacie Nabeul

# \*\*Étudiant :\*\* Ahmed Boumaiza · \*\*Module :\*\* DevOps, L3 DSI, ISET · \*\*Dépôt :\*\* https://github.com/Ahmedboumaizaa1/Pharmacie-Nabeul

# 

# \## Architecture

# ```

# &#x20;Développeur ──git push──> GitHub ──pipeline──> GHCR (image)

# &#x20;                                                  │

# &#x20;                        tag vX.Y.Z ── release ────┘ (re-étiquetage, pas de reconstruction)

# &#x20;                                                  │

# &#x20;                                      deploy\_test (Docker Compose)

# &#x20;                                      ┌──────────────────────────┐

# &#x20;                      port 8000  ───> │ app (Flask, non root)    │

# &#x20;                                      │        │ nom de service  │

# &#x20;                                      │        ▼                 │

# &#x20;                                      │ db (PostgreSQL, sans port│

# &#x20;                                      │     publié) + volume     │

# &#x20;                                      └──────────────────────────┘

# ```

# \*\*Application :\*\* Flask, route `/health` et routes de gestion des pharmacies.

# \*\*Conteneur :\*\* image `python:3.12-slim`, utilisateur non root, `HEALTHCHECK`.

# \*\*Compose :\*\* services `app` et `db` ; l'application joint la base par le nom `db` ; le port de la base n'est pas publié ; les données sont dans le volume `db\\\\\\\_data` ; `app` démarre seulement quand `db` est sain.

# \*\*Pipeline (GitHub Actions) :\*\* `test` (Python 3.11 et 3.12) → `build` → `release` (tag) → `deploy\\\\\\\_test`.

# \*\*Protection de main :\*\* ruleset exigeant une PR et les contrôles `test (3.11)` et `test (3.12)`.

# 

# \## Version mise en service

# \- Version : `v1.1.0` (précédente : `v1.0.0`), image `ghcr.io/ahmedboumaizaa1/pharmacie-nabeul:v1.1.0`

# \- Pipeline réussi (PR #3) : https://github.com/Ahmedboumaizaa1/Pharmacie-Nabeul/actions/runs/43728951243

# \- Pipeline en échec (PR #2) : https://github.com/Ahmedboumaizaa1/Pharmacie-Nabeul/actions/runs/43727618964

# \- Mise en service du tag v1.1.0 : https://github.com/Ahmedboumaizaa1/Pharmacie-Nabeul/actions/runs/43729126095

# 

# \## Déroulé du retour arrière

# 1\. Version courante `v1.1.0` en service dans l'environnement de test.

# 2\. Décision de revenir en arrière (raison : \[MOTIF]).

# 3\. Actions, workflow « Retour arrière », Run workflow, version = `v1.0.0` (en local : `scripts/deploy.sh v1.0.0`).

# 4\. L'image `v1.0.0` déjà publiée est tirée, non reconstruite (`--no-build`) ; Compose recrée le service `app`.

# 5\. `--wait` puis `scripts/check.sh` renvoient 0 : `/health` répond.

# 6\. Les données sont intactes grâce au volume `db\\\\\\\_data`.

# Exécution : https://github.com/Ahmedboumaizaa1/Pharmacie-Nabeul/actions/runs/43730061659



