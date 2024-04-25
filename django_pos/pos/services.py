import requests
from django.conf import settings


def refresh_license(company_id) -> dict:
    server = settings.LICENSE_SERVER
    req = requests.get(f"{server}/licenses/fetch/{company_id}", timeout=5)
    try:
        data = req.json()
        # license = License.objects.get(company_id=company_id)
        # license.active = data.get("active")
        # license.expires = data.get("license_expires")
        # license.save()
        return data
    except Exception as e:
        return {"error": str(e)}
