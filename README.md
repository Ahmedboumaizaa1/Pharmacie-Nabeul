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

## Chaîne CI/CD (GitLab)

| Étape | Déclencheur | Ce qui se passe |
|---|---|---|
| `test` | merge request, branche principale | pytest sur Python 3.11 et 3.12, rapport JUnit en artefact |
| `build` | après `test` (`needs`) | construction de l'image, publiée sous le SHA du commit |
| `release` | tag `vX.Y.Z` | l'image du commit est re-étiquetée `vX.Y.Z` (jamais reconstruite) |
| `deploy_test` | tag `vX.Y.Z` | mise en service en environnement `test`, puis `scripts/check.sh` |
| `rollback_test` | manuel, sur un tag | remise en service de `ROLLBACK_VERSION` (par défaut `v1.0.0`) |

Protection de la branche principale (bonus) : GitLab > Settings > Merge requests >
cocher « Pipelines must succeed ». Une merge request rouge ne peut alors plus être fusionnée.

## Scénario de démonstration (soutenance)

1. **MR verte** : créer une branche, modifier un détail, ouvrir une merge request, montrer le pipeline vert.
2. **MR rouge** : dans `app.py`, remplacer `pharmacies.c.quartier == quartier` par `pharmacies.c.quartier != quartier`.
   Le test `test_filtre_par_quartier` échoue : montrer la première erreur utile dans le journal du job `test`.
3. **Version** : fusionner une MR verte dans la branche principale, attendre le job `build`, puis créer le tag `v1.0.0`.
   Montrer `release` et `deploy_test`, puis `/health` qui affiche `"version": "v1.0.0"`.
4. **Retour arrière** : publier `v1.1.0` (un petit changement), la mettre en service, puis lancer le job manuel
   `rollback_test` avec `ROLLBACK_VERSION=v1.0.0` et montrer que `/health` affiche de nouveau `v1.0.0`.
   En local, la même chose se fait avec : `scripts/deploy.sh v1.0.0`.

## Limite à connaître

L'environnement de test du pipeline est le moteur Docker temporaire du job (`docker:dind`) : il disparaît à la fin du job.
Il prouve que la version démarre et passe le contrôle de santé. Pour un environnement qui reste en place, remplacer
`deploy_test` par une connexion SSH vers un serveur qui exécute `scripts/deploy.sh`.
