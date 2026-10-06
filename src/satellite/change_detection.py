import os
import requests
import numpy as np
from dotenv import load_dotenv
from PIL import Image

load_dotenv()

TOKEN_URL = (
    "https://identity.dataspace.copernicus.eu/"
    "auth/realms/CDSE/protocol/openid-connect/token"
)

PROCESS_URL = "https://sh.dataspace.copernicus.eu/process/v1"

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


def download_radar_data(date, output_file):
    token = get_access_token()

    # Return VV and VH as numerical values
    evalscript = """
    //VERSION=3

    function setup() {
        return {
            input: ["VV", "VH"],
            output: {
                bands: 2,
                sampleType: "FLOAT32"
            }
        };
    }

    function evaluatePixel(samples) {
        return [
            samples.VV,
            samples.VH
        ];
    }
    """

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
                        "type": "image/tiff"
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


def main():

    print("Downloading numerical Sentinel-1 data...")

    download_radar_data(
        "2026-09-10",
        "vijayawada_before.tiff"
    )

    download_radar_data(
        "2026-09-22",
        "vijayawada_after.tiff"
    )

    print("\nVV/VH radar data downloaded successfully.")


if __name__ == "__main__":
    main()