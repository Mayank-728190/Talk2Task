import os
import requests
from dotenv import load_dotenv

# ================= LOAD ENV =================

load_dotenv()

PPTGEN_TOKEN = os.getenv("PPTGEN_BEARER_TOKEN")
if not PPTGEN_TOKEN:
    raise RuntimeError("❌ PPTGEN_BEARER_TOKEN not set in .env")

# ================= CONFIG =================

payload = {
    "jsonData": '''{
        "presentation": {
            "template": "title_slide_template.pptx",
            "export_version": "Pptx2013",
            "slides": [
                {
                    "type": "slide",
                    "slide_index": 0,
                    "shapes": [
                        {
                            "name": "Title 1",
                            "content": "Your generated PowerPoint presentation"
                        },
                        {
                            "name": "Subtitle 2",
                            "content": "Create, fill and manage PowerPoint documents through simple API requests."
                        }
                    ]
                }
            ]
        }
    }'''
}

with open("./base_template.pptx", "rb") as pptx_file:
    files = [
        ('files', ('title_slide_template.pptx', pptx_file, 'application/vnd.openxmlformats-officedocument.presentationml.presentation'))
    ]
    
    try:
        print("⏳ Sending request...")
        response = requests.post(
            'https://gen.powerpointgeneratorapi.com/v1.0/generator/create',
            data=payload,
            files=files,
            headers={'Authorization': f'Bearer {PPTGEN_TOKEN}'},
            timeout=360
        )
        
        print("🚀 Response received!")
        
        # Validate response before saving
        if response.status_code == 200:
            with open("./generated.pptx", "wb") as output_file:
                output_file.write(response.content)
            print("✅ PowerPoint file generated successfully!")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Request failed: {e}")