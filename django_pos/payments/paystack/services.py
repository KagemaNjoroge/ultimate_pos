from dotenv import load_dotenv
import os
import requests

load_dotenv()

paystack_live_secret_key = os.getenv("PAYSTACK_LIVE_SECRET_KEY")
paystack_charge_url = "https://api.paystack.co/charge"
paystack_verify_url = "https://api.paystack.co/transaction/verify/"


def request_payment(phone, amount, email, currency="KES"):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {paystack_live_secret_key}",
    }
    body = {
        "currency": currency,
        "email": email,
        amount: amount,
        "mobile_money": {
            "phone": phone,
            "provider": "mpesa",
        },
    }

    response = requests.post(paystack_charge_url, json=body, headers=headers)
    if response.status_code == 200:
        return {"status": "success", "data": response.json()}
    else:
        return {"status": "error", "data": response.json()}


def verify_payment(reference):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {paystack_live_secret_key}",
    }
    response = requests.get(f"{paystack_verify_url}{reference}", headers=headers)
    if response.status_code == 200:
        return {"status": "success", "data": response.json()}
    else:
        return {"status": "error", "data": response.json()}
