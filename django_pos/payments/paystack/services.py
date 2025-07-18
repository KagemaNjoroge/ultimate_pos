from dotenv import load_dotenv
import os
import requests

load_dotenv()

paystack_live_secret_key = os.getenv("PAYSTACK_LIVE_SECRET_KEY")
paystack_charge_url = "https://api.paystack.co/charge"
paystack_verify_url = "https://api.paystack.co/transaction/verify/"
paystack_transactions_list_url = "https://api.paystack.co/transaction"

TIMEOUT = 10  # seconds


class PaymentError(Exception):
    """Custom exception for payment errors."""

    pass


class PaymentService:
    def __init__(self, secret_key=None):
        self.secret_key = secret_key or paystack_live_secret_key
        if not self.secret_key:
            raise PaymentError("Paystack secret key is not set.")

    def _get_headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.secret_key}",
        }

    def _make_request(self, method, url, data=None):
        headers = self._get_headers()
        try:
            if method.lower() == "post":
                response = requests.post(
                    url, json=data, headers=headers, timeout=TIMEOUT
                )
            elif method.lower() == "get":
                response = requests.get(url, headers=headers, timeout=TIMEOUT)
            else:
                raise PaymentError("Unsupported HTTP method.")

            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise PaymentError(f"Payment request failed: {str(e)}")

    def request_mpesa_payment(self, phone, email, amount, currency="KES"):
        data = {
            "email": email,
            "amount": int(amount * 100),  # Paystack expects amount in cents
            "currency": currency,
            "mobile_money": {
                "phone": phone,  # Assuming email is used as phone for M-Pesa
                "provider": "mpesa",
            },
        }
        return self._make_request("post", paystack_charge_url, data)

    def list_payments(self):
        return self._make_request("get", paystack_transactions_list_url)

    def verify_payment(self, reference):
        url = f"{paystack_verify_url}{reference}"
        return self._make_request("get", url)
