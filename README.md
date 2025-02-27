# Service de reservation de billets

## Description

Ce projet a permit à développer une infrastructure résiliente et distribuée pour une application de gestion de réservation de billets. L'objectif principal est d'assurer la cohérence des données, une haute disponibilité et des performances  à travers l'intégration de divers services distribués.


## Equipe
Garcia Adrien
Deborde Clement 

## Défi rencontrés
curl non fonctionnel => on a utilisé  Invoke-WebRequest de powershell
Problème d'accès aux data mysql => nous n'avons pas souvent utiliser mysql et parfois l'accès avec l'user n'etait pas forcément garanti et provoquait des problèmes de connexion et donc d'accès aux datas 

## Architecture Générale

### Services

1. **API RESTful** : Interaction entre les différents composants. (FastAPI)
2. **MySQL** : Base de données relationnelle 
3. **Redis** (optionnel) : Mise en cache pour les données fréquemment consultées.
4. **etcd** : Stockage de la configuration distribuée et gestion des verrous distribués.
5. **Docker-Compose** : Déploiement et orchestration des composants.


## Configuration du Projet

### Prérequis

- Docker
- Docker-Compose
- Python

## Instructions de Déploiement

1. **Construire et démarrer un container Docker** :

   ```sh
   docker-compose up --build

 # Scénario de Test

## 1. Préparation de l'Environnement

On exécute cette requête pour construire ou restart les container dockers :
docker-compose up --build

## 2. Consultation des Billets Disponibles
Pour vérifier les billets disponibles pour l'événement créé, on utilise la commande powershell suivante :

```sh
Invoke-WebRequest -Uri "http://localhost:8000/evenements/1/billets" `
                  -Method Get

```
reponse :
```json
{
  "billets": 100
}
```
## 3. Réservation de Billets
Pour réserver un billet pour l'événement, on utilise la commande suivante sur powershell:
```sh
Invoke-WebRequest -Uri "http://localhost:8000/evenements/1/reserver" `
                  -Method Post `
                  -ContentType "application/json" `
                  -Body '{"utilisateur_id": 1}'
```
reponse

```json
{
  "message": "Billet reservé",
  "billets restants": 99
}
```
## 4.  Vérification de la Mise à Jour des Billets Disponibles
Après la réservation d'un billet, on vérifie à nouveau les billets disponibles :

```sh
Invoke-WebRequest -Uri "http://localhost:8000/evenements/1/billets" `
                  -Method Get
```
On peut s'apercevoir que le nombre de billets disponibles a changé 

```json
{
 "billets": 99
}
```
## 6.  Vérification des Sauvegardes
Pour vérifier que les sauvegardes fonctionnent correctement, On accéde aux journaux du conteneur de sauvegarde :

```sh
docker logs ticketing-system-master-api-1
```
On peut voir ici les events différents de notre conteneur docker 


## 7.  Gestion des Conflits de Réservation
Pour tester la gestion des conflits de réservation, On peut laisser le nombre de ticket initiaux a 1 dans initialization.sql et lancer 2 fois la requête pour voir si le dernier ticket peut etre reservé 2 fois

Ensuite, vérifiez que le nombre de billets disponibles a été correctement mis à jour et que les verrous distribués ont empêché les conflits :
```sh
Invoke-WebRequest -Uri "http://localhost:8000/evenements/1/billets" `
                  -Method Get
```
