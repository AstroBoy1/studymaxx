import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("fire-5a6ba-e3c9ccfcc757.json")

app = firebase_admin.initialize_app(cred)

db = firestore.client()

# doc_ref = db.collection("users").document("guest")
# doc_ref.set({"hours": "20", "last": "Lovelace", "reminders": "no", "pomodoro": "no"})
users_ref = db.collection("users")
docs = users_ref.stream()

for doc in docs:
    print(f"{doc.id} => {doc.to_dict()}")