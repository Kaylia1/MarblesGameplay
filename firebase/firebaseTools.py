
import firebase_admin
from firebase_admin import credentials, firestore
import json
import sys
from pathlib import Path

class FirebaseTools:
    def __init__(self):
        # service account name: firebase-adminsdk-w7dfa@marbles-dcc42.iam.gserviceaccount.com
        self.service_key = Path(__file__).resolve().parent.parent / "secrets/marbles-dcc42-cred.json"

        self.cred = credentials.Certificate(self.service_key)
        firebase_admin.initialize_app(self.cred)

        # Initialize Firestore
        self.db = firestore.client()
        
        # currently only usage is marbles collection
        self.collection_name = 'points_collection'

    # creates a collection if collection does not exist 
    def storeData(self, jsonData):
        # Store data in a Firestore collection
        for doc_id, doc_data in jsonData.items():
            self.db.collection(self.collection_name).document(doc_id).set(doc_data)
        print("JSON data has been loaded into Firebase!")

    def loadData(self):
        # Retrieve all documents from the Firestore collection
        docs = self.db.collection(self.collection_name).stream()

        # Convert Firestore data to json
        retrieved_data = {doc.id: doc.to_dict() for doc in docs}

        print("Data retrieved from Firebase!")
        return retrieved_data

# only need one instance of this class for now
fb = FirebaseTools()