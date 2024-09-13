import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, storage

load_dotenv()


def initialize_firebase():
    if not firebase_admin._apps:
        test = {
            "type": os.getenv("type"),
            "project_id": os.getenv("project_id"),
            "private_key_id": os.getenv("private_key_id"),
            "private_key": os.getenv("private_key"),
            "client_email": os.getenv("client_email"),
            "client_id": os.getenv("client_id"),
            "auth_uri": os.getenv("auth_uri"),
            "token_uri": os.getenv("token_uri"),
            "auth_provider_x509_cert_url": os.getenv("auth_provider_x509_cert_url"),
            "client_x509_cert_url": os.getenv("client_x509_cert_url"),
            "universe_domain": os.getenv("universe_domain"),
        }
 
        cred = credentials.Certificate(test)
  
        firebase_admin.initialize_app(
            cred,
            {"storageBucket": os.getenv("FIREBASE_BUCKET")},
        )

    return storage.bucket()
