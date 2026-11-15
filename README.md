# Pharmacie Nabeul

Mini-application web : les pharmacies de garde de Nabeul (Flask + PostgreSQL).
Projet de fin de module DevOps (Licence 3 DSI, ISET). Seule la chaîne DevOps est évaluée.

## Démarrer en une commande

```bash
docker compose up -d --build
```

Puis :

```bash
scripts/check.sh                      # code 0 si l'application est en bonne santé
curl http://localhost:8000/health
curl -X POST http://localhost:8000/pharmacies \
     -H "Content-Type: application/json" \
     -d '{"nom":"Pharmacie Centrale","quartier":"Centre-ville","telephone":"72 000 000"}'
curl "http://localhost:8000/pharmacies?quartier=Centre-ville"
```

Arrêter : `docker compose down` (les données restent dans le volume `db_data` ; `docker compose down -v` les supprime).

Mot de passe de la base : valeur de développement par défaut. Pour la changer, copier `.env.example` en `.env` (jamais commité).

## Routes

| Route | Rôle |
|---|---|
| `GET /health` | état de l'application, de la base et version en service |
| `GET /pharmacies[?quartier=...]` | pharmacies de garde (filtre optionnel) |
| `POST /pharmacies` | ajoute une pharmacie (`nom` et `quartier` obligatoires) |

## Tests en local

```bash
pip install -r requirements-dev.txt
pytest
```

## Chaîne CI/CD (GitHub Actions)

| Étape | Déclencheur | Ce qui se passe |
|---|---|---|
| `test` | pull request, branche principale | pytest sur Python 3.11 et 3.12, rapport JUnit en artefact |
| `build` | après `test` (`needs`) | construction de l'image, publiée sur GHCR sous le SHA du commit |
| `release` | tag `vX.Y.Z` | l'image du commit est re-étiquetée `vX.Y.Z` (jamais reconstruite) |
| `deploy_test` | tag `vX.Y.Z` | mise en service en environnement `test`, puis `scripts/check.sh` |
| Retour arrière | manuel (workflow `Retour arrière`) | remise en service de la version choisie (ex. `v1.0.0`) |

Protection de la branche principale (bonus) : Settings > Branches > Add rule sur `main` >
cocher « Require status checks to pass before merging » et choisir `test (3.11)` et `test (3.12)`.
Une pull request rouge ne peut alors plus être fusionnée.

## Scénario de démonstration (soutenance)

1. **PR verte** : créer une branche, modifier un détail, ouvrir une pull request, montrer le pipeline vert.
2. **PR rouge** : dans `app.py`, remplacer `pharmacies.c.quartier == quartier` par `pharmacies.c.quartier != quartier`.
   Le test `test_filtre_par_quartier` échoue : montrer la première erreur utile dans le journal du job `test`.
3. **Version** : fusionner une PR verte dans `main`, attendre le job `build`, puis créer le tag `v1.0.0`.
   Montrer `release` et `deploy_test`, puis `/health` qui affiche `"version": "v1.0.0"`.
4. **Retour arrière** : publier `v1.1.0` (un petit changement), la mettre en service, puis lancer le workflow
   `Retour arrière` (onglet Actions > Run workflow) avec la version `v1.0.0`.
   En local, la même chose se fait avec : `scripts/deploy.sh v1.0.0`.

## Limite à connaître

L'environnement de test du pipeline est la machine temporaire du job : elle disparaît à la fin.
Il prouve que la version démarre et passe le contrôle de santé. Pour un environnement qui reste en place, remplacer
`deploy_test` par une connexion SSH vers un serveur qui exécute `scripts/deploy.sh`.

Auteur : Ahmed Boumaiza
