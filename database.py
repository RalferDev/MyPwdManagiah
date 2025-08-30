import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from security import encrypt_data, decrypt_data

# Carica le variabili d'ambiente dal file .env
load_dotenv()

# Prendi l'intera stringa di connessione dal file .env
MONGO_URI = os.getenv("MONGO_URI")

# Controlla se la variabile d'ambiente è stata impostata
if not MONGO_URI:
    print("❌ ERRORE: Imposta la variabile MONGO_URI nel tuo file .env")
    exit() # Esce dal programma se la stringa di connessione manca


class Database:
    def __init__(self):
        self.client = None
        try:
            self.client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
            self.client.server_info()
            self.db = self.client.password_manager_db
            self.collection = self.db.credentials
            print("✅ MongoDB connection and authentication successful.")
        except OperationFailure as e:
            print(f"❌ Autenticazione fallita: Controlla la stringa MONGO_URI nel file .env. Dettagli: {e.details}")
            self.client = None
        except ConnectionFailure as e:
            print(f"❌ Connessione a MongoDB fallita. Il container Docker è in esecuzione? Dettagli: {e}")
            self.client = None

    def save_password(self, website_url, username, password):
        """Encrypts and saves credentials to the database."""
        if not self.client:
            print("Impossibile salvare la password, nessuna connessione al database.")
            return None

        encrypted_username = encrypt_data(username)
        encrypted_password = encrypt_data(password)

        document = {
            "website_url": website_url.lower(),
            "username": encrypted_username,
            "password": encrypted_password
        }

        self.collection.update_one(
            {"website_url": website_url.lower()},
            {"$set": document},
            upsert=True
        )
        print(f"Credenziali per {website_url} salvate.")

    def get_password(self, website_url):
        """Retrieves and decrypts credentials from the database."""
        if not self.client:
            print("Impossibile ottenere la password, nessuna connessione al database.")
            return None

        document = self.collection.find_one({"website_url": website_url.lower()})

        if document:
            decrypted_username = decrypt_data(document["username"])
            decrypted_password = decrypt_data(document["password"])
            return {"username": decrypted_username, "password": decrypted_password}

        return None
