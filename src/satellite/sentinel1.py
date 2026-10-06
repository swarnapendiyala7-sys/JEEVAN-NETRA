import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN_URL = (
    "https://identity.dataspace.copernicus.eu/"
    "auth/realms/CDSE/protocol/openid-connect/token"
)

PROCESS_URL = "https://sh.dataspace.copernicus.eu/process/v1"


def get_access_token():
    client_id = os.getenv("CDSE_CLIENT_ID")
    client_secret = os.getenv("CDSE_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise RuntimeError("Copernicus credentials are missing from .env")

    response = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        },
        timeout=30,
    )

    response.raise_for_status()
    return response.json()["access_token"]


def get_vijayawada_sentinel1(output_file="vijayawada_sentinel1.png"):
    token = get_access_token()

    # Approximate Vijayawada city-area bounding box
    bbox = [80.55, 16.45, 80.75, 16.60]

    evalscript = """
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

    request_body = {
        "input": {
            "bounds": {
                "bbox": bbox,
                "properties": {
                    "crs": "http://www.opengis.net/def/crs/EPSG/0/4326"
                }
            },
            "data": [
                {
                    "type": "sentinel-1-grd",
                    "dataFilter": {
                        "timeRange": {
                            "from": "2026-09-01T00:00:00Z",
                            "to": "2026-10-02T23:59:59Z"
                        }
                    },
                    "processing": {
                        "orthorectify": "true"
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
        "evalscript": evalscript
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        PROCESS_URL,
        headers=headers,
        json=request_body,
        timeout=120
    )

    print("Sentinel-1 HTTP Status:", response.status_code)

    if not response.ok:
        print(response.text)
        response.raise_for_status()

    with open(output_file, "wb") as file:
        file.write(response.content)

    print("Satellite image saved:", output_file)


if __name__ == "__main__":
    get_vijayawada_sentinel1()