# database.py
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from security import encrypt_data, decrypt_data

MONGO_URI = "mongodb://Ralferdev:MongoPwdRalferdev@localhost:27017/?authSource=admin"

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
            print(f"❌ Authentication failed: {e.details}")
            self.client = None
        except ConnectionFailure as e:
            print(f"❌ MongoDB connection failed. Is the Docker container running? Details: {e}")
            self.client = None

    def save_password(self, website_url, username, password):
        if not self.client:
            print("Cannot save password, no database connection.")
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
        print(f"Credentials for {website_url} saved.")

    def get_password(self, website_url):
        if not self.client:
            print("Cannot get password, no database connection.")
            return None
        document = self.collection.find_one({"website_url": website_url.lower()})
        if document:
            decrypted_username = decrypt_data(document["username"])
            decrypted_password = decrypt_data(document["password"])
            return {"username": decrypted_username, "password": decrypted_password}
        return None