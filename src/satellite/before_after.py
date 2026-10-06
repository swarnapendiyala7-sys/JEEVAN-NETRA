import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN_URL = (
    "https://identity.dataspace.copernicus.eu/"
    "auth/realms/CDSE/protocol/openid-connect/token"
)

PROCESS_URL = "https://sh.dataspace.copernicus.eu/process/v1"

# Vijayawada area
BBOX = [80.55, 16.45, 80.75, 16.60]

EVALSCRIPT = """
//VERSION=3

function setup() {
    return {
        input: ["VV"],
        output: {
            id: "default",
            bands: 1
        }
    };
}

function evaluatePixel(samples) {
    return [2 * samples.VV];
}
"""


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


def download_sentinel1(date, output_file):
    token = get_access_token()

    payload = {
        "input": {
            "bounds": {
                "bbox": BBOX,
                "properties": {
                    "crs": "http://www.opengis.net/def/crs/EPSG/0/4326"
                }
            },
            "data": [
                {
                    "type": "sentinel-1-grd",
                    "dataFilter": {
                        "timeRange": {
                            "from": f"{date}T00:00:00Z",
                            "to": f"{date}T23:59:59Z"
                        },
                        "mosaickingOrder": "mostRecent"
                    },
                    "processing": {
                        "orthorectify": True
                    }
                }
            ]
        },
        "output": {
            "width": 512,
            "height": 512,
            "responses": [
                {
                    "identifier": "default",
                    "format": {
                        "type": "image/png"
                    }
                }
            ]
        },
        "evalscript": EVALSCRIPT
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        PROCESS_URL,
        headers=headers,
        json=payload,
        timeout=120
    )

    print(f"{date} HTTP Status:", response.status_code)

    if not response.ok:
        print(response.text)
        response.raise_for_status()

    with open(output_file, "wb") as file:
        file.write(response.content)

    print("Saved:", output_file)


if __name__ == "__main__":

    # Available Sentinel-1 acquisition dates found from Catalog
    before_date = "2026-09-10"
    after_date = "2026-09-22"

    download_sentinel1(
        before_date,
        "vijayawada_before.png"
    )

    download_sentinel1(
        after_date,
        "vijayawada_after.png"
    )

    print("\nBoth Sentinel-1 images downloaded successfully.")