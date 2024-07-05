# Ticket Reservation System

## Description

Ce projet consiste à concevoir une infrastructure résiliente et distribuée pour une application de gestion de réservation de billets. Cette infrastructure garantit la cohérence des données, la haute disponibilité et des performances optimales via l'intégration de divers services distribués.


## Architecture Générale

### Services

1. **API RESTful** : Interaction entre les différents composants. (FastAPI)
2. **MySQL** : Base de données relationnelle pour stocker les informations des utilisateurs, événements et réservations.
3. **Redis** (optionnel) : Mise en cache pour les données fréquemment consultées.
4. **etcd** : Stockage de la configuration distribuée et gestion des verrous distribués.
5. **Docker-Compose** : Déploiement et orchestration des composants.


## Configuration du Projet

### Prérequis

- Docker
- Docker-Compose

## Instructions de Déploiement

1. **Construisez et démarrez les services Docker** :

   ```sh
   docker-compose up --build

 # Scénario de Test

## 1. Préparation de l'Environnement

Assurez-vous que tous les conteneurs sont en cours d'exécution :

```sh
docker-compose up --build
```
## 2. Consultation des Billets Disponibles
Pour vérifier les billets disponibles pour l'événement créé, utilisez la commande curl suivante :

```sh
curl -X GET "http://localhost:8000/events/1/tickets"
```
Vous devriez obtenir une réponse similaire à ceci :
```json
{
  "tickets": 100
}
```
## 3. Réservation de Billets
Pour réserver un billet pour l'événement, utilisez la commande curl suivante :
```sh
{
 curl -X POST "http://localhost:8000/events/1/reserve"

}
```
Vous devriez obtenir une réponse similaire à ceci :
```json
{
  "message": "Ticket reserved",
  "remaining_tickets": 99
}
```
## 4.  Vérification de la Mise à Jour des Billets Disponibles
Après la réservation d'un billet, vérifiez à nouveau les billets disponibles :

```sh
curl -X GET "http://localhost:8000/events/1/tickets"
```
Vous devriez obtenir une réponse indiquant que le nombre de billets disponibles a diminué :

```json
{
 "tickets": 99
}
```
## 6.  Vérification des Sauvegardes
Pour vérifier que les sauvegardes fonctionnent correctement, vous pouvez accéder aux journaux du conteneur de sauvegarde :

```sh
docker-compose logs backup
```
Vous devriez voir des entrées de journal indiquant que des sauvegardes ont été effectuées avec succès. Recherchez des lignes comme celles-ci (exemple ficitif):

```json
Starting backup at 20240626120000
Backup completed: /backups/backup_20240626120000.sql
```
## 7.  Gestion des Conflits de Réservation
Pour tester la gestion des conflits de réservation, vous pouvez essayer de réserver plusieurs billets simultanément. Vous pouvez utiliser un outil comme ab (ApacheBench) pour envoyer plusieurs requêtes de réservation en même temps 
```sh
ab -n 10 -c 5 -p reservation_payload.json -T application/json http://localhost:8000/events/1/reserve
```
Où reservation_payload.json contient le corps de la requête :
```json
{}
```
Ensuite, vérifiez que le nombre de billets disponibles a été correctement mis à jour et que les verrous distribués ont empêché les conflits :
```sh
curl -X GET "http://localhost:8000/events/1/tickets"
```
