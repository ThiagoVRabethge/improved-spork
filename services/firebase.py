import json
import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, storage

load_dotenv()


def initialize_firebase():
    if not firebase_admin._apps:
        service_account_info = json.loads(os.getenv("FIREBASE_SERVICE_ACCOUNT"))
 
        cred = credentials.Certificate(service_account_info)
  
        firebase_admin.initialize_app(
            cred,
            {"storageBucket": os.getenv("FIREBASE_BUCKET")},
        )

    return storage.bucket()
