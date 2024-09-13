import json
import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, storage

load_dotenv()


def load_config():
    with open("config.json", "r") as json_file:
        config = json.load(json_file)
        # Substitui os placeholders pelas variáveis de ambiente
        config["type"] = os.getenv("type")
        config["project_id"] = os.getenv("project_id")
        config["private_key_id"] = os.getenv("private_key_id")
        config["private_key"] = os.getenv("private_key")
        config["client_email"] = os.getenv("client_email")
        config["client_id"] = os.getenv("client_id")
        config["auth_uri"] = os.getenv("auth_uri")
        config["token_uri"] = os.getenv("token_uri")
        config["auth_provider_x509_cert_url"] = os.getenv("auth_provider_x509_cert_url")
        config["client_x509_cert_url"] = os.getenv("client_x509_cert_url")
        config["universe_domain"] = os.getenv("universe_domain")
    return config


def initialize_firebase():
    if not firebase_admin._apps:
        config = load_config()
 
        cred = credentials.Certificate(config)
  
        firebase_admin.initialize_app(
            cred,
            {"storageBucket": os.getenv("FIREBASE_BUCKET")},
        )

    return storage.bucket()
