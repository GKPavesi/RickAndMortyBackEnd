import firebase_admin
from firebase_admin import credentials, auth

# cred = credentials.Certificate("src/firebase/firebase-rick-and-morty.json")

cred = credentials.Certificate("/etc/secrets/firebase-rick-and-morty.json")


firebase = firebase_admin.initialize_app(cred)