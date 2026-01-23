import os
import requests
from dotenv import load_dotenv
from pathlib import Path

# ================= LOAD ENV =================
load_dotenv()

PPTGEN_TOKEN = os.getenv("PPTGEN_BEARER_TOKEN")
if not PPTGEN_TOKEN:
    raise RuntimeError("❌ PPTGEN_BEARER_TOKEN not set in .env")

# ================= CONFIG =================
PPTGEN_URL = "https://gen.powerpointgeneratorapi.com/v1.0/generator/create"
BASE_DIR = Path(__file__).resolve().parents[3]
TEMPLATE_PATH = BASE_DIR / "base_template.pptx"

def generate_ppt_with_pptgen(slides_json: str) -> bytes:
    """
    slides_json: stringified JSON for PPTGEN (jsonData)
    returns: pptx bytes
    """

    if not TEMPLATE_PATH.exists():
        raise RuntimeError("❌ base_template.pptx not found")

    payload = {
        "jsonData": slides_json
    }

    with open(TEMPLATE_PATH, "rb") as pptx_file:
        response = requests.post(
            PPTGEN_URL,
            headers={
                "Authorization": f"Bearer {PPTGEN_TOKEN}"
            },
            data=payload,
            files={
                "files": (
                    "base_template.pptx",
                    pptx_file,
                    "application/vnd.openxmlformats-officedocument.presentationml.presentation"
                )
            },
            timeout=360
        )

    if response.status_code != 200:
        raise RuntimeError(
            f"PPTGen API error {response.status_code}: {response.text}"
        )

    return response.content
