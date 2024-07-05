from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
import etcd3
import redis

app = FastAPI()

# Connexion MySQL
try:
    db = mysql.connector.connect(
        host="mysql",
        user="root",
        password="example",
        database="ticket_db"
    )
except mysql.connector.Error as err:
    raise HTTPException(status_code=500, detail=f"Erreur de connexion MySQL : {err}")

# Connexion Redis
try:
    cache = redis.Redis(host="redis", port=6379)
    cache.ping()
except redis.RedisError as err:
    raise HTTPException(status_code=500, detail=f"Erreur de connexion Redis : {err}")

# Connexion Etcd
try:
    etcd = etcd3.client(host="etcd", port=2379)
    etcd.status()
except Exception as err:
    raise HTTPException(status_code=500, detail=f"Erreur de connexion Etcd : {err}")

class UtilisateurCreate(BaseModel):
    nom_utilisateur: str
    email: str
    mot_de_passe: str

class ReservationCreate(BaseModel):
    utilisateur_id: int

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/utilisateurs/")
async def creer_utilisateur(utilisateur: UtilisateurCreate):
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                       (utilisateur.nom_utilisateur, utilisateur.email, utilisateur.mot_de_passe))
        db.commit()
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Erreur MySQL : {err}")
    return {"message": "Utilisateur créé"}

@app.get("/evenements/{event_id}/billets")
async def obtenir_billets(event_id: int):
    # accéder au cache
    cache_key = f"event:{event_id}:tickets"
    if cache.exists(cache_key):
        tickets = cache.get(cache_key)
        return {"billets": int(tickets)}

    # curseur sur tout les tickets 
    cursor = db.cursor()
    cursor.execute("SELECT available_tickets FROM events WHERE id = %s", (event_id,))
    result = cursor.fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Événement non trouvé")

    available_tickets = result[0]
    cache.set(cache_key, available_tickets)
    return {"billets": available_tickets}

@app.post("/evenements/{event_id}/reserver")
async def reserver_billet(event_id: int, reservation: ReservationCreate):
    lock_key = f"event:{event_id}:lock"

    # Acquérir le verrou
    with etcd.lock(lock_key, ttl=60):
        cursor = db.cursor()
        cursor.execute("SELECT available_tickets FROM events WHERE id = %s FOR UPDATE", (event_id,))
        result = cursor.fetchone()
        if not result or result[0] <= 0:
            raise HTTPException(status_code=404, detail="Billets non disponibles")

        available_tickets = result[0] - 1
        cursor.execute("UPDATE events SET available_tickets = %s WHERE id = %s", (available_tickets, event_id))
        cursor.execute("INSERT INTO reservations (user_id, event_id) VALUES (%s, %s)", (reservation.utilisateur_id, event_id))
        db.commit()

        # Mettre à jour le cache
        cache_key = f"event:{event_id}:tickets"
        cache.set(cache_key, available_tickets)

    return {"message": "Billet réservé", "billets_restants": available_tickets}

@app.get("/sante")
async def verification_sante():
    try:
        db.ping(reconnect=True)
        cache.ping()
        etcd.status()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Service indisponible")
    return {"statut": "OK"}
