import firebase_admin
from dotenv import load_dotenv
from firebase_admin import firestore
from firebase_admin import credentials
import os
import pytz
import datetime

from company.models import Company
from company.models import Subscription


load_dotenv()
cred = credentials.Certificate(os.getenv("FIREBASE_CONFIG"))
app = firebase_admin.initialize_app(cred)


def add_subscription(end_date: datetime.datetime, notes: str = None) -> dict:
    # company is always the first company in the database
    company = Company.objects.first()
    if company == None:
        return {"message": "No company found", "status": "Failed"}
    else:
        subscription = Subscription(company=company, end_date=end_date, notes=notes)
        subscription.save()
        return {
            "message": "Subscription added successfully",
            "subscription": subscription.to_dict(),
            "status": "Okay",
        }


def save_subscription_to_firebase(subscription: Subscription) -> dict:
    db = firestore.client()
    doc_ref = db.collection("subscriptions").document(str(subscription.company.kra_pin))
    doc_ref.set(subscription.to_dict())
    return {"message": "Subscription saved to Firebase", "status": "Okay"}


def check_subscription_in_firebase(subscription: Subscription) -> dict:
    db = firestore.client()
    doc_ref = db.collection("subscriptions").document(subscription.company.kra_pin)
    doc = doc_ref.get()

    if doc.exists:
        # check if it has expired and deactivate it and if it has not expired, return the subscription
        data = doc.to_dict()

        end_date = data["end_date"]
        is_active = data["is_active"]

        if not is_active:
            return {
                "message": "Subscription has expired or has been deactivated",
                "status": "Failed",
            }
        if datetime.datetime.now(pytz.UTC) > end_date:
            doc_ref.update({"is_active": False})
            return {"message": "Subscription has expired", "status": "Failed"}
        return {
            "message": "Subscription found in Firebase",
            "status": "Okay",
            "subscription": data,
        }

    else:
        return {"message": "Subscription not found in Firebase", "status": "Failed"}



def verify_subscription(subs: Subscription) -> bool:
    # compare the subscription in the database with the one in Firebase
    db = firestore.client()
    doc_ref = db.collection("subscriptions").document(str(subs.company.kra_pin))
    doc = doc_ref.get()
    if doc.exists:
        data = doc.to_dict()
        if data["end_date"] == subs.end_date and data["is_active"] == subs.is_active:
            return True
        return False
    return False
