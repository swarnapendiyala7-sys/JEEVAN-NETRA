import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN_URL = (
    "https://identity.dataspace.copernicus.eu/"
    "auth/realms/CDSE/protocol/openid-connect/token"
)

CATALOG_URL = "https://sh.dataspace.copernicus.eu/catalog/v1/search"

BBOX = [80.55, 16.45, 80.75, 16.60]


def get_access_token():
    response = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "client_credentials",
            "client_id": os.getenv("CDSE_CLIENT_ID"),
            "client_secret": os.getenv("CDSE_CLIENT_SECRET"),
        },
        timeout=30,
    )

    response.raise_for_status()
    return response.json()["access_token"]


def search_sentinel1():
    token = get_access_token()

    payload = {
        "bbox": BBOX,
        "datetime": "2026-08-01T00:00:00Z/2026-10-02T23:59:59Z",
        "collections": ["sentinel-1-grd"],
        "limit": 100,
        "distinct": "date",
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        CATALOG_URL,
        headers=headers,
        json=payload,
        timeout=60,
    )

    print("Catalog HTTP Status:", response.status_code)

    response.raise_for_status()

    data = response.json()

    print("\nAvailable Sentinel-1 dates for Vijayawada:\n")

    for date in data.get("features", []):
        print("Date:", date)


if __name__ == "__main__":
    search_sentinel1()