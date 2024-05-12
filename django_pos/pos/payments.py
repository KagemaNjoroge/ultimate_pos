from intasend import APIService
from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv("INTASEND_SECRET_API_KEY ")
publishable_key = os.getenv("INTASEND_PUBLIC_API_KEY")
service = APIService(token=token, publishable_key=publishable_key, test=True)
